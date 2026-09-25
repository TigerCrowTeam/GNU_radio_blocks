#
# Copyright 2008,2009 Free Software Foundation, Inc.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# The presence of this file turns this directory into a Python package

'''
This is the GNU Radio SIK_RADIOS module. Place your Python package
description here (python/__init__.py).
'''
import os

# import pybind11 generated symbols into the Sik_Radios namespace
try:
    # this might fail if the module is python-only
    from .Sik_Radios_python import *
except ModuleNotFoundError:
    pass
from .Framer import Framer
from .SyncInserter import SyncInserter
from .UniversalWhitener import UniversalWhitener

# import any pure python here
#
