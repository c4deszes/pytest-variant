#pylint: disable = missing-function-docstring
"""
Tests variant filtering mechanisms
"""
import pytest

@pytest.mark.integration
def test_filter_dict(testdir):
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

        def test_feature_common(variant):
            pass

        @pytest.mark.variant({'os': 'win32'})
        def test_feature_win32():
            pass

        @pytest.mark.variant({'os': 'win32', 'arch': 'x64'})
        def test_feature_win32_x64():
            pass

        @pytest.mark.variant({'os': 'win32', 'arch': ['x86', 'x64']})
        def test_feature_win32_x86():
            pass
        """
    )
    result = testdir.runpytest_subprocess()
    result.assert_outcomes(passed=3, failed=0)

@pytest.mark.integration
def test_filter_expr(testdir):
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

        def test_feature_common(variant):
            pass

        @pytest.mark.variant("os == 'win32'")
        def test_feature_win32():
            pass

        @pytest.mark.variant("os == 'win32' and arch == 'x64'")
        def test_feature_win32_x64():
            pass

        @pytest.mark.variant("os == 'win32' and arch == 'x86'")
        def test_feature_win32_x86():
            pass
        """
    )
    result = testdir.runpytest_subprocess()
    result.assert_outcomes(passed=3, failed=0)
