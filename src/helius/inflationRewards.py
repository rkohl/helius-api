from __future__ import annotations
from typing import TYPE_CHECKING
from .types import PublicKey
from .models.inflationRewards import (
  InflationGovernorModel,
  InflationRateModel,
  TInflationRewardModel,
)

if TYPE_CHECKING:
  from .helius import Helius
  from .types import PublicKey


class InflationRewards:
  """
  Retrieve inflation and rewards information
  from the solana blockchain

  https://www.helius.dev/docs/api-reference/rpc/http-methods#inflation-&-rewards

  Methods (3):
    - getInflationGovernor
    - getInflationRate
    - getInflationReward
  """

  def __init__(self, helius: Helius):
    self._helius: Helius = helius

  def getInflationGovernor(self) -> InflationGovernorModel | None:
    """
    Returns the current inflation governor parameters
    """
    _method = "getInflationGovernor"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return InflationGovernorModel(**data["result"]) if data else None

  def getInflationRate(self) -> InflationRateModel | None:
    """
    Returns the specific inflation values for the current epoch
    """
    _method = "getInflationRate"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return InflationRateModel(**data["result"]) if data else None

  def getInflationReward(self, addresses: list[PublicKey], epoch: int | None = None) -> list | None:
    """
    Returns the inflation reward for a list
    of addresses for an epoch
    """
    _method = "getInflationReward"
    _params = [addresses] if epoch is None else [addresses, {"epoch": epoch}]

    data = self._helius._makeRequest(_method, _params)
    return TInflationRewardModel.validate_python(data["result"]) if data else None
