from __future__ import annotations
from typing import TYPE_CHECKING
from models.systemInfo import (
  IdentityModel,
  VersionModel,
  TClusterNodesModel,
  TPerformanceSamplesModel,
  TPrioritizationFeesModel,
  VoteAccountsModel,
  SupplyModel,
)

if TYPE_CHECKING:
  from helius import Helius, Pubkey


class SystemInfo:
  """
  Retrieve system information from the solana blockchain

  https://www.helius.dev/docs/api-reference/rpc/http-methods#system-information

  Methods (11):
    - getHealth
    - getIdentity
    - getVersion
    - getClusterNodes
    - getGenesisHash
    - getFirstAvailableBlock
    - getRecentPerformanceSamples
    - getRecentPrioritizationFees
    - getVoteAccounts
    - getSupply
    - getStakeMinimumDelegation
  """

  def __init__(self, helius: Helius):
    self._helius: Helius = helius

  def getHealth(self) -> str | None:
    """
    Returns the current health status of the node
    """
    _method = "getHealth"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return data["result"] if data else None

  def getIdentity(self) -> IdentityModel | None:
    """
    Returns the identity pubkey for the current node
    """
    _method = "getIdentity"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return IdentityModel(**data["result"]) if data else None

  def getVersion(self) -> VersionModel | None:
    """
    Returns the current software version running on the node
    """
    _method = "getVersion"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return VersionModel(**data["result"]) if data else None

  def getClusterNodes(self) -> list | None:
    """
    Returns information about all the nodes in the cluster
    """
    _method = "getClusterNodes"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return TClusterNodesModel.validate_python(data["result"]) if data else None

  def getGenesisHash(self) -> str | None:
    """
    Returns the genesis hash
    """
    _method = "getGenesisHash"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return data["result"] if data else None

  def getFirstAvailableBlock(self) -> int | None:
    """
    Returns the lowest slot that the node has information about
    """
    _method = "getFirstAvailableBlock"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return int(data["result"]) if data else None

  def getRecentPerformanceSamples(self, limit: int | None = None) -> list | None:
    """
    Returns a list of recent performance samples
    """
    _method = "getRecentPerformanceSamples"
    _params = [] if limit is None else [limit]

    data = self._helius._makeRequest(_method, _params)
    return TPerformanceSamplesModel.validate_python(data["result"]) if data else None

  def getRecentPrioritizationFees(self, addresses: list[Pubkey] | None = None) -> list | None:
    """
    Returns recent block hash fee information
    """
    _method = "getRecentPrioritizationFees"
    _params = [] if addresses is None else [addresses]

    data = self._helius._makeRequest(_method, _params)
    return TPrioritizationFeesModel.validate_python(data["result"]) if data else None

  def getVoteAccounts(self) -> VoteAccountsModel | None:
    """
    Returns the current vote accounts
    """
    _method = "getVoteAccounts"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return VoteAccountsModel(**data["result"]) if data else None

  def getSupply(self) -> SupplyModel | None:
    """
    Returns information about the current supply
    """
    _method = "getSupply"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return SupplyModel(**data["result"]["value"]) if data else None

  def getStakeMinimumDelegation(self) -> int | None:
    """
    Returns the minimum delegation required for staking
    """
    _method = "getStakeMinimumDelegation"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return int(data["result"]["value"]) if data else None
