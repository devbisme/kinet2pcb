# -*- coding: utf-8 -*-

"""Tests for `kinet2pcb` package."""

import pytest

from kinet2pcb import *

def test_1():
    """Just test to see if a netlist can be processed without an error."""
    kinet2pcb("kinet2pcb_test/kinet2pcb_test.net", "test_1.brd")
