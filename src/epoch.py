from __future__ import annotations
from typing import TYPE_CHECKING
from models.epoch import (
  EpochInfoModel,
  EpochScheduleModel,
  TLeaderScheduleModel,
)

if TYPE_CHECKING:
  from helius import Helius


class Epoch:
  """
  Retrieve epoch information from the solana blockchain

  https://www.helius.dev/docs/api-reference/rpc/http-methods#epoch-information

  Methods (3):
    - getEpochInfo
    - getEpochSchedule
    - getLeaderSchedule
  """

  def __init__(self, helius: Helius):
    self._helius: Helius = helius

  def getEpochInfo(self) -> EpochInfoModel | None:
    """
    Returns information about the current epoch
    """
    _method = "getEpochInfo"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return EpochInfoModel(**data["result"]) if data else None

  def getEpochSchedule(self) -> EpochScheduleModel | None:
    """
    Returns epoch schedule information
    """
    _method = "getEpochSchedule"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return EpochScheduleModel(**data["result"]) if data else None

  def getLeaderSchedule(self, slot: int | None = None) -> dict[str, list[int]] | None:
    """
    Returns the leader schedule for an epoch
    """
    _method = "getLeaderSchedule"
    _params = [] if slot is None else [slot]

    data = self._helius._makeRequest(_method, _params)
    return (
      TLeaderScheduleModel.validate_python(data["result"])
      if data and data["result"] is not None
      else None
    )
