import pytest

from helius import Helius


@pytest.fixture
def client():
    return Helius(apiKey="test-key")
