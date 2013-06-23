#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from dw.objects import Object

###############################################################
# ObjectTest
###############################################################
class ObjectTest(TestCase):
    """Unit Test for Object class."""
    list_attrs = list((
        {'foo': 'bar',},
    ))

    tuple_attrs = tuple((
        {'foo': 'bar',},
    ))

    dict_attrs = dict({
        'foo': 'bar',
    })

    mixed_attrs = {
        'foo': 'bar',
        'get_list': list_attrs,
        'get_tuple': tuple_attrs,
        'get_dict': dict_attrs,
    }

    def test_list(self):
        """Creates an object from list."""
        o = Object(self.list_attrs)

        # Check attributes
        self.assertTrue(isinstance(o, Object))
        self.assertEqual(hasattr(o['0'], 'foo'), True)

    def test_tuple(self):
        """Creates an object from tuple."""
        o = Object(self.tuple_attrs)

        # Check attributes
        self.assertTrue(isinstance(o, Object))
        self.assertEqual(hasattr(o['0'], 'foo'), True)

    def test_dict(self):
        """Creates an object from dictionary."""
        o = Object(self.dict_attrs)

        # Check attributes
        self.assertTrue(isinstance(o, Object))
        self.assertEqual(hasattr(o, 'foo'), True)

    def test_mixed(self):
        """Creates an object from a dictionary mixed with lists, dicts. and tuples."""
        o = Object(self.mixed_attrs)

        # Check attributes
        self.assertTrue(isinstance(o, Object))
        self.assertEqual(hasattr(o, 'foo'), True)

        self.assertEqual(hasattr(o, 'get_list'), True)
        self.assertEqual(hasattr(o, 'get_tuple'), True)
        self.assertEqual(hasattr(o, 'get_dict'), True)

        self.assertEqual(o.get_list[0].has_key('foo'), True)
        self.assertEqual(o.get_tuple[0].has_key('foo'), True)
        self.assertEqual(hasattr(o.get_dict, 'foo'), True)
