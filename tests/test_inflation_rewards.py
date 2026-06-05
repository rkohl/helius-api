from unittest.mock import MagicMock

from helius.models.inflationRewards import (
    InflationGovernorModel,
    InflationRateModel,
    InflationRewardModel,
)


def test_get_inflation_governor(client):
    client._makeRequest = MagicMock(
        return_value={
            "result": {
                "initial": 0.15,
                "terminal": 0.015,
                "taper": 0.15,
                "foundation": 0.05,
                "foundationTerm": 7.0,
            }
        }
    )
    res = client.inflationRewards.getInflationGovernor()
    assert isinstance(res, InflationGovernorModel) and res.initial == 0.15
    client._makeRequest.assert_called_once_with("getInflationGovernor", [])


def test_get_inflation_rate(client):
    client._makeRequest = MagicMock(
        return_value={
            "result": {"total": 0.08, "validator": 0.07, "foundation": 0.01, "epoch": 5}
        }
    )
    res = client.inflationRewards.getInflationRate()
    assert isinstance(res, InflationRateModel) and res.epoch == 5
    client._makeRequest.assert_called_once_with("getInflationRate", [])


def test_get_inflation_reward(client):
    client._makeRequest = MagicMock(
        return_value={
            "result": [
                {
                    "epoch": 5,
                    "effectiveSlot": 100,
                    "amount": 2500,
                    "postBalance": 10000,
                    "commission": 5,
                },
                None,
            ]
        }
    )
    res = client.inflationRewards.getInflationReward(["A1", "A2"])
    assert isinstance(res[0], InflationRewardModel) and res[0].amount == 2500
    assert res[1] is None
    client._makeRequest.assert_called_once_with("getInflationReward", [["A1", "A2"]])


def test_get_inflation_reward_with_epoch(client):
    client._makeRequest = MagicMock(return_value={"result": [None]})
    client.inflationRewards.getInflationReward(["A1"], epoch=7)
    client._makeRequest.assert_called_once_with(
        "getInflationReward", [["A1"], {"epoch": 7}]
    )
