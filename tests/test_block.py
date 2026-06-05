from unittest.mock import MagicMock

from helius.models.block import (
    BlockCommitmentModel,
    BlockModel,
    BlockProductionModel,
    LatestBlockhashModel,
)


def test_get_block(client):
    client._makeRequest = MagicMock(
        return_value={
            "result": {
                "blockhash": "BH",
                "previousBlockhash": "PBH",
                "parentSlot": 10,
                "blockHeight": 9,
                "blockTime": 123,
                "transactions": [],
                "signatures": None,
                "rewards": None,
            }
        }
    )
    res = client.block.getBlock(100)
    assert isinstance(res, BlockModel) and res.blockhash == "BH" and res.parentSlot == 10
    client._makeRequest.assert_called_once_with(
        "getBlock", [100, {"maxSupportedTransactionVersion": 0}]
    )


def test_get_blocks(client):
    client._makeRequest = MagicMock(return_value={"result": [1, 2, 3]})
    assert client.block.getBlocks(1, 3) == [1, 2, 3]
    client._makeRequest.assert_called_once_with("getBlocks", [1, 3])


def test_get_blocks_no_end(client):
    client._makeRequest = MagicMock(return_value={"result": [1]})
    client.block.getBlocks(1)
    client._makeRequest.assert_called_once_with("getBlocks", [1])


def test_get_blocks_with_limit(client):
    client._makeRequest = MagicMock(return_value={"result": [5, 6]})
    assert client.block.getBlocksWithLimit(5, 2) == [5, 6]
    client._makeRequest.assert_called_once_with("getBlocksWithLimit", [5, 2])


def test_get_block_height(client):
    client._makeRequest = MagicMock(return_value={"result": 777})
    assert client.block.getBlockHeight() == 777
    client._makeRequest.assert_called_once_with("getBlockHeight", [])


def test_get_block_time(client):
    client._makeRequest = MagicMock(return_value={"result": 1690000000})
    assert client.block.getBlockTime(100) == 1690000000
    client._makeRequest.assert_called_once_with("getBlockTime", [100])


def test_get_block_commitment(client):
    client._makeRequest = MagicMock(
        return_value={"result": {"commitment": [1, 2], "totalStake": 1000}}
    )
    res = client.block.getBlockCommitment(100)
    assert isinstance(res, BlockCommitmentModel) and res.totalStake == 1000
    client._makeRequest.assert_called_once_with("getBlockCommitment", [100])


def test_get_block_production(client):
    client._makeRequest = MagicMock(
        return_value={
            "result": {
                "value": {
                    "byIdentity": {"id1": [10, 5]},
                    "range": {"firstSlot": 0, "lastSlot": 100},
                }
            }
        }
    )
    res = client.block.getBlockProduction()
    assert isinstance(res, BlockProductionModel) and res.range.lastSlot == 100
    client._makeRequest.assert_called_once_with("getBlockProduction", [])


def test_get_latest_blockhash(client):
    client._makeRequest = MagicMock(
        return_value={"result": {"value": {"blockhash": "BH", "lastValidBlockHeight": 999}}}
    )
    res = client.block.getLatestBlockhash()
    assert isinstance(res, LatestBlockhashModel) and res.lastValidBlockHeight == 999
    client._makeRequest.assert_called_once_with("getLatestBlockhash", [])


def test_is_blockhash_valid(client):
    client._makeRequest = MagicMock(return_value={"result": {"value": True}})
    assert client.block.isBlockhashValid("BH") is True
    client._makeRequest.assert_called_once_with("isBlockhashValid", ["BH"])
