from unittest.mock import MagicMock

from helius.models.transactions import (
    SignatureInfoModel,
    SignatureStatusModel,
    SimulateTransactionModel,
    TransactionModel,
    TransactionsForAddressModel,
    TransfersByAddressModel,
)


def test_get_transaction(client):
    client._makeRequest = MagicMock(
        return_value={
            "result": {
                "slot": 100,
                "blockTime": 123,
                "transaction": {"x": 1},
                "meta": {"y": 2},
                "version": 0,
            }
        }
    )
    res = client.transactions.getTransaction("SIG")
    assert isinstance(res, TransactionModel) and res.slot == 100
    client._makeRequest.assert_called_once_with(
        "getTransaction", ["SIG", {"maxSupportedTransactionVersion": 0}]
    )


def test_get_transaction_count(client):
    client._makeRequest = MagicMock(return_value={"result": 999})
    assert client.transactions.getTransactionCount() == 999
    client._makeRequest.assert_called_once_with("getTransactionCount", [])


def test_get_signatures_for_address(client):
    client._makeRequest = MagicMock(
        return_value={
            "result": [
                {
                    "signature": "S",
                    "slot": 1,
                    "err": None,
                    "memo": None,
                    "blockTime": None,
                    "confirmationStatus": "finalized",
                }
            ]
        }
    )
    res = client.transactions.getSignaturesForAddress("ADDR")
    assert isinstance(res[0], SignatureInfoModel) and res[0].signature == "S"
    client._makeRequest.assert_called_once_with(
        "getSignaturesForAddress", ["ADDR", {"limit": 1000}]
    )


def test_get_transactions_for_address(client):
    client._makeRequest = MagicMock(
        return_value={"result": {"data": [{"a": 1}], "paginationToken": "tok"}}
    )
    res = client.transactions.getTransactionsForAddress("ADDR", paginationToken="prev")
    assert isinstance(res, TransactionsForAddressModel) and res.paginationToken == "tok"
    client._makeRequest.assert_called_once_with(
        "getTransactionsForAddress",
        ["ADDR", {"transactionDetails": "signatures", "limit": 1000, "paginationToken": "prev"}],
    )


def test_get_transactions_for_address_no_token(client):
    client._makeRequest = MagicMock(
        return_value={"result": {"data": [], "paginationToken": None}}
    )
    client.transactions.getTransactionsForAddress("ADDR")
    client._makeRequest.assert_called_once_with(
        "getTransactionsForAddress",
        ["ADDR", {"transactionDetails": "signatures", "limit": 1000}],
    )


def test_get_transfers_by_address(client):
    transfer = {
        "signature": "S",
        "slot": 1,
        "blockTime": None,
        "type": "TRANSFER",
        "fromUserAccount": "F",
        "toUserAccount": "T",
        "fromTokenAccount": None,
        "toTokenAccount": None,
        "mint": None,
        "amount": "10",
        "decimals": 9,
        "uiAmount": None,
        "confirmationStatus": None,
        "transactionIdx": None,
        "instructionIdx": None,
        "innerInstructionIdx": None,
    }
    client._makeRequest = MagicMock(
        return_value={"result": {"data": [transfer], "paginationToken": None}}
    )
    res = client.transactions.getTransfersByAddress("ADDR", mint="MINT")
    assert isinstance(res, TransfersByAddressModel) and res.data[0].amount == "10"
    client._makeRequest.assert_called_once_with(
        "getTransfersByAddress", ["ADDR", {"limit": 1000, "mint": "MINT"}]
    )


def test_get_signature_statuses(client):
    client._makeRequest = MagicMock(
        return_value={
            "result": {
                "value": [
                    {
                        "slot": 1,
                        "confirmations": 10,
                        "err": None,
                        "confirmationStatus": "confirmed",
                    },
                    None,
                ]
            }
        }
    )
    res = client.transactions.getSignatureStatuses(["S1", "S2"])
    assert isinstance(res[0], SignatureStatusModel) and res[1] is None
    client._makeRequest.assert_called_once_with(
        "getSignatureStatuses", [["S1", "S2"], {"searchTransactionHistory": False}]
    )


def test_get_fee_for_message(client):
    client._makeRequest = MagicMock(return_value={"result": {"value": 5000}})
    assert client.transactions.getFeeForMessage("MSG") == 5000
    client._makeRequest.assert_called_once_with("getFeeForMessage", ["MSG"])


def test_send_transaction(client):
    client._makeRequest = MagicMock(return_value={"result": "SIGNATURE"})
    assert client.transactions.sendTransaction("TX") == "SIGNATURE"
    client._makeRequest.assert_called_once_with("sendTransaction", ["TX"])


def test_simulate_transaction(client):
    client._makeRequest = MagicMock(
        return_value={
            "result": {
                "value": {
                    "err": None,
                    "logs": ["log1"],
                    "accounts": None,
                    "unitsConsumed": 1000,
                    "returnData": None,
                }
            }
        }
    )
    res = client.transactions.simulateTransaction("TX")
    assert isinstance(res, SimulateTransactionModel) and res.unitsConsumed == 1000
    client._makeRequest.assert_called_once_with("simulateTransaction", ["TX"])


def test_request_airdrop(client):
    client._makeRequest = MagicMock(return_value={"result": "AIRDROP_SIG"})
    assert client.transactions.requestAirdrop("PUB", 1000000000) == "AIRDROP_SIG"
    client._makeRequest.assert_called_once_with("requestAirdrop", ["PUB", 1000000000])
