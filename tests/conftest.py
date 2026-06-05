import pytest

from helius import Helius

# Create a fixture for the Helius client
@pytest.fixture
def client():
    return Helius(apiKey="test-key")
