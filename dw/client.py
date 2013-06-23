#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Python Demandware SDK provides access to the OCAPI services.
# Copyright (C) 2013  Moises Brenes
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#   Moises Brenes <mbrenes@weareconflict.com>

import json
import httplib
import urllib
import urllib2
import cookielib

from . import __version__
from objects import Object
from errors import ParameterInvalidError, ParameterMissedError

###############################################################
# Demandware Library
###############################################################
class Demandware(object):
    """
    Python Demandware SDK.

    https://documentation.demandware.com/display/DOC131/Open+Commerce+API

    """
    __USER_AGENT = 'Demandware Python SDK/%s' % __version__

    __cookie = None

    __last_call = Object()

    __required = set((
        'client_id',
        'hostname',
        'site',
        'version',
    ))

    def __init__(self, params=dict()):
        """
        Set a client to consume OCAPI services.

        Examples:

        params=dict({
            'client_id': '',
            'hostname': '',
            'site': '',
            'version': '',
        })

        Args:

        ``params``: Dictionary that contains settings to be applied,
        all keys are required.

        Raises:

        ``ParameterInvalidError``: If an invalid parameter is detected.

        ``ParameterMissedError``: If an parameter is missed.

        """
        args = set(params.keys())
        diff = self.__required.symmetric_difference(args)

        for arg in diff:
            if arg in self.__required:
                raise ParameterMissedError('%s' % arg)
            elif arg in args:
                raise ParameterInvalidError('%s' % arg)

        self.__client_id = params.get('client_id')
        self.__hostname = params.get('hostname')
        self.__site = params.get('site')
        self.__version = params.get('version')

        self._reset()
        self._debug()
        self._set_cookie()

    def _set_cookie(self):
        """
        Store cookie.

        """
        self.__cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.__cookie))
        opener.addheaders = [('User-agent', self.__USER_AGENT)]
        urllib2.install_opener(opener)

    def _unset_cookie(self):
        """
        Remove cookie.

        """
        if self.__cookie is not None:
            self.__cookie.clear()

    def _reset(self):
        """
        Restore default values used to request a service.

        """
        self.__secure = False
        self.__method = 'GET'

        self.__headers = {
            'User-Agent': self.__USER_AGENT,
            'x-dw-client-id': self.__client_id,
        }

        self.__get = {
            'format': 'json',
            'client_id': self.__client_id
        }

        self.__post = {
        }

    def _debug(self):
        """
        Lets inspect request and response data.

        Returns:

        Dictionary with request and response keys.

        """
        self.__debug = {
            'request': {
                'headers': self.__headers,
                'get': self.__get,
                'post': self.__post,
                'method': self.__method,
            },
            'response': {
                'info': {},
                'headers': {},
                'body': {},
            },
        }

    def _call(self, uri):
        """
        Execute a request and save last response data.

        Args:

        ``uri``: String that represents resource path.

        """
        protocol = 'https' if self.__secure else 'http'
        url = '%s://%s/s/%s/dw/shop/%s/%s?&%s' % (
            protocol,
            self.__hostname,
            self.__site,
            self.__version,
            uri,
            urllib.urlencode(self.__get),
        )

        self._debug()

        request = urllib2.Request(url=url, headers=self.__headers)

        if self.__method == 'POST':
            request.add_data(json.dumps(self.__post))
        try:
            response = urllib2.urlopen(request)
        except IOError, e:
            self.__debug['response']['info'] = {'code': None, 'reason': e}
        except urllib2.URLError, e:
            self.__debug['response']['info'] = {'code': None, 'reason': e.reason}
        except urllib2.HTTPError, e:
            self.__debug['response']['info'] = {'code': e.code, 'reason': e.msg}
        else:
            self.__debug['response']['info'] = {'code': response.getcode(), 'url': response.geturl()}
            self.__debug['response']['headers'] = dict(response.info())

            try:
                self.__debug['response']['body'] = json.loads(response.read())
            except ValueError:
                self.__debug['response']['body'] = json.loads(str(dict()))


        self.__last_call = Object(self.__debug)

        self._reset()

    def set_header(self, key, value):
        """
        Add or update HEADERS data.

        Args:

        ``key``: String that represents key in HEADERS parameters.
        ``value``: Value to be saved.

        """
        self.__headers.update({str(key): value})

    def set_get(self, key, value):
        """
        Add or update GET data.

        Args:

        ``key``: String that represents key in GET parameters.
        ``value``: Value to be saved.

        """
        self.__get.update({str(key): value})

    def set_post(self, key, value):
        """
        Add or update POST data.

        Args:

        ``key``: String that represents key in POST parameters.
        ``value``: Value to be saved.

        """
        self.__post.update({str(key): value})

    def get(self, key=None):
        """
        Lets inspect current GET data.

        Args:

        ``key``: String  that represents key in GET that should be returned.

        Returns:

        Value for key or all GET dictionary.

        """
        if key is not None:
            return self.__get.get(str(key))
        else:
            return self.__get

    def post(self, key=None):
        """
        Lets inspect current POST data.

        Args:

        ``key``: String  that represents key in POST that should be returned.

        Returns:

        Value for key or all POST dictionary.

        """
        if key is not None:
            return self.__post.get(str(key))
        else:
            return self.__post

    def header(self, key=None):
        """
        Lets inspect current HEADERS used to request an service.

        Args:

        ``key``: String that represents a HEADER that should be returned.

        Returns:

        Value for key or all HEADERS dictionary.

        """
        if key is not None:
            return self.__headers.get(str(key))
        else:
            return self.__headers

    def get_response(self, as_dict=False):
        """
        Lets inspect last response.

        Args:

        ``as_dict``: Boolean that indicates if should returns as object or dictionary.

        Returns:

        Last response as object or dictionary, it depends of as_dict.

        """
        if as_dict:
            return self.__debug['response']
        else:
            return self.__last_call

    def get_request(self, as_dict=False):
        """
        Lets inspect last request.

        Args:

        ``as_dict``: Boolean that indicates if should returns as object or dictionary.

        Returns:

        Last request as object or dictionary, it depends of as_dict.

        """
        if as_dict:
            return self.__debug['request']
        else:
            return self.__last_call

    def debug(self):
        """
        Lets inspect request and response data.

        Returns:

        Dictionary with request and response keys.

        """
        return {
            'request': self.get_request(as_dict=True),
            'response': self.get_response(as_dict=True),
        }

    def get_product(self, ids, arrayify=False):
        """
        Access products resource.

        Args:

        ``ids``: String o Array of Strings that represents SKU of a product.
        ``arrayify``: Boolean thats indicate if a single product should be returned in a List.

        Returns:

        Product as object if SKU exists otherwise None.

        https://documentation.demandware.com/display/DOC131/Product+resource#Productresource-Getsingleproduct

        """
        if isinstance(ids, (list, tuple)):
            ids = '(%s)' % ''.join(str('%s,' % e) for e in ids)

        self._call('products/%s' % ids)

        if self.__last_call.response.info.code == httplib.OK:
            if hasattr(self.__last_call.response.body, 'data'):
                return [Object(o) for o in self.__last_call.response.body.data]
            elif arrayify:
                return [self.__last_call.response.body]
            else:
                return self.__last_call.response.body

    def search_product(self, query):
        """
        Provides keyword and refinement search functionality for products.

        Args:

        ``query``: String, the query phrase to search for.

        Returns:

        Search results as object, if an error occur then None.

        https://documentation.demandware.com/display/DOC131/ProductSearch+resource#ProductSearchresource-SearchProducts

        """
        self.set_get('q', query)
        self._call('product_search')

        if self.__last_call.response.info.code == httplib.OK:
            return self.__last_call.response.body

    def search_category(self, category='root', levels=2):
        """
        Get online categories.

        Args:

        ``category``: String, category Id.

        ``levels``: Integer, Specifies how many levels of nested sub-categories you want the server to return. The default
        value is 1.

        Returns:

        Categories as object, if an error occur then None.

        https://documentation.demandware.com/display/DOC131/Category+resource#Categoryresource-Getcategory

        """
        self.set_get('levels', levels)
        self._call('categories/%s' % category)

        if self.__last_call.response.info.code == httplib.OK:
            return self.__last_call.response.body

    def get_user(self):
        """
        Get current customer data.

        Returns:

        Returns the account profile object, if an error occur then None.

        https://documentation.demandware.com/display/DOC131/Account+resource#Accountresource-Getaccountprofile

        """
        self.__secure = True
        self._call('account/this')

        if self.__last_call.response.info.code == httplib.OK:
            return self.__last_call.response.body

    def login(self, username, password):
        """
        Action to login a customer.

        Args:

        ``username``: String, customer username.
        ``password:``: String, customer password.

        Returns:

        If success then returns True otherwise False.

        https://documentation.demandware.com/display/DOC131/Account+resource#Accountresource-Loginaction

        """
        self.__secure = True
        self.__method = 'POST'

        self.set_header('Content-Type', 'application/json')
        self.set_post('username', str(username))
        self.set_post('password', str(password))
        self._call('account/login')

        if self.__last_call.response.info.code == httplib.NO_CONTENT:
            return True
        return False

    def logout(self):
        """
        Action to logout a customer.

        Returns:

        If success then returns True otherwise False.

        https://documentation.demandware.com/display/DOC131/Account+resource#Accountresource-Logoutaction

        """
        self.__secure = True
        self.__method = 'POST'

        self.set_header('Content-Type', 'application/json')
        self._call('account/logout')

        if self.__last_call.response.info.code == httplib.NO_CONTENT:
            return True
        return False

    def get_basket(self):
        """
        Returns a limited set of basket information. Limited means that no checkout related information
        (i.e. addresses, shipping and payment method) are returned.

        Returns:

        If success then Basket as object otherwise None.

        https://documentation.demandware.com/display/DOC131/Basket+resource#Basketresource-Getbasket

        """
        self._call('basket/this')

        if self.__last_call.response.info.code == httplib.OK:
            return self.__last_call.response.body
