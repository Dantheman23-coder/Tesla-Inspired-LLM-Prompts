"""Compatibility shim for the relocated advanced feature tests.

PyPI mirrors and forks previously referenced ``test_advanced_features.py`` at
repository root. The actual tests now live in ``tests/test_advanced_features.py``
so we re-export them here to keep the old entry point functional without
duplicating assertions.
"""

from tests.test_advanced_features import *  # noqa: F401,F403
