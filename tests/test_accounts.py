from unittest.mock import MagicMock

from helius.models.accounts import (
    AccountInfoModel,
    LargestAccountsModel,
    ProgramAccountsModel,
)


def _account_value():
    return {
        "lamports": 100,
        "owner": "Own111",
        "data": ["base64data", "base64"],
        "executable": False,
        "rentEpoch": 5,
        "space": 10,
    }


def test_get_account_info(client):
    client._makeRequest = MagicMock(return_value={"result": {"value": _account_value()}})
    res = client.accounts.getInfo("PUB")
    assert isinstance(res, AccountInfoModel)
    assert res.lamports == 100 and res.owner == "Own111"
    client._makeRequest.assert_called_once_with(
        "getAccountInfo", ["PUB", {"commitment": "finalized"}]
    )


def test_get_account_info_none(client):
    client._makeRequest = MagicMock(return_value=None)
    assert client.accounts.getInfo("PUB") is None


def test_get_balance(client):
    client._makeRequest = MagicMock(return_value={"result": {"value": 5000}})
    assert client.accounts.getBalance("PUB") == 5000
    client._makeRequest.assert_called_once_with(
        "getBalance", ["PUB", {"commitment": "finalized"}]
    )


def test_get_program_accounts(client):
    client._makeRequest = MagicMock(
        return_value={"result": [{"account": _account_value(), "pubkey": "P1"}]}
    )
    res = client.accounts.getPrograms("PROG")
    assert len(res) == 1 and isinstance(res[0], ProgramAccountsModel)
    assert res[0].pubkey == "P1"
    client._makeRequest.assert_called_once_with(
        "getProgramAccounts",
        ["PROG", {"commitment": "finalized", "encoding": "base64"}],
    )


def test_get_multiple_accounts(client):
    client._makeRequest = MagicMock(
        return_value={"result": {"value": [_account_value(), None]}}
    )
    res = client.accounts.getMultiple(["P1", "P2"])
    assert res[0].lamports == 100 and res[1] is None
    client._makeRequest.assert_called_once_with(
        "getMultipleAccounts",
        [["P1", "P2"], {"commitment": "finalized", "encoding": "base64"}],
    )


def test_get_minimum_balance_for_rent_exemption(client):
    client._makeRequest = MagicMock(return_value={"result": 890880})
    assert client.accounts.getMinimumRentBalance("PUB") == 890880
    client._makeRequest.assert_called_once_with(
        "getMinimumBalanceForRentExemption", ["PUB", {"commitment": "finalized"}]
    )


def test_get_largest_accounts(client):
    client._makeRequest = MagicMock(
        return_value={"result": {"value": [{"lamports": 9, "address": "A1"}]}}
    )
    res = client.accounts.getLargest()
    assert isinstance(res[0], LargestAccountsModel) and res[0].address == "A1"
    client._makeRequest.assert_called_once_with(
        "getLargestAccounts",
        [{"filter": "circulating"}, {"commitment": "finalized"}],
    )
