from __future__ import annotations
from typing import TYPE_CHECKING

from .models.token import (
  TokenAmountModel,
  TTokenAccountsModel,
  TTokenLargestAccountsModel,
)

if TYPE_CHECKING:
  from .helius import Helius
  from .types import PublicKey, Mint


class Token:
  """
  Retrieve token information from the solana blockchain

  https://www.helius.dev/docs/api-reference/rpc/http-methods#token-information

  Methods (5):
    - getTokenAccountBalance
    - getTokenAccountsByOwner
    - getTokenAccountsByDelegate
    - getTokenLargestAccounts
    - getTokenSupply
  """

  def __init__(self, helius: Helius):
    self._helius: Helius = helius

  def getTokenAccountBalance(self, publicKey: PublicKey) -> TokenAmountModel | None:
    """
    Returns the token balance of an account
    """
    _method = "getTokenAccountBalance"
    _params = [publicKey]

    data = self._helius._makeRequest(_method, _params)
    return TokenAmountModel(**data["result"]["value"]) if data else None

  def getTokenAccountsByOwner(self, owner: PublicKey, mint: PublicKey) -> list | None:
    """
    Returns all token accounts owned by the specified address
    """
    _method = "getTokenAccountsByOwner"
    _params = [owner, {"mint": mint}, {"encoding": "jsonParsed"}]

    data = self._helius._makeRequest(_method, _params)
    return TTokenAccountsModel.validate_python(data["result"]["value"]) if data else None

  def getTokenAccountsByDelegate(self, delegate: PublicKey, mint: Mint) -> list | None:
    """
    Returns all token accounts that delegate to the specified address
    """
    _method = "getTokenAccountsByDelegate"
    _params = [delegate, {"mint": mint}, {"encoding": "jsonParsed"}]

    data = self._helius._makeRequest(_method, _params)
    return TTokenAccountsModel.validate_python(data["result"]["value"]) if data else None

  def getTokenLargestAccounts(self, mint: Mint) -> list | None:
    """
    Returns the largest accounts for a specific token
    """
    _method = "getTokenLargestAccounts"
    _params = [mint]

    data = self._helius._makeRequest(_method, _params)
    return TTokenLargestAccountsModel.validate_python(data["result"]["value"]) if data else None

  def getTokenSupply(self, mint: Mint) -> TokenAmountModel | None:
    """
    Returns the total supply of a token
    """
    _method = "getTokenSupply"
    _params = [mint]

    data = self._helius._makeRequest(_method, _params)
    return TokenAmountModel(**data["result"]["value"]) if data else None
