# Pytest Variant

[![PyPI version](https://badge.fury.io/py/pytest-variant.svg)](https://pypi.org/project/pytest-variant/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-variant.svg)](https://pypi.org/project/pytest-variant/)
![GitHub last commit](https://img.shields.io/github/last-commit/c4deszes/pytest-variant)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

> pytest-variant is a plugin for pytest that allows handling variants in test cases.

## Installation

You can install this library from PyPI using pip.

`pip install pytest-variant`

## Usage

### Define variant attributes

Parameters can be loaded from INI files from the `variant` section. To load from INI file use
`pytest --variant INI:config.ini`.

An example of such `.ini` file.

```ini
[variant]
os = win32
arch = x86
```

---

Parameters can also be loaded from JSON files, they are loaded as a dictionary using `json.load`.
To load from JSON file use `pytest --variant JSON:config.json`.

An example of a `.json` file.

```json
{
    "os": "win32",
    "arch": "x86"
}
```

---

Variants can also be inferred from environment variables using `pytest --variant ENV:<prefix>`.
When the prefix is empty all environment variables will be loaded, otherwise it will only load the
variables that start with the prefix and the attribute names will have the prefix stripped.

For example `pytest --variant ENV:VARIANT_` in a context where `VARIANT_OS=win32` and
`VARIANT_ARCH=x86` exist then the loaded variant will be:

```json
{
    "OS": "win32",
    "ARCH": "x86"
}
```

Note that on Windows systems environment variable names are case insensitive and they always have to
be referred to using capital letters.

---

Lastly the internal variant variable can be overwritten and therefore it's possible to implement
custom configuration and loading mechanisms. This can be done by using a custom
[pytest hook](https://docs.pytest.org/en/6.2.x/_modules/_pytest/hookspec.html#pytest_configure).

```python
def pytest_configure(config):
    config.variant = {
        'os': 'win32',
        'arch': 'x86'
    }
```

### Accessing variant attributes

The plugin automatically registers a fixture called `variant`, which is a dictionary containing the
attributes that were loaded. You can use these to make a test behave a certain way given a variant
or you could conditionally skip the test case.

```python
def test_case1(variant):
    if variant['os'] == 'win32':
        # windows specific behavior
        pass
    else:
        pass
```

### Marking tests

There are two styles of marking tests for variant selection.

When a dictionary is passed as the marker's argument the value of each key must match the currently
active variant's. Missing keys are ignored, you can think of each supplied key as an `and`
operation, and providing a list as a key as an `or` operation.

```python
def pytest_configure(config):
    config.variant = {
        'os': 'win32',
        'arch': 'x86'
    }

# Will be selected
@pytest.mark.variant({'os': 'win32'})
def test_case1():
    pass

# Will be deselected
@pytest.mark.variant({'os': 'ubuntu'})
def test_case2():
    pass

# Will be selected
@pytest.mark.variant({'os': 'win32', 'arch': 'x86'})
def test_case3():
    pass

# Will be deselected
@pytest.mark.variant({'os': 'win32', 'arch': 'x64'})
def test_case4():
    pass

# Will be selected
@pytest.mark.variant({'os': 'win32', 'arch': ['x86', 'x64']})
def test_case5():
    pass
```

When a string is passed it's assumed to be a Python expression, which when evaluates to `True`
indicates that the test should be selected. In the context of the expression all attributes are
available.

```python
def pytest_configure(config):
    config.variant = {
        'os': 'win32',
        'arch': 'x86'
    }

# Will be selected
@pytest.mark.variant("os == 'win32'")
def test_case1():
    pass

# Will be deselected
@pytest.mark.variant("os == 'win32' and arch == 'x64'")
def test_case2():
    pass
```

## Why not just use custom marks or skips?

Pytest marks allow you to filter the tests based on the active marks, this is good when you have a
few test sets and you can control what marks are being used. For example you have tests specific to
Windows, you could use `@pytest.mark.win32` but this is hard to scale up, if you want to use integer
types as variant attributes then it becomes awkward to use.

The `skipif` mark can be a decent option however when used with a reporting tool like Jenkins they
will show up as skipped tests and looking at the report it won't be evident that a test shouldn't be
performed at all for the specific variant.

Truly the only difference between custom marks and this plugin is that pytest marks are in a list,
while variant attributes are in a dictionary.

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
