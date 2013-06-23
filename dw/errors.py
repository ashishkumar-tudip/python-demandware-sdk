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
# Demandware Exceptions
###############################################################
class DemandwareError(Exception):
    """Base Exception for Demandware."""
    pass

class ParameterMissedError(DemandwareError):
    """Raised if an parameter is missed."""
    pass

class ParameterInvalidError(DemandwareError):
    """Raised if an invalid parameter is detected."""
    pass
