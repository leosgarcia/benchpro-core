import re

import benchpro_core
from benchpro_core.version import __version__


def test_package_imports():
    assert benchpro_core.__version__ == __version__


def test_version_is_valid_semver():
    assert re.fullmatch(r"\d+\.\d+\.\d+", __version__)


def test_initial_version_is_pre_alpha():
    assert __version__ == "0.1.0"

