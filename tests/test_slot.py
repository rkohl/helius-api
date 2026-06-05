from unittest.mock import MagicMock

from helius.models.slot import HighestSnapshotSlotModel


def test_get_slot(client):
    client._makeRequest = MagicMock(return_value={"result": 12345})
    assert client.slot.getSlot() == 12345
    client._makeRequest.assert_called_once_with("getSlot", [])


def test_get_slot_leader(client):
    client._makeRequest = MagicMock(return_value={"result": "LEADER"})
    assert client.slot.getSlotLeader() == "LEADER"
    client._makeRequest.assert_called_once_with("getSlotLeader", [])


def test_get_slot_leaders(client):
    client._makeRequest = MagicMock(return_value={"result": ["L1", "L2"]})
    assert client.slot.getSlotLeaders(100, 2) == ["L1", "L2"]
    client._makeRequest.assert_called_once_with("getSlotLeaders", [100, 2])


def test_get_minimum_ledger_slot(client):
    client._makeRequest = MagicMock(return_value={"result": 5})
    assert client.slot.getMinimumLedgerSlot() == 5
    client._makeRequest.assert_called_once_with("minimumLedgerSlot", [])


def test_get_max_retransmit_slot(client):
    client._makeRequest = MagicMock(return_value={"result": 9})
    assert client.slot.getMaxRetransmitSlot() == 9
    client._makeRequest.assert_called_once_with("getMaxRetransmitSlot", [])


def test_get_max_shred_insert_slot(client):
    client._makeRequest = MagicMock(return_value={"result": 11})
    assert client.slot.getMaxShredInsertSlot() == 11
    client._makeRequest.assert_called_once_with("getMaxShredInsertSlot", [])


def test_get_highest_snapshot_slot(client):
    client._makeRequest = MagicMock(
        return_value={"result": {"full": 100, "incremental": 110}}
    )
    res = client.slot.getHighestSnapshotSlot()
    assert isinstance(res, HighestSnapshotSlotModel) and res.full == 100
    client._makeRequest.assert_called_once_with("getHighestSnapshotSlot", [])
