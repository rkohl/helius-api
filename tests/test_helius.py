from unittest.mock import MagicMock, patch

import pytest
import requests

from helius import Helius
from helius.accounts import Accounts
from helius.block import Block
from helius.epoch import Epoch
from helius.inflationRewards import InflationRewards
from helius.slot import Slot
from helius.systemInfo import SystemInfo
from helius.token import Token
from helius.transactions import Transactions


def test_url_default():
    assert Helius(apiKey="abc").url == "https://mainnet.helius-rpc.com/?api-key=abc"


def test_url_custom_base():
    assert Helius(apiKey="abc", url="https://example.com").url == "https://example.com/?api-key=abc"


def test_default_id():
    assert Helius(apiKey="k")._id == 1


def test_custom_id():
    assert Helius(apiKey="k", id=42)._id == 42


@pytest.mark.parametrize(
    "attr, cls",
    [
        ("accounts", Accounts),
        ("block", Block),
        ("epoch", Epoch),
        ("inflationRewards", InflationRewards),
        ("slot", Slot),
        ("systemInfo", SystemInfo),
        ("token", Token),
        ("transactions", Transactions),
    ],
)
def test_subclient_properties(client, attr, cls):
    assert isinstance(getattr(client, attr), cls)


def test_make_request_success(client):
    with patch("requests.post") as mock_post:
        resp = MagicMock()
        resp.json.return_value = {"result": 123}
        mock_post.return_value = resp
        data = client._makeRequest("getSlot", [])
    assert data == {"result": 123}
    _, kwargs = mock_post.call_args
    assert kwargs["json"]["method"] == "getSlot"
    assert kwargs["json"]["params"] == []


def test_make_request_request_exception_returns_none(client):
    with patch(
        "requests.post",
        side_effect=requests.exceptions.RequestException("boom"),
    ):
        assert client._makeRequest("getSlot", []) is None


def test_make_request_rpc_error_returns_none(client):
    with patch("requests.post") as mock_post:
        resp = MagicMock()
        resp.json.return_value = {"error": {"code": -32000, "message": "bad"}}
        mock_post.return_value = resp
        assert client._makeRequest("getSlot", []) is None
