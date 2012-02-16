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

import re

from pygments import highlight
from pygments.lexers import XmlLexer, DiffLexer
from pygments.formatters import HtmlFormatter

from django import db
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.utils import DatabaseError
from django.db import transaction
from django.utils.translation import ugettext as _

from peer.entity.filters import get_filters, filter_entities
from peer.entity.forms import EditMetarefreshForm
from peer.entity.forms import EditMonitoringPreferencesForm
from peer.entity.models import Entity, PermissionDelegation
from peer.entity.security import can_edit_entity
from peer.entity.security import can_change_entity_team
from peer.entity.utils import is_subscribed, add_subscriber, remove_subscriber
from peer.entity.paginator import paginated_list_of_entities


@login_required
def metarefresh_edit(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
    if not can_edit_entity(request.user, entity):
        raise PermissionDenied

    if request.method == 'POST':
        form = EditMetarefreshForm(request.POST)
        if form.is_valid():
            entity.metarefresh_frequency = \
                    form.cleaned_data['metarefresh_frequency']
            entity.save()
            messages.success(request, _('Metarefresh edited succesfully'))
            return HttpResponseRedirect(reverse('metarefresh_edit',
                                                args=(entity_id,)))
        else:
            messages.error(request, _('Please correct the errors'
                                      ' indicated below'))
    else:
        form = EditMetarefreshForm(instance=entity)

    return render_to_response('entity/edit_metarefresh.html', {
            'entity': entity,
            'form': form,
            }, context_instance=RequestContext(request))



def _search_entities(search_terms):
    lang = getattr(settings, 'PG_FT_INDEX_LANGUAGE', u'english')
    sql = u"select * from entity_entity where to_tsvector(%s, name) @@ to_tsquery(%s, %s)"
    return Entity.objects.raw(sql, [lang, lang, search_terms])


def search_entities(request):
    search_terms_raw = request.GET.get('query', '').strip()
    op = getattr(settings, 'PG_FTS_OPERATOR', '&')
    sid = transaction.savepoint()
    if db.database['ENGINE'] == 'django.db.backends.postgresql_psycopg2':
        search_terms = re.sub(ur'\s+', op, search_terms_raw)
        entities = _search_entities(search_terms)
    else:
        search_terms_list = search_terms_raw.split(' ')
        where = (u' %s ' % op).join([u"name ilike '%s'"] * len(search_terms_list))
        sql = u"select * from entity_entity where " + where
        entities = Entity.objects.raw(sql, search_terms_list)
        search_terms = op.join(search_terms_raw)

    try:
        entities = list(entities)
    except DatabaseError:
        transaction.savepoint_rollback(sid)
        entities = []
        msg = _(u'There seem to be illegal characters in your search.\n'
                u'You should not use !, :, &, | or \\')
        messages.error(request, msg)
    else:
        if search_terms_raw == '':
            entities = Entity.objects.all()
        else:
            n = len(entities)
            plural = n == 1 and 'entity' or 'entities'
            msg = _(u'Found %d %s matching "%s"') % (n, plural,
                                                     search_terms_raw)
            messages.success(request, msg)

    filters = get_filters(request.GET)
    entities = filter_entities(filters, entities)

    query_string = [u'%s=%s' % (f.name, f.current_value)
                    for f in filters if not f.is_empty()]
    if search_terms_raw:
        query_string.append(u'query=%s' % search_terms_raw)

    paginated_entities = paginated_list_of_entities(request, entities)
    return render_to_response('entity/search_results.html', {
            'entities': paginated_entities,
            'search_terms': search_terms_raw,
            'filters': filters,
            'query_string': u'&'.join(query_string),
            }, context_instance=RequestContext(request))


# SHARING ENTITY EDITION

@login_required
def sharing(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
    if not can_change_entity_team(request.user, entity):
        raise PermissionDenied

    return render_to_response('entity/sharing.html', {
            'entity': entity,
            }, context_instance=RequestContext(request))


@login_required
def list_delegates(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
    if not can_change_entity_team(request.user, entity):
        raise PermissionDenied

    return render_to_response('entity/delegate_list.html', {
            'delegates': entity.delegates.all(),
            'entity_id': entity.pk,
            }, context_instance=RequestContext(request))


@login_required
def remove_delegate(request, entity_id, user_id):
    entity = get_object_or_404(Entity, id=entity_id)
    if not can_change_entity_team(request.user, entity):
        raise PermissionDenied

    delegate = User.objects.get(pk=user_id)
    if entity and delegate:
        delegations = PermissionDelegation.objects.filter(entity=entity,
                                                  delegate=delegate)
        for delegation in delegations:
            delegation.delete()
    return list_delegates(request, entity_id)


@login_required
def add_delegate(request, entity_id, username):
    entity = get_object_or_404(Entity, id=entity_id)
    if not can_change_entity_team(request.user, entity):
        raise PermissionDenied

    new_delegate = User.objects.get(username=username)
    if entity and new_delegate:
        pd = PermissionDelegation.objects.filter(entity=entity,
                                                delegate=new_delegate)
        if not pd and new_delegate != entity.owner:
            pd = PermissionDelegation(entity=entity, delegate=new_delegate)
            pd.save()
        elif pd:
            return HttpResponse('delegate')
        else:
            return HttpResponse('owner')
    return list_delegates(request, entity_id)


@login_required
def make_owner(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
    if not can_change_entity_team(request.user, entity):
        raise PermissionDenied

    old_owner = entity.owner
    new_owner_id = request.POST.get('new_owner_id')
    if new_owner_id:
        new_owner = User.objects.get(pk=int(new_owner_id))
        if new_owner:
            entity.owner = new_owner
            entity.save()
            msg = _('New owner successfully set')
            old_pd = PermissionDelegation.objects.get(entity=entity,
                                                  delegate=new_owner)
            if old_pd:
                old_pd.delete()
            if old_owner:
                new_pd = PermissionDelegation.objects.filter(entity=entity,
                                              delegate=old_owner)
                if not new_pd:
                    new_pd = PermissionDelegation(entity=entity,
                                                  delegate=old_owner)
                    new_pd.save()
        else:
            msg = _('User not found')
    else:
        msg = _('You must provide the user id of the new owner')
    messages.success(request, msg)
    return HttpResponseRedirect(reverse('entity_view', args=(entity_id,)))


# Monitor endpoints

@login_required
def monitoring_prefs(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)

    initial = {'want_alerts': is_subscribed(entity, request.user)}

    if request.method == 'POST':
        form = EditMonitoringPreferencesForm(request.POST, initial=initial)
        if form.is_valid():
            want_alerts = form.cleaned_data['want_alerts']
            if want_alerts:
                add_subscriber(entity, request.user)
                msg = _("You are subscribed to this entity's alerts")
            else:
                remove_subscriber(entity, request.user)
                msg = _("You are not subscribed anymore to this entity's alerts")
            entity.save()
            messages.success(request, msg)
            return HttpResponseRedirect(reverse('entity_view',
                                                args=(entity_id, )))
        else:
            messages.error(request,
                           _('Please correct the errors indicated below'))
    else:
        form = EditMonitoringPreferencesForm(initial=initial)

    return render_to_response('entity/edit_monitoring_preferences.html', {
            'entity': entity,
            'form': form,
            }, context_instance=RequestContext(request))


# ENTITY DETAILS

HTML_WRAPPER = u'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>%s - %s</title>
</head>
<body>
%s
</body>
</html>
'''


def get_diff(request, entity_id, r1, r2):
    entity = get_object_or_404(Entity, id=entity_id)
    diff = entity.metadata.get_diff(r1, r2)
    formatter = HtmlFormatter(linenos=True)
    html = HTML_WRAPPER % (entity_id, u'%s:%s' % (r1, r2),
                           highlight(diff, DiffLexer(), formatter))
    return HttpResponse(html.encode(settings.DEFAULT_CHARSET))


#import difflib
#def get_diff2(request, entity_id, r1, r2):
#    entity = get_object_or_404(Entity, id=entity_id)
#    md1 = entity.metadata.get_revision(r1).split('\n')
#    md2 = entity.metadata.get_revision(r2).split('\n')
#    html = difflib.HtmlDiff().make_table(md1, md2)
#    return HttpResponse(html)


def get_revision(request, entity_id, rev):
    entity = get_object_or_404(Entity, id=entity_id)
    md = entity.metadata.get_revision(rev)
    formatter = HtmlFormatter(linenos=True)
    html = HTML_WRAPPER % (entity_id, rev,
                           highlight(md, XmlLexer(), formatter))
    return HttpResponse(html.encode(settings.DEFAULT_CHARSET))


def get_latest_metadata(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
    metadata_text = entity.metadata.get_revision()
    return HttpResponse(metadata_text, mimetype="application/samlmetadata+xml")


@cache_page
def get_pygments_css(request):
    formatter = HtmlFormatter(linenos=True, outencoding='utf-8')
    return HttpResponse(content=formatter.get_style_defs(arg=''),
                    mimetype='text/css',
                content_type='text/css; charset=' + settings.DEFAULT_CHARSET)
