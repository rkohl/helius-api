from unittest.mock import MagicMock

from helius.models.epoch import EpochInfoModel, EpochScheduleModel


def test_get_epoch_info(client):
    client._makeRequest = MagicMock(
        return_value={
            "result": {
                "absoluteSlot": 100,
                "blockHeight": 90,
                "epoch": 5,
                "slotIndex": 10,
                "slotsInEpoch": 432000,
                "transactionCount": 12345,
            }
        }
    )
    res = client.epoch.getEpochInfo()
    assert isinstance(res, EpochInfoModel) and res.epoch == 5
    client._makeRequest.assert_called_once_with("getEpochInfo", [])


def test_get_epoch_schedule(client):
    client._makeRequest = MagicMock(
        return_value={
            "result": {
                "slotsPerEpoch": 432000,
                "leaderScheduleSlotOffset": 432000,
                "warmup": False,
                "firstNormalEpoch": 0,
                "firstNormalSlot": 0,
            }
        }
    )
    res = client.epoch.getEpochSchedule()
    assert isinstance(res, EpochScheduleModel) and res.slotsPerEpoch == 432000
    client._makeRequest.assert_called_once_with("getEpochSchedule", [])


def test_get_leader_schedule(client):
    client._makeRequest = MagicMock(return_value={"result": {"validator1": [0, 1, 2]}})
    assert client.epoch.getLeaderSchedule() == {"validator1": [0, 1, 2]}
    client._makeRequest.assert_called_once_with("getLeaderSchedule", [])


def test_get_leader_schedule_with_slot(client):
    client._makeRequest = MagicMock(return_value={"result": {"v": [0]}})
    client.epoch.getLeaderSchedule(123)
    client._makeRequest.assert_called_once_with("getLeaderSchedule", [123])
