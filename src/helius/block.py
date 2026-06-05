from __future__ import annotations
from typing import TYPE_CHECKING
from .models.block import (
  BlockModel,
  TBlocksModel,
  BlockCommitmentModel,
  BlockProductionModel,
  LatestBlockhashModel,
)

if TYPE_CHECKING:
  from .helius import Helius


class Block:
  """
  Retrieve block information from the solana blockchain

  https://www.helius.dev/docs/api-reference/rpc/http-methods#block-information

  Methods (9):
    - getBlock
    - getBlocks
    - getBlocksWithLimit
    - getBlockHeight
    - getBlockTime
    - getBlockCommitment
    - getBlockProduction
    - getLatestBlockhash
    - isBlockhashValid
  """

  def __init__(self, helius: Helius):
    self._helius: Helius = helius

  def getBlock(self, slot: int) -> BlockModel | None:
    """
    Returns identity and transaction information
    about a confirmed block
    """
    _method = "getBlock"
    _params = [slot, {"maxSupportedTransactionVersion": 0}]

    data = self._helius._makeRequest(_method, _params)
    return BlockModel(**data["result"]) if data and data["result"] is not None else None

  def getBlocks(self, startSlot: int, endSlot: int | None = None) -> list[int] | None:
    """
    Returns a list of confirmed blocks between two slots
    """
    _method = "getBlocks"
    _params = [startSlot] if endSlot is None else [startSlot, endSlot]

    data = self._helius._makeRequest(_method, _params)
    return TBlocksModel.validate_python(data["result"]) if data else None

  def getBlocksWithLimit(self, startSlot: int, limit: int) -> list[int] | None:
    """
    Returns a list of confirmed blocks starting
    at a given slot with a limit
    """
    _method = "getBlocksWithLimit"
    _params = [startSlot, limit]

    data = self._helius._makeRequest(_method, _params)
    return TBlocksModel.validate_python(data["result"]) if data else None

  def getBlockHeight(self) -> int | None:
    """
    Returns the current block height of the node
    """
    _method = "getBlockHeight"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return int(data["result"]) if data else None

  def getBlockTime(self, slot: int) -> int | None:
    """
    Returns the estimated production time of a block
    """
    _method = "getBlockTime"
    _params = [slot]

    data = self._helius._makeRequest(_method, _params)
    return data["result"] if data else None

  def getBlockCommitment(self, slot: int) -> BlockCommitmentModel | None:
    """
    Returns commitment information for a block
    """
    _method = "getBlockCommitment"
    _params = [slot]

    data = self._helius._makeRequest(_method, _params)
    return BlockCommitmentModel(**data["result"]) if data else None

  def getBlockProduction(self) -> BlockProductionModel | None:
    """
    Returns recent block production information
    """
    _method = "getBlockProduction"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return BlockProductionModel(**data["result"]["value"]) if data else None

  def getLatestBlockhash(self) -> LatestBlockhashModel | None:
    """
    Returns the latest blockhash
    """
    _method = "getLatestBlockhash"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return LatestBlockhashModel(**data["result"]["value"]) if data else None

  def isBlockhashValid(self, blockhash: str) -> bool | None:
    """
    Returns whether a blockhash is still valid or not
    """
    _method = "isBlockhashValid"
    _params = [blockhash]

    data = self._helius._makeRequest(_method, _params)
    return bool(data["result"]["value"]) if data else None
