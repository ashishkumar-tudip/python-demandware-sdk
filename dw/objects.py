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

###############################################################
# Generic Object
###############################################################
class Object(object):
    """Class to represent OCAPI resources."""
    def __init__(self, params=dict()):
        """
        Convert dictionary to generic object, also can receives
        lists, tuples as argument.

        Examples:

        o = Object(list((
            {'foo': 'bar',},
        )))

        o['0'].foo

        o = Object(tuple((
            {'foo': 'bar',},
        )))

        o['0'].foo

        o = Object(dict({
            'foo': 'bar',
        }))

        o.foo

        Args:

        ``params``: Iterable to be mapped.

        """
        if isinstance(params, (list, tuple)):
            # Creates a dictionary named with values staring from 0...N
            # e.g my_object.['0']
            params = dict(enumerate(params))

        if isinstance(params, dict):
            # If a dictionary if found set key as attribute
            for key, value in params.iteritems():
                key = str(key)
                if isinstance(value, dict):
                    setattr(self, key, Object(value))
                else:
                    setattr(self, key, value)

    def __getitem__(self, value):
        """
        Returns value for attribute requested, if attribute
        requested does not exits then None value is returned.

        """
        return self.__dict__[value]
