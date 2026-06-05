from __future__ import annotations
from typing import TYPE_CHECKING
from .types import PublicKey, Encoding, Address, Addresses, Commitment, Slice, Slots, Configurator, BasicTypes, BasicTypesList, BasicTypesDict, Filter, Filters, Filtering, AccountFilter
from .models.accounts import (
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
  from .helius import Helius
  from .types import PublicKey, Encoding, Commitment, Slice, Slots, Address

type AccountParams = list[Address|Addresses|PublicKey|str|int|dict[str, BasicTypes|BasicTypesList|BasicTypesList]]

class Accounts:
  """
  Retrieve information about accounts from the solana blockchain

  https://www.helius.dev/docs/api-reference/rpc/http-methods#account-information

  Methods (6):
    - getInfo
    - getBalance
    - getPrograms
    - getMultiple
    - getMinimumRentBalance
    - getLargest
  """

  def __init__(self, helius: Helius):
    self._helius: Helius = helius

  def getInfo(self, 
              publicKey: PublicKey,
              commitment: Commitment = "finalized", 
              encoding: Encoding = "base64", 
              slice: Slice | None = None, 
              slot: Slots | None = None
              ) -> AccountInfoModel | None:
    """
    Returns all information associated with
    the account of provided Pubkey

    Args:
     - pubKey: `Pubkey` of the account to query

    Retuns: 
      `AccountInfoModel` or None
    """
    _method = "getAccountInfo"
    _params: AccountParams = [publicKey]
    _config = Configurator(commitment=commitment, 
                           slice=slice, 
                           slot=slot)
    _params.append(_config.configure)

    data = self._helius._makeRequest(_method, _params)
    return AccountInfoModel(**data["result"]["value"]) if data else None

  def getBalance(self, 
                 publicKey: PublicKey, 
                 commitment: Commitment = "finalized", 
                 slot: Slots | None = None
                 ) -> int | None:
    """
    Returns the lamport balance of the
    account of provided Pubkey

    Args:
      - pubKey: Pubkey of the account to query

    Returns:
      int or None
    """
    _method = "getBalance"
    _params: AccountParams = [publicKey]
    _config = Configurator(commitment=commitment, 
                           slot=slot)
    _params.append(_config.configure)

    data = self._helius._makeRequest(_method, _params)
    return int(data["result"]["value"]) if data else None

  def getPrograms(self, 
                 address: Address,
                 commitment: Commitment = "finalized", 
                 encoding: Encoding = "base64", 
                 slice: Slice | None = None, 
                 slot: Slots | None = None,
                 filters: Filtering | None = None, 
                 withContext: bool| None = None) -> list[ProgramAccountsModel] | None:
    """
    Returns all accounts owned by the
    provided program Pubkey

    Args:
      - pubKey: Pubkey of the program to query

    Returns:
      list[ProgramAccountsModel] or None
    """
    _method = "getProgramAccounts"
    _params: AccountParams = [address]
    _config = Configurator(commitment=commitment, 
                           encoding=encoding,
                           slice=slice, 
                           slot=slot,
                           filters=filters)
    _params.append(_config.configure)
    if withContext is not None:
      _params.append({"withContext": withContext})

    data = self._helius._makeRequest(_method, _params)
    return TProgramAccountsModel.validate_python(data["result"]) if data else None

  def getMultiple(self, 
                  addresses: Addresses, 
                  commitment: Commitment = "finalized", 
                  encoding: Encoding = "base64", 
                  slice: Slice | None = None, 
                  slot: Slots | None = None) -> list[AccountInfoModel | None] | None:
    """
    Returns information about multiple accounts
    for the provided list of Pubkeys

    Args:
      - pubKeys: list of `Pubkeys` to query

    Returns:
      list[`AccountInfoModel` | None] or None
    """
    _method = "getMultipleAccounts"
    _params: AccountParams = [addresses]
    _config = Configurator(commitment=commitment, 
                           encoding=encoding,
                           slice=slice, 
                           slot=slot)
    _params.append(_config.configure)

    data = self._helius._makeRequest(_method, _params)
    return TMultipleAccountsModel.validate_python(data["result"]["value"]) if data else None

  def getMinimumRentBalance(self, 
                        minimum: int = 50, 
                        commitment: Commitment = "finalized") -> int | None:
    """
    Returns minimum balance required to make account rent exempt

    Args:
      - minimum: `int` Size of account data in bytes that you need to 
        store on the Solana blockchain.

    Returns:
      `int` or None
    """
    _method = "getMinimumBalanceForRentExemption"
    _params: AccountParams = [minimum]
    _config = Configurator(commitment=commitment)
    _params.append(_config.configure)


    data = self._helius._makeRequest(_method, _params)
    return int(data["result"]) if data else None

  def getLargest(self, 
                 filter: AccountFilter = "circulating", 
                 commitment: Commitment = "finalized") -> list[LargestAccountsModel] | None:
    """
    Returns the 20 largest accounts, by lamport balance
    (results may be cached up to two hours
    """
    _method = "getLargestAccounts"
    _params: AccountParams = [{"filter": filter}]
    _config = Configurator(commitment=commitment)
    _params.append(_config.configure)

    data = self._helius._makeRequest(_method, _params)
    return TLargestAccountsModel.validate_python(data["result"]["value"]) if data else None
    