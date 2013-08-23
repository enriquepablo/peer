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


import datetime
import hashlib
import whois

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.template import Context
from django.utils.encoding import smart_str
from django.utils.translation import ugettext as _


def get_custom_user_agent():
    if hasattr(settings, 'DOP_USER_AGENT'):
        return settings.DOP_USER_AGENT
    else:
        return None


def generate_validation_key(domain_name, domain_owner=None):
    """ Generates a unique validation key """
    m = hashlib.sha256()
    m.update(smart_str(domain_name))

    # add also current datetime and owner for more security
    m.update(datetime.datetime.now().isoformat())
    if domain_owner:
        m.update(domain_owner)

    return m.hexdigest()


def send_mail_for_validation(request, domain, token, mailto):
    url_prefix = 'http'
    if request.is_secure():
        url_prefix += 's'
    relative_path = reverse('domain_verify',
                             kwargs={'domain_id': domain.id, 'token': token})
    validation_url = "%s://%s%s" % (url_prefix, request.get_host(), relative_path)

    plaintext = get_template('domain/validation_by_mail.txt')
    htmly = get_template('domain/validation_by_mail.html')

    data = Context({'domain_name': domain.name, 'validation_url': validation_url})
    subject = _("Activate domain %(domain_name)s") % {'domain_name': domain.name}
    text_content = plaintext.render(data)
    html_content = htmly.render(data)
    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [mailto])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def get_administrative_emails(domain_name):
    administrative_emails = []
    default_administrative_email_addresses = getattr(settings, 'ADMINISTRATIVE_EMAIL_ADDRESSES', [])
    for default_administrative_email_address in default_administrative_email_addresses:
        administrative_emails.append('%s@%s' % (default_administrative_email_address, domain_name))

    whois_data = whois.whois(domain_name)
    if whois_data:
        administrative_emails += whois_data.emails
    administrative_emails = list(set(administrative_emails))
    return administrative_emails


