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
import urllib2

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
from entity.validation import validate

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

def _get_username(request):
    return u'%s <%s>' % (
            request.user.get_full_name() or request.user.username,
            request.user.email or request.user.username)

@login_required
def text_edit_metadata(request, entity_id):
    entity = Entity.objects.get(pk=entity_id)
    if request.method == 'POST':
        form = MetadataTextEditForm(request.POST)
        text = form['metadata_text'].data
        if not text:
            form.errors['metadata_text'] = [_('Empty metadata not allowed')]
        else:
            errors = validate(text)
            if errors:
                form.errors['metadata_text'] = errors
        if form.is_valid():
            tmp = NamedTemporaryFile(delete=True)
            tmp.write(text.encode('utf8'))
            tmp.seek(0)
            content = File(tmp)
            name = entity.metadata.name
            username = _get_username(request)
            commit_msg = form['commit_msg_text'].data.encode('utf8')
            entity.metadata.save(name, content, username, commit_msg)
            entity.save()
            messages.success(request, _('Entity metadata has been modified'))
        else:
            messages.error(request, _('Please correct the errors'
                                      ' indicated below'))
    else:
        form = None
    return edit_metadata(request, entity.id, text_form=form,
                         accordion_activate='text')


@login_required
def file_edit_metadata(request, entity_id):
    entity = Entity.objects.get(pk=entity_id)
    if request.method == 'POST':
        form = MetadataFileEditForm(request.POST, request.FILES)
        content = form['metadata_file'].data
        if content is not None:
            text = content.read()
            content.seek(0)
            if not text:
                form.errors['metadata_file'] = [_('Empty metadata not allowed')]
            else:
                errors = validate(text)
                if errors:
                    form.errors['metadata_file'] = errors
        if form.is_valid():
            name = entity.metadata.name
            username = _get_username(request)
            commit_msg = form['commit_msg_text'].data.encode('utf8')
            entity.metadata.save(name, content, username, commit_msg)
            entity.save()
            messages.success(request, _('Entity metadata has been modified'))
        else:
            messages.error(request, _('Please correct the errors'
                                      ' indicated below'))
    else:
        form = None
    return edit_metadata(request, entity.id, accordion_activate='upload',
                         file_form=form)


@login_required
def remote_edit_metadata(request, entity_id):
    entity = Entity.objects.get(pk=entity_id)
    if request.method == 'POST':
        form = MetadataRemoteEditForm(request.POST)
        content_url = form['metadata_url'].data
        try:
            resp = urllib2.urlopen(content_url, None, CONNECTION_TIMEOUT)
        except urllib2.URLError, e:
            form.errors['metadata_url'] = ['URL Error: '+str(e)]
        except urllib2.HTTPError, e:
            form.errors['metadata_url'] = ['HTTP Error: '+str(e)]
        else:
            if resp.getcode() != 200:
                form.errors['metadata_url'] = [_(
                                      'Error getting the data: %s'
                                                ) % resp.msg]
            text = resp.read()
            if not text:
                form.errors['metadata_url'] = [_('Empty metadata not allowed')]
            else:
                errors = validate(text)
                if errors:
                    form.errors['metadata_url'] = errors
            try:
                encoding = resp.headers['content-type'].split('charset=')[1]
            except (KeyError, IndexError):
                encoding = ''
            resp.close()
        if form.is_valid():
            tmp = NamedTemporaryFile(delete=True)
            if encoding:
                text = text.decode(encoding).encode('utf8')
            tmp.write(text)
            tmp.seek(0)
            content = File(tmp)
            name = entity.metadata.name
            username = _get_username(request)
            commit_msg = form['commit_msg_text'].data.encode('utf8')
            entity.metadata.save(name, content, username, commit_msg)
            entity.save()
            messages.success(request, _('Entity metadata has been modified'))
        else:
            messages.error(request, _('Please correct the errors'
                                      ' indicated below'))
    else:
        form = None
    return edit_metadata(request, entity.id, accordion_activate='remote',
                         remote_form=form)


@login_required
def edit_metadata(request, entity_id, accordion_activate='text',
                  text_form=None, file_form=None, remote_form=None):
    entity = Entity.objects.get(pk=entity_id)

    return render_to_response('entity/edit_metadata.html', {
            'entity': entity,
            'text_html': _get_edit_metadata_form(request, entity, 'text',
                                                 form=text_form),
            'file_html': _get_edit_metadata_form(request, entity, 'file',
                                                 form=file_form),
            'remote_html': _get_edit_metadata_form(request, entity, 'remote',
                                                   form=remote_form),
            'activate': accordion_activate,

            }, context_instance=RequestContext(request))
