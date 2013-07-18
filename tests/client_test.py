#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from unittest import TestCase

from dw.client import Demandware
from dw.objects import Object
from dw.errors import ParameterMissedError, ParameterInvalidError
from pprint import pprint

###############################################################
# DemandwareTest
###############################################################
class DemandwareTest(TestCase):
    """Unit Test for Demandware SDK."""
    def setUp(self):
        defaults = json.loads(open('tests/fixtures/client.json').read())

        self.SETTINGS_OK_VALID = defaults['settings']['ok_valid']
        self.SETTINGS_BAD_MISSED = defaults['settings']['bad_missed']
        self.SETTINGS_BAD_INVALID = defaults['settings']['bad_invalid']

        self.general = defaults['payload']['general']
        self.products = defaults['payload']['products']
        self.search = defaults['payload']['search']
        self.category = defaults['payload']['category']
        self.account = defaults['payload']['account']
        self.register = defaults['payload']['register']

    def test_defaults(self):
        """Verify settings and instance data."""
        conn = Demandware(self.SETTINGS_OK_VALID)

        # Check client
        self.assertTrue(bool(conn))

        # Check default values
        self.assertTrue(isinstance(conn.get_response(True), dict))
        self.assertTrue(isinstance(conn.get_request(True), dict))
        self.assertTrue(isinstance(conn.get_response(), Object))
        self.assertTrue(isinstance(conn.get_request(), Object))
        self.assertTrue(isinstance(conn.debug(), dict))

        self.assertTrue(isinstance(conn.header(), dict))
        self.assertTrue(isinstance(conn.get(), dict))
        self.assertTrue(isinstance(conn.post(), dict))

        conn.set_header(
            self.general[0]['key'],
            self.general[0]['value']
        )
        conn.set_get(
            self.general[1]['key'],
            self.general[1]['value']
        )
        conn.set_post(
            'username',
            self.account[0]['username']
        )

        self.assertEqual(
            conn.header(self.general[0]['key']),
            self.general[0]['value']
        )
        self.assertEqual(
            conn.get(self.general[1]['key']),
            self.general[1]['value']
        )
        self.assertEqual(
            conn.post('username'),
            self.account[0]['username']
        )

    def test_settings_parameter_missed(self):
        """Detect initialization with missed parameters."""
        self.assertRaises(
            ParameterMissedError,
            Demandware,
            self.SETTINGS_BAD_MISSED
        )

    def test_settings_parameter_invalid(self):
        """Detect initialization with invalid parameters."""
        self.assertRaises(
            ParameterInvalidError,
            Demandware,
            self.SETTINGS_BAD_INVALID
        )

    def test_get_product_single(self):
        """Verify requests for single products."""
        conn = Demandware(self.SETTINGS_OK_VALID)
        products = conn.get_product(self.products[0]['id'])

        # Compare response
        self.assertEqual(hasattr(products, 'name'), True)
        # Compare attribute
        self.assertEqual(products.name, self.products[0]['name'])

    def test_get_product_single_as_list(self):
        """Verify requests for single products returned in a list."""
        conn = Demandware(self.SETTINGS_OK_VALID)

        # Returns as list
        products = conn.get_product(self.products[0]['id'], True)

        # Compare response
        self.assertTrue(isinstance(products, list))
        self.assertEqual(len(products), 1)

    def test_get_product_multiple(self):
        """Verify requests for multiple products."""
        conn = Demandware(self.SETTINGS_OK_VALID)
        products = conn.get_product((self.products[0]['id'],))

        # Compare response
        self.assertTrue(isinstance(products, list))
        self.assertEqual(len(products), 1)
        self.assertEqual(hasattr(products[0], 'name'), True)
        # Compare attribute
        self.assertEqual(products[0].name, self.products[0]['name'])

    def test_get_search_products(self):
        """Verify requests that search products."""
        conn = Demandware(self.SETTINGS_OK_VALID)
        search = conn.search_product(self.search[0]['query'])

        # Compare response
        self.assertEqual(hasattr(search, 'hits'), True)
        self.assertTrue(isinstance(search.hits, list))
        self.assertNotEqual(len(search.hits), 0)

    def test_get_search_products_with_count(self):
        """Verify requests that search products, limited to N results."""
        conn = Demandware(self.SETTINGS_OK_VALID)

        # Set count parameter
        conn.set_get('count', self.search[0]['count'])
        search = conn.search_product(self.search[0]['query'])

        # Compare response
        self.assertEqual(hasattr(search, 'hits'), True)
        self.assertTrue(isinstance(search.hits, list))
        self.assertEqual(len(search.hits), 1)

    def test_get_category_single(self):
        """Verify requests that looking for a category."""
        conn = Demandware(self.SETTINGS_OK_VALID)
        category = conn.search_category(self.category[0]['category'], self.category[0]['levels'])

        # Compare response
        self.assertEqual(hasattr(category, 'categories'), True)
        self.assertTrue(isinstance(category.categories, list))
        self.assertNotEqual(len(category.categories), 0)

    def test_loginwith_correct_credentials(self):
        """Verify login that tried to log in with correct credentials."""
        conn = Demandware(self.SETTINGS_OK_VALID)
        crt = conn.login(self.account[0]['username'], self.account[0]['password'])

        # Compare response
        self.assertEqual(crt, True)
        conn.logout()

    def test_login_with_wrong_credentials(self):
        """Verify login that tried to log in with wrong credentials.."""
        conn = Demandware(self.SETTINGS_OK_VALID)
        crt = conn.login(self.account[1]['username'], self.account[1]['password'])

        # Compare response
        self.assertNotEqual(crt, True)
        conn.logout()

    def test_logout(self):
        """Verify logout."""
        conn = Demandware(self.SETTINGS_OK_VALID)

        conn.login(self.account[0]['username'], self.account[0]['password'])
        crt = conn.logout()

        # Compare response
        self.assertEqual(crt, True)

    def test_get_user_logged_with_wrong_credentials(self):
        """Verify customer profile when logged."""
        conn = Demandware(self.SETTINGS_OK_VALID)

        conn.login(self.account[0]['username'], self.account[0]['password'])
        customer = conn.get_user()
        conn.logout()

        # Compare response
        self.assertEqual(hasattr(customer, 'customer_no'), True)

    def test_get_user_logged_with_correct_credentials(self):
        """Verify customer profile that tried to log in with wrong credentials."""
        conn = Demandware(self.SETTINGS_OK_VALID)

        # Check invalid customer
        conn.login(self.account[1]['username'], self.account[1]['password'])
        customer = conn.get_user()
        conn.logout()

        # Compare response
        self.assertNotEqual(hasattr(customer, 'customer_no'), True)

    def test_get_user_anonymous(self):
        """Verify customer profile when not logged."""
        conn = Demandware(self.SETTINGS_OK_VALID)

        # Check customer without login
        customer = conn.get_user()

        # Compare response
        self.assertNotEqual(hasattr(customer, 'customer_no'), True)

    def test_register_correct_user(self):
        """Verify that register an profile correctly."""
        conn = Demandware(self.SETTINGS_OK_VALID)

        # Check valid register
        user = conn.register(self.register[0]['username'], self.register[0]['password'], self.register[0]['profile'])
        conn.logout()

        # Compare response
        self.assertEqual(hasattr(user, 'email'), True)

    def test_register_wrong_user(self):
        """Verify that register an profile correctly."""
        conn = Demandware(self.SETTINGS_OK_VALID)

        # Check valid register
        user = conn.register(self.register[1]['username'], self.register[1]['password'], self.register[1]['profile'])
        conn.logout()

        # Compare response
        self.assertNotEqual(hasattr(user, 'email'), True)

    def test_get_basket(self):
        """Verify requests that gets basket."""
        conn = Demandware(self.SETTINGS_OK_VALID)
        basket = conn.get_basket()

        # Compare response
        self.assertEqual(hasattr(basket, 'product_total'), True)

    def test_get_product_with_expanded_ok(self):
        """Verify requests for single product with expanded options"""
        conn = Demandware(self.SETTINGS_OK_VALID)
        expand = [Demandware.EXPAND_PRICES, Demandware.EXPAND_IMAGES]
        products = conn.get_product(self.products[0]['id'], expand=expand)

        # Compare response
        self.assertEqual(hasattr(products, 'name'), True)
        # Compare attribute
        self.assertEqual(products.name, self.products[0]['name'])
        self.assert_('price' in products.__dict__)
