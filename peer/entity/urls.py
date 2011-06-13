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

from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
    'entity.views',
    url(r'^$', 'entities_list', name='entities_list'),
    url(r'^add$', 'entity_add', name='entity_add'),
    url(r'^(?P<domain_name>\w.+)/add$', 'entity_add_with_domain',
        name='entity_add_with_domain'),
    url(r'^(?P<entity_id>\d+)$', 'entity_view', name='entity_view'),
    url(r'^(?P<entity_id>\d+)/remove/$', 'entity_remove', name='entity_remove'),
    url(r'^(?P<entity_id>\d+)/edit_metadata/$', 'edit_metadata', name='edit_metadata'),
    url(r'^(?P<entity_id>\d+)/text_edit_metadata/$', 'text_edit_metadata', name='text_edit_metadata'),
    url(r'^(?P<entity_id>\d+)/file_edit_metadata/$', 'file_edit_metadata', name='file_edit_metadata'),
    url(r'^(?P<entity_id>\d+)/remote_edit_metadata/$', 'remote_edit_metadata', name='remote_edit_metadata'),
)
