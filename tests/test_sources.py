#pylint: disable = missing-function-docstring
"""
Tests whether data sources are correctly loaded
"""
import os
import pytest

@pytest.mark.integration
def test_sources_configure_none(testdir):
    testdir.makepyfile(
        """
        import pytest

        def test_something():
            pass
        """
    )
    result = testdir.runpytest_subprocess()
    result.assert_outcomes(passed=1, failed=0)

@pytest.mark.integration
def test_sources_configure_hook(testdir):
    testdir.makeconftest(
        """
        # Local variant setting
        def pytest_configure(config):
            config.variant = {'os': 'win32', 'arch': 'x86'}
        """
    )
    testdir.makepyfile(
        """
        import pytest

        def test_something(variant):
            assert variant['os'] == 'win32'
            assert variant['arch'] == 'x86'
        """
    )
    result = testdir.runpytest_subprocess()
    result.assert_outcomes(passed=1, failed=0)

@pytest.mark.integration
def test_sources_ini(testdir):
    ini_file = testdir.makefile('.ini',
        "[variant]",
        "os = win32",
        "arch = x86"
    )
    testdir.makepyfile(
        """
        import pytest

        def test_something(variant):
            assert variant['os'] == 'win32'
            assert variant['arch'] == 'x86'
        """
    )
    result = testdir.runpytest_subprocess('--variant', f"INI:{ini_file}")
    result.assert_outcomes(passed=1, failed=0)

@pytest.mark.integration
def test_sources_json(testdir):
    json_file = testdir.makefile('.json',
        '{',
        '"os": "win32",',
        '"arch": "x86"',
        '}'
    )
    testdir.makepyfile(
        """
        import pytest

        def test_something(variant):
            assert variant['os'] == 'win32'
            assert variant['arch'] == 'x86'
        """
    )
    result = testdir.runpytest_subprocess('-s', '--variant', f"JSON:{json_file}")
    result.assert_outcomes(passed=1, failed=0)

@pytest.mark.integration
def test_source_env(testdir):
    testdir.makepyfile(
        """
        import pytest

        def test_something(variant):
            assert variant['OS'] == 'win32'
            assert variant['ARCH'] == 'x86'
        """
    )
    os.environ['VARIANT_OS'] = 'win32'
    os.environ['VARIANT_ARCH'] = 'x86'
    result = testdir.runpytest_subprocess('-s', '--variant', 'ENV:VARIANT_')
    result.assert_outcomes(passed=1, failed=0)
