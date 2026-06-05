from unittest.mock import MagicMock

from helius.models.token import (
    TokenAccountModel,
    TokenAmountModel,
    TokenLargestAccountModel,
)


def _amount():
    return {"amount": "1000", "decimals": 6, "uiAmount": 0.001, "uiAmountString": "0.001"}


def test_get_token_account_balance(client):
    client._makeRequest = MagicMock(return_value={"result": {"value": _amount()}})
    res = client.token.getTokenAccountBalance("PUB")
    assert isinstance(res, TokenAmountModel) and res.amount == "1000"
    client._makeRequest.assert_called_once_with("getTokenAccountBalance", ["PUB"])


def test_get_token_accounts_by_owner(client):
    account = {
        "account": {
            "lamports": 1,
            "owner": "O",
            "data": {"parsed": {}},
            "executable": False,
            "rentEpoch": 0,
            "space": 165,
        },
        "pubkey": "P",
    }
    client._makeRequest = MagicMock(return_value={"result": {"value": [account]}})
    res = client.token.getTokenAccountsByOwner("OWN", "MINT")
    assert isinstance(res[0], TokenAccountModel) and res[0].pubkey == "P"
    client._makeRequest.assert_called_once_with(
        "getTokenAccountsByOwner",
        ["OWN", {"mint": "MINT"}, {"encoding": "jsonParsed"}],
    )


def test_get_token_accounts_by_delegate(client):
    account = {
        "account": {
            "lamports": 1,
            "owner": "O",
            "data": {},
            "executable": False,
            "rentEpoch": 0,
            "space": None,
        },
        "pubkey": "P",
    }
    client._makeRequest = MagicMock(return_value={"result": {"value": [account]}})
    res = client.token.getTokenAccountsByDelegate("DEL", "MINT")
    assert isinstance(res[0], TokenAccountModel)
    client._makeRequest.assert_called_once_with(
        "getTokenAccountsByDelegate",
        ["DEL", {"mint": "MINT"}, {"encoding": "jsonParsed"}],
    )


def test_get_token_largest_accounts(client):
    client._makeRequest = MagicMock(
        return_value={
            "result": {
                "value": [
                    {
                        "address": "A",
                        "amount": "500",
                        "decimals": 6,
                        "uiAmount": 0.0005,
                        "uiAmountString": "0.0005",
                    }
                ]
            }
        }
    )
    res = client.token.getTokenLargestAccounts("MINT")
    assert isinstance(res[0], TokenLargestAccountModel) and res[0].address == "A"
    client._makeRequest.assert_called_once_with("getTokenLargestAccounts", ["MINT"])


def test_get_token_supply(client):
    client._makeRequest = MagicMock(return_value={"result": {"value": _amount()}})
    res = client.token.getTokenSupply("MINT")
    assert isinstance(res, TokenAmountModel) and res.decimals == 6
    client._makeRequest.assert_called_once_with("getTokenSupply", ["MINT"])
