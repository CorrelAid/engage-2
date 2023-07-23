import pytest
from settings import settings

database_test = pytest.mark.skipif(
    not settings.tests.test_database, reason="Database tests disabled"
)
