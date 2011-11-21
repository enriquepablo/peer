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

import urlparse

from lxml import etree
from django.utils.importlib import import_module
from django.conf import settings

from peer.entity.models import Metadata
from peer.entity.utils import NAMESPACES


def validate(entity, doc):
    """
    Call all validators defined in in settings.METADATA_VALIDATORS
    on the xml given as a string (doc). Information about the
    entity this metadata is validating for is passed in the first
    argument (entity).

    Each entry in METADATA_VALIDATORS is a string with the import path
    to a callable that accepts a string as input and returns a list
    of strings describing errors, or an empty list on no errors.
    """
    try:
        validators = settings.METADATA_VALIDATORS
    except AttributeError:
        validators = []
    errors = set()
    for v in validators:
        val_list = v.split('.')
        mname = '.'.join(val_list[:-1])
        cname = val_list[-1]
        module = import_module(mname)
        validator = getattr(module, cname)
        errors.update(validator(entity, doc))
    return list(errors)


def _parse_metadata(doc):
    """Aux function that returns a list of errors and a metadata object"""
    try:
        metadata = Metadata(etree.XML(doc))
    except etree.XMLSyntaxError, e:
        # XXX sin traducir (como traducimos e.msg?)
        error = e.msg or 'Unknown error, perhaps an empty doc?'
        return [u'XML syntax error: ' + error], None
    else:
        return [], metadata


def validate_xml_syntax(entity, doc):
    """
    Check that the provided string contains syntactically valid xml,
    simply by trying to parse it with lxml.
    """
    return _parse_metadata(doc)[0]


def validate_domain_in_endpoints(entity, doc):
    """
    Makes sure the endpoints urls belongs to the domain of the entity
    """
    errors, metadata = _parse_metadata(doc)
    if errors:
        return errors

    domain = entity.domain.name

    for endpoint in metadata.endpoints:
        url = urlparse.urlparse(endpoint['Location'])
        if url.netloc.lower() != domain.lower():
            errors.append(
                u'The endpoint at %s does not belong to the domain %s' %
                (endpoint['Location'], domain))

    return errors


def validate_domain_in_entityid(entity, doc):
    """
    Makes sure the entityid url belongs to the domain of the entity
    """
    errors, metadata = _parse_metadata(doc)
    if errors:
        return errors

    domain = entity.domain.name

    url = urlparse.urlparse(metadata.entityid)
    if url.netloc.lower() != domain.lower():
        errors.append(
            u'The entityid does not belong to the domain %s' % domain)

    return errors


def validate_metadata_permissions(entity, doc):
    """
    Checks whether the user has permission to change the attributes of an
    entity.
    """
    errors, metadata = _parse_metadata(doc)
    if errors:
        return errors

    new_etree = metadata.etree
    old_etree = entity.metadata_etree

    if old_etree == new_etree:
        return errors

    permissions = settings.METADATA_PERMISSIONS

    for xpath_str, permission in permissions.iteritems():
        if old_etree is not None:
            old_elems = old_etree.xpath(xpath_str, namespaces=NAMESPACES)
        else:
            old_elems = list()
        new_elems = new_etree.xpath(xpath_str, namespaces=NAMESPACES)

        # Element addition
        if len(old_elems) < len(new_elems) and \
           'a' not in permission:
            errors.append(u'Addition is forbidden in element %s' %
                          (new_elems[0].tag))

        # Element deletion
        elif len(old_elems) > len(new_elems) \
            and 'd' not in permission:
            errors.append(u'Deletion is forbidden in element %s' %
                          (new_elems[0].tag))

        # Element modification
        elif (old_elems and new_elems) and \
            (len(old_elems) == len(new_elems)) and \
            'w' not in permission:
            for old_elem, new_elem in zip(old_elems, new_elems):
                if old_elem.values() != new_elem.values():
                    errors.append(
                        u'Value modification is forbidden for element %s' %
                        (new_elem.tag))

                    break
    return errors
