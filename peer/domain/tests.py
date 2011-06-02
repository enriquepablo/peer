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

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import httplib2

from django.test import TestCase

import fudge

from domain.validation import validate_ownership


class ValidationTest(TestCase):

    @fudge.patch('httplib2.Http')
    def test_validate_ownership(self, FakeHttp):
        url = 'http://www.example.com/non_valid_key'
        (FakeHttp.expects_call()
                 .returns_fake()
                 .expects('request')
                 .with_args(url)
                 .returns(
                   ({'status': '404'}, '')
                 ))
        self.assertEquals(False, validate_ownership(url))

        url = 'http://www.example.com/valid_key'
        (FakeHttp.expects_call()
                 .returns_fake()
                 .expects('request')
                 .with_args(url)
                 .returns(
                   ({'status': '200'}, '')
                 ))

        self.assertEquals(True, validate_ownership(url))

        url = 'http://www.invalid-domain.com/garbage'
        (FakeHttp.expects_call()
                 .returns_fake()
                 .expects('request')
                 .with_args(url)
                 .raises(httplib2.ServerNotFoundError())
                 .returns(
                   ({'status': '200'}, '')
                 ))

        self.assertEquals(False, validate_ownership(url))
