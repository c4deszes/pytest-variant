#pylint: disable = redefined-outer-name, missing-function-docstring
"""
Tests helper functions
"""
import pytest
from pytest_variant.plugin import (
    variant_marker_eval_dict, variant_marker_eval_expr
)

@pytest.fixture(scope="module")
def variant():
    return {
        "os": "win32",
        "arch": "x64"
    }

class Item():
    #pylint: disable = missing-class-docstring, too-few-public-methods
    def __init__(self):
        self.nodeid = 'test'

@pytest.fixture()
def dummy_item():
    return Item()

@pytest.mark.unit
def test_helpers_marker_dict_partial_match(variant, dummy_item):
    marker = {
        "os": "win32"
    }
    assert variant_marker_eval_dict(variant, dummy_item, marker) is True

@pytest.mark.unit
def test_helpers_marker_dict_mismatch(variant, dummy_item):
    marker = {
        "os": "linux"
    }
    assert variant_marker_eval_dict(variant, dummy_item, marker) is False

@pytest.mark.unit
def test_helpers_marker_dict_full_match(variant, dummy_item):
    marker = {
        "os": "win32",
        "arch": "x64"
    }
    assert variant_marker_eval_dict(variant, dummy_item, marker) is True

@pytest.mark.unit
def test_helpers_marker_dict_unknown_property(variant, dummy_item):
    marker = {
        "os": "win32",
        "arch": "x64",
        "build": "release"
    }
    assert variant_marker_eval_dict(variant, dummy_item, marker) is False

@pytest.mark.unit
@pytest.mark.parametrize(
    ('expr', 'result'),
    [
        ("os == 'win32'", True),
        ("os == 'win32' and arch == 'x64'", True),
        ("os == 'win32' and arch == 'x86'", False),
        ("os == 'linux'", False)
    ]
)
def test_helper_marker_expr_match(variant, dummy_item, expr, result):
    assert variant_marker_eval_expr(variant, dummy_item, expr) is result
