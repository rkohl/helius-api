from __future__ import annotations
from typing import TYPE_CHECKING
from models.accounts import (
  AccountInfoModel,
  AccountBalanceModel,
  TMultipleAccountsModel,
  TProgramAccountsModel,
  ProgramAccountsModel,
  TLargestAccountsModel,
  LargestAccountsModel,
  TLargestAccountsModel,
)

if TYPE_CHECKING:
  from .helius import Helius, Pubkey


class Accounts:
  """
  Retrieve information about accounts from the solana blockchain

  https://www.helius.dev/docs/api-reference/rpc/http-methods#account-information

  Methods (6):
    - getAccountInfo
    - getBalance
    - getProgramAccounts
    - getMultipleAccounts
    - getMinimumBalanceForRentExemption
    - getLargestAccounts
  """

  def __init__(self, helius: Helius):
    self._helius: Helius = helius

  def getAccountInfo(self, pubKey: Pubkey) -> AccountInfoModel | None:
    """
    Returns all information associated with
    the account of provided Pubkey
    """
    _method = "getAccountInfo"
    _params = [pubKey]

    data = self._helius._makeRequest(_method, _params)
    return AccountInfoModel(**data["result"]["value"]) if data else None

  def getBalance(self, pubKey: Pubkey) -> int | None:
    """
    Returns the lamport balance of the
    account of provided Pubkey
    """
    _method = "getBalance"
    _params = [pubKey]

    data = self._helius._makeRequest(_method, _params)
    return int(data["result"]["value"]) if data else None

  def getProgramAccounts(self, pubKey: Pubkey) -> list[ProgramAccountsModel] | None:
    """
    Returns all accounts owned by the
    provided program Pubkey
    """
    _method = "getProgramAccounts"
    _params = [pubKey]

    data = self._helius._makeRequest(_method, _params)
    return TProgramAccountsModel.validate_python(data["result"]) if data else None

  def getMultipleAccounts(self, pubKeys: list[Pubkey]) -> list[AccountInfoModel | None] | None:
    """
    Returns information about multiple accounts
    for the provided list of Pubkeys
    """
    _method = "getMultipleAccounts"
    _params = [pubKeys]

    data = self._helius._makeRequest(_method, _params)
    return TMultipleAccountsModel.validate_python(data["result"]["value"]) if data else None

  def getMinimumBalanceForRentExemption(self, pubKey: Pubkey) -> int | None:
    """
    Returns minimum balance required to make account rent exempt
    """
    _method = "getMinimumBalanceForRentExemption"
    _params = [pubKey]

    data = self._helius._makeRequest(_method, _params)
    return int(data["result"]) if data else None

  def getLargestAccounts(self) -> list[LargestAccountsModel] | None:
    """
    Returns the 20 largest accounts, by lamport balance
    (results may be cached up to two hours
    """
    _method = "getLargestAccounts"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return TLargestAccountsModel.validate_python(data["result"]["value"]) if data else None
    