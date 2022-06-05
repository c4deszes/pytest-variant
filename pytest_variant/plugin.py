"""
Pytest variant plugin
"""
from typing import Dict, List
import os
import logging
import warnings
import configparser
import json
import pytest

logger = logging.getLogger('pytest-variant')

INI_PREFIX = 'INI:'
JSON_PREFIX = 'JSON:'
ENV_PREFIX = 'ENV:'

@pytest.fixture(scope="session")
def variant(request):
    """
    Returns the currently active variant settings
    """
    if not getattr(request.config, 'variant', None):
        return {}
    return request.config.variant

def pytest_addoption(parser):
    """
    Adds variant command line option
    """
    group = parser.getgroup('variant')

    group.addoption(
        "--variant",
        action="store",
        dest="variant",
        metavar="SOURCE",
        help="Selects a variant source"
    )

def pytest_configure(config):
    """
    Registers variant as a marker in Pytest and loads variant settings when supplied
    """
    config.addinivalue_line("markers", "variant: for filtering tests based on variants")

    variant_source = config.getoption('variant')

    if variant_source is None:
        pass
    elif variant_source.startswith(INI_PREFIX):
        config.variant = variant_load_ini(strip_prefix(variant_source, INI_PREFIX))
    elif variant_source.startswith(JSON_PREFIX):
        config.variant = variant_load_json(strip_prefix(variant_source, JSON_PREFIX))
    elif variant_source.startswith(ENV_PREFIX):
        config.variant = variant_load_env(strip_prefix(variant_source, ENV_PREFIX))

def pytest_collection_modifyitems(session, config, items):
    #pylint: disable = unused-argument
    """
    Filters test cases based on variant marker
    """
    deselected = []

    for item in items.copy():
        variant_marker = item.get_closest_marker('variant')

        if variant_marker and config.variant is None:
            warnings.warn(f"Variant source is missing, '{item.nodeid}' will be deselected.")
            deselected.append(item)
            items.remove(item)
        elif variant_marker and not variant_marker_eval(config.variant, item, variant_marker):
            deselected.append(item)
            items.remove(item)

    config.hook.pytest_deselected(items = deselected)

def variant_marker_eval(config, item, marker):
    """
    Evaluates whether an item should be selected based on the marker on the test case
    """
    if len(marker.args) != 1:
        warnings.warn(f"Variant filter incorrectly supplied, '{item.nodeid}' will be deselected!")
        return False
    arg = marker.args[0]

    if isinstance(arg, str):
        return variant_marker_eval_expr(config, item, arg)

    if isinstance(arg, Dict):
        return variant_marker_eval_dict(config, item, arg)

    warnings.warn(f"Variant filter type is not supported, '{item.nodeid}' will be deselected!")
    return False

def variant_marker_eval_dict(config, item, val):
    """
    Evaluates whether the dictionary matches the current variant
    """
    for prop in val.items():
        if prop[0] in config and not variant_marker_eval_dict_value(prop[1], config[prop[0]]):
            return False
        if prop[0] not in config:
            warnings.warn(f"Variant attribute '{prop[0]}' used on '{item.nodeid}' is not defined!")
            return False
    return True

def variant_marker_eval_dict_value(value, selection):
    """
    Evaluates whether a dictionary's value matches a variant attribute

    Returns:
        `True` if the value matches the variant exactly, or if the value is
        a `List` and has an item that matches
        `False` otherwise
    """
    if isinstance(value, List):
        for item in value:
            if item == selection:
                return True
    elif value == selection:
        return True
    return False

def variant_marker_eval_expr(config, item, expr):
    #pylint: disable = broad-except
    """
    Evaluates whether the expression matches the current variant
    """
    try:
        #pylint: disable = eval-used
        return eval(expr, config)
    except Exception:
        warnings.warn(f"Failed to evaluate variant expression '{expr}' used on '{item.nodeid}'!")
        return False

def variant_load_json(filepath):
    """
    Loads a JSON file as variant configuration
    """
    with open(filepath, 'r') as content:
        return json.load(content)

def variant_load_ini(filepath):
    """
    Loads an INI file as variant configuration
    """
    parser = configparser.ConfigParser()
    parser.read(filepath)

    return dict(parser.items('variant'))

def variant_load_env(prefix):
    """
    Loads environment variables as variant configuration
    """
    env = {}
    for var in os.environ.items():
        if var[0].startswith(prefix):
            env[strip_prefix(var[0], prefix)] = var[1]
    return env

def strip_prefix(text, prefix):
    """
    Returns a string without the prefix, only if it starts with the given prefix
    otherwise it returns the original string

    Introduced as `removeprefix` in Python 3.9
    """
    if text.startswith(prefix):
        return text[len(prefix):]
    return text
