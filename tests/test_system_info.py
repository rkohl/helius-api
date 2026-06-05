from unittest.mock import MagicMock

from helius.models.systemInfo import (
    ClusterNodeModel,
    IdentityModel,
    PerformanceSampleModel,
    PrioritizationFeeModel,
    SupplyModel,
    VersionModel,
    VoteAccountsModel,
)


def test_get_health(client):
    client._makeRequest = MagicMock(return_value={"result": "ok"})
    assert client.systemInfo.getHealth() == "ok"
    client._makeRequest.assert_called_once_with("getHealth", [])


def test_get_identity(client):
    client._makeRequest = MagicMock(return_value={"result": {"identity": "ID"}})
    res = client.systemInfo.getIdentity()
    assert isinstance(res, IdentityModel) and res.identity == "ID"
    client._makeRequest.assert_called_once_with("getIdentity", [])


def test_get_version(client):
    client._makeRequest = MagicMock(
        return_value={"result": {"solana-core": "1.18.22", "feature-set": 123}}
    )
    res = client.systemInfo.getVersion()
    assert isinstance(res, VersionModel)
    assert res.solanaCore == "1.18.22" and res.featureSet == 123
    client._makeRequest.assert_called_once_with("getVersion", [])


def test_get_cluster_nodes(client):
    client._makeRequest = MagicMock(
        return_value={
            "result": [
                {
                    "pubkey": "P",
                    "gossip": "g",
                    "tpu": "t",
                    "rpc": "r",
                    "version": "1.0",
                    "featureSet": 1,
                    "shredVersion": 2,
                }
            ]
        }
    )
    res = client.systemInfo.getClusterNodes()
    assert isinstance(res[0], ClusterNodeModel) and res[0].pubkey == "P"
    client._makeRequest.assert_called_once_with("getClusterNodes", [])


def test_get_genesis_hash(client):
    client._makeRequest = MagicMock(return_value={"result": "HASH"})
    assert client.systemInfo.getGenesisHash() == "HASH"
    client._makeRequest.assert_called_once_with("getGenesisHash", [])


def test_get_first_available_block(client):
    client._makeRequest = MagicMock(return_value={"result": 42})
    assert client.systemInfo.getFirstAvailableBlock() == 42
    client._makeRequest.assert_called_once_with("getFirstAvailableBlock", [])


def test_get_recent_performance_samples(client):
    client._makeRequest = MagicMock(
        return_value={
            "result": [
                {
                    "slot": 1,
                    "numTransactions": 10,
                    "numSlots": 2,
                    "samplePeriodSecs": 60,
                    "numNonVoteTransactions": 5,
                }
            ]
        }
    )
    res = client.systemInfo.getRecentPerformanceSamples()
    assert isinstance(res[0], PerformanceSampleModel) and res[0].numTransactions == 10
    client._makeRequest.assert_called_once_with("getRecentPerformanceSamples", [])


def test_get_recent_performance_samples_with_limit(client):
    client._makeRequest = MagicMock(return_value={"result": []})
    client.systemInfo.getRecentPerformanceSamples(5)
    client._makeRequest.assert_called_once_with("getRecentPerformanceSamples", [5])


def test_get_recent_prioritization_fees(client):
    client._makeRequest = MagicMock(
        return_value={"result": [{"slot": 1, "prioritizationFee": 100}]}
    )
    res = client.systemInfo.getRecentPrioritizationFees()
    assert isinstance(res[0], PrioritizationFeeModel) and res[0].prioritizationFee == 100
    client._makeRequest.assert_called_once_with("getRecentPrioritizationFees", [])


def test_get_vote_accounts(client):
    vote = {
        "votePubkey": "VP",
        "nodePubkey": "NP",
        "activatedStake": 1000,
        "epochVoteAccount": True,
        "commission": 5,
        "lastVote": 99,
        "epochCredits": [[1, 2, 3]],
        "rootSlot": 50,
    }
    client._makeRequest = MagicMock(
        return_value={"result": {"current": [vote], "delinquent": []}}
    )
    res = client.systemInfo.getVoteAccounts()
    assert isinstance(res, VoteAccountsModel) and res.current[0].votePubkey == "VP"
    client._makeRequest.assert_called_once_with("getVoteAccounts", [])


def test_get_supply(client):
    client._makeRequest = MagicMock(
        return_value={
            "result": {
                "value": {
                    "total": 100,
                    "circulating": 80,
                    "nonCirculating": 20,
                    "nonCirculatingAccounts": ["A"],
                }
            }
        }
    )
    res = client.systemInfo.getSupply()
    assert isinstance(res, SupplyModel) and res.total == 100
    client._makeRequest.assert_called_once_with("getSupply", [])


def test_get_stake_minimum_delegation(client):
    client._makeRequest = MagicMock(return_value={"result": {"value": 1000000}})
    assert client.systemInfo.getStakeMinimumDelegation() == 1000000
    client._makeRequest.assert_called_once_with("getStakeMinimumDelegation", [])
