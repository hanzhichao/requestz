import pytest

from requestz import session


@pytest.fixture
def s():
    return session()