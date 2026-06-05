from __future__ import annotations
from typing import TYPE_CHECKING
from .models.slot import (
  TSlotLeadersModel,
  HighestSnapshotSlotModel,
)

if TYPE_CHECKING:
  from .helius import Helius


class Slot:
  """
  Retrieve slot information from the solana blockchain

  https://www.helius.dev/docs/api-reference/rpc/http-methods#slot-information

  Methods (7):
    - getSlot
    - getSlotLeader
    - getSlotLeaders
    - getMinimumLedgerSlot
    - getMaxRetransmitSlot
    - getMaxShredInsertSlot
    - getHighestSnapshotSlot
  """

  def __init__(self, helius: Helius):
    self._helius: Helius = helius

  def getSlot(self) -> int | None:
    """
    Returns the current slot that the node is processing
    """
    _method = "getSlot"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return int(data["result"]) if data else None

  def getSlotLeader(self) -> str | None:
    """
    Returns the identity of the current slot leader
    """
    _method = "getSlotLeader"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return data["result"] if data else None

  def getSlotLeaders(self, startSlot: int, limit: int) -> list[str] | None:
    """
    Returns the slot leaders for a slot range
    """
    _method = "getSlotLeaders"
    _params = [startSlot, limit]

    data = self._helius._makeRequest(_method, _params)
    return TSlotLeadersModel.validate_python(data["result"]) if data else None

  def getMinimumLedgerSlot(self) -> int | None:
    """
    Returns the lowest slot that the node has information about
    """
    _method = "minimumLedgerSlot"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return int(data["result"]) if data else None

  def getMaxRetransmitSlot(self) -> int | None:
    """
    Returns the maximum slot seen from retransmit stage
    """
    _method = "getMaxRetransmitSlot"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return int(data["result"]) if data else None

  def getMaxShredInsertSlot(self) -> int | None:
    """
    Returns the maximum slot seen from shred insert
    """
    _method = "getMaxShredInsertSlot"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return int(data["result"]) if data else None

  def getHighestSnapshotSlot(self) -> HighestSnapshotSlotModel | None:
    """
    Returns the highest available snapshot slot
    """
    _method = "getHighestSnapshotSlot"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return HighestSnapshotSlotModel(**data["result"]) if data else None
