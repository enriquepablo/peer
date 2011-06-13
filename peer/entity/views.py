# Copyright 2011 Terena. All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:

#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.

#    2. Redistributions in binary form must reproduce the above copyright notice,
#       this list of conditions and the following disclaimer in the documentation
#        and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY TERENA ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL TERENA OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies,
# either expressed or implied, of Terena.

from tempfile import NamedTemporaryFile
import httplib2

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.files.base import File
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils.translation import ugettext as _

from domain.models import Domain
from entity.forms import EntityForm, MetadataTextEditForm
from entity.forms import MetadataFileEditForm, MetadataRemoteEditForm
from entity.models import Entity

from vff.storage import create_fname

CONNECTION_TIMEOUT = 10


def get_entities_per_page():
    if hasattr(settings, 'ENTITIES_PER_PAGE'):
        return settings.ENTITIES_PER_PAGE
    else:
        return 10


def entities_list(request):
    entities = Entity.objects.all()
    paginator = Paginator(entities, get_entities_per_page())

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        entities = paginator.page(page)
    except (EmptyPage, InvalidPage):
        entities = paginator.page(paginator.num_pages)

    return render_to_response('entity/list.html', {
            'entities': entities,
            }, context_instance=RequestContext(request))


@login_required
def entity_add(request):
    return entity_add_with_domain(request, None, 'entities_list')


@login_required
def entity_add_with_domain(request, domain_name=None,
                           return_view_name='account_profile'):
    if domain_name is None:
        entity = None
    else:
        domain = get_object_or_404(Domain, name=domain_name)
        entity = Entity(domain=domain)

    if request.method == 'POST':
        form = EntityForm(request.user, request.POST, instance=entity)
        if form.is_valid():
            form.save()
            messages.success(request, _('Entity created succesfully'))
            return HttpResponseRedirect(reverse(return_view_name))

    else:
        form = EntityForm(request.user, instance=entity)

    return render_to_response('entity/add.html', {
            'form': form,
            }, context_instance=RequestContext(request))


def entity_view(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
    return render_to_response('entity/view.html', {
            'entity': entity,
            }, context_instance=RequestContext(request))


@login_required
def entity_remove(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
    if request.method == 'POST':
        entity.delete()
        messages.success(request, _('Entity removed succesfully'))
        return HttpResponseRedirect(reverse('entities_list'))

    return render_to_response('entity/remove.html', {
            'entity': entity,
            }, context_instance=RequestContext(request))

# METADATA EDIT


def _get_edit_metadata_form(request, entity, edit_mode, form=None):
    if form is None:
        if edit_mode == 'text':
            fname = create_fname(entity, 'metadata')
            text = entity.metadata.storage.get_revision(fname)
            form = MetadataTextEditForm(initial={'metadata_text': text})
        elif edit_mode == 'file':
            # XXX siempre vacia, imborrable, required
            form = MetadataFileEditForm()
        elif edit_mode == 'remote':
            form = MetadataRemoteEditForm()
    form_action = reverse('%s_edit_metadata' % edit_mode, args=(entity.id, ))

    context_instance = RequestContext(request)
    return render_to_string('entity/simple_edit_metadata.html', {
        'edit': edit_mode,
        'entity': entity,
        'form': form,
        'form_action': form_action,
    }, context_instance=context_instance)

def text_edit_metadata(request, entity_id):
    entity = Entity.objects.get(pk=entity_id)
    if request.method == 'POST':
        form = MetadataTextEditForm(request.POST)
        if form.is_valid():
            text = form['metadata_text'].data
            tmp = NamedTemporaryFile(delete=True)
            tmp.write(text.encode('utf8'))
            tmp.seek(0)
            content = File(tmp)
            name = entity.metadata.name
            entity.metadata.save(name, content)
            entity.vff_commit_msg = form['commit_msg_text'].data.encode('utf8')
            entity.save()
            messages.success(request, _('Entity metadata has been modified'))
        else:
            messages.error(request, _('Please correct the errors'
                                      ' indicated below'))
    else:
        form = None
    return edit_metadata(request, entity.id, text_form=form)

def file_edit_metadata(request, entity_id):
    entity = Entity.objects.get(pk=entity_id)
    if request.method == 'POST':
        form = MetadataFileEditForm(request.POST, request.FILES)
        if form.is_valid():
            content = form['metadata_file'].data
            name = entity.metadata.name
            entity.metadata.save(name, content)
            entity.vff_commit_msg = form['commit_msg_file'].data.encode('utf8')
            entity.save()
            messages.success(request, _('Entity metadata has been modified'))
        else:
            messages.error(request, _('Please correct the errors'
                                      ' indicated below'))
    else:
        form = None
    return edit_metadata(request, entity.id, accordion_activate=1,
                                              file_form=form)

def remote_edit_metadata(request, entity_id):
    entity = Entity.objects.get(pk=entity_id)
    if request.method == 'POST':
        form = MetadataRemoteEditForm(request.POST)
        content_url = form['metadata_url'].data
        http = httplib2.Http(timeout=CONNECTION_TIMEOUT)
        try:
            resp, text = http.request(content_url)
        except httplib2.ServerNotFoundError:
            form.errors['metadata_url'] = [_('Server not found')]
        except httplib2.RelativeURIError:
            form.errors['metadata_url'] = [_('Relative URLs are not allowed')]
        else:
            if resp.status != 200:
                form.errors['metadata_url'] = [_(
                                      'Error getting the data: %s'
                                                ) % resp.reason]
            try:
                encoding = resp['content-type'].split('=')[1]
            except (KeyError, IndexError):
                encoding = ''
        if form.is_valid():
            tmp = NamedTemporaryFile(delete=True)
            if encoding:
                text = text.decode(encoding).encode('utf8')
            tmp.write(text)
            tmp.seek(0)
            content = File(tmp)
            name = entity.metadata.name
            entity.metadata.save(name, content)
            entity.vff_commit_msg = form['commit_msg_remote'].data.encode('utf8')
            entity.save()
            messages.success(request, _('Entity metadata has been modified'))
        else:
            messages.error(request, _('Please correct the errors'
                                      ' indicated below'))
    else:
        form = None
    return edit_metadata(request, entity.id, accordion_activate=2,
                                             remote_form=form)

def edit_metadata(request, entity_id, accordion_activate=0,
                  text_form=None, file_form=None, remote_form=None):
    entity = Entity.objects.get(pk=entity_id)
    context = {'entity': entity}
    context['text_html'] = _get_edit_metadata_form(request, entity, 'text',
                                                        form=text_form)
    context['file_html'] = _get_edit_metadata_form(request, entity, 'file',
                                                        form=file_form)
    context['remote_html'] = _get_edit_metadata_form(request, entity,
                                                'remote', form=remote_form)
    context['activate'] = accordion_activate

    return render_to_response('entity/edit_metadata.html',
            context, context_instance=RequestContext(request))
