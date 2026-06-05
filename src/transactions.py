from __future__ import annotations
from typing import TYPE_CHECKING, Literal
from models.transactions import (
  TransactionModel,
  TSignaturesForAddressModel,
  TransactionsForAddressModel,
  TransfersByAddressModel,
  TSignatureStatusesModel,
  SimulateTransactionModel,
)

if TYPE_CHECKING:
  from helius import Helius, Pubkey


class Transactions:
  """
  Retrieve transaction information from the solana blockchain

  https://www.helius.dev/docs/api-reference/rpc/http-methods#transaction-information

  Methods (8):
    - getTransaction
    - getTransactionCount
    - getSignaturesForAddress
    - getTransactionsForAddress
    - getTransfersByAddress
    - getSignatureStatuses
    - getFeeForMessage
    - sendTransaction
    - simulateTransaction
    - requestAirdrop
  """

  def __init__(self, helius: Helius):
    self._helius: Helius = helius

  def getTransaction(self, signature: str) -> TransactionModel | None:
    """
    Returns transaction details for a confirmed transaction
    """
    _method = "getTransaction"
    _params = [signature, {"maxSupportedTransactionVersion": 0}]

    data = self._helius._makeRequest(_method, _params)
    return TransactionModel(**data["result"]) if data and data["result"] is not None else None

  def getTransactionCount(self) -> int | None:
    """
    Returns the current transaction count from the ledger
    """
    _method = "getTransactionCount"
    _params = []

    data = self._helius._makeRequest(_method, _params)
    return int(data["result"]) if data else None

  def getSignaturesForAddress(self, address: Pubkey, limit: int = 1000) -> list | None:
    """
    Returns signatures for confirmed transactions
    that include the given address
    """
    _method = "getSignaturesForAddress"
    _params = [address, {"limit": limit}]

    data = self._helius._makeRequest(_method, _params)
    return TSignaturesForAddressModel.validate_python(data["result"]) if data else None

  def getTransactionsForAddress(
    self,
    address: Pubkey,
    transactionDetails: Literal["signatures", "full"] = "signatures",
    limit: int = 1000,
    paginationToken: str | None = None,
  ) -> TransactionsForAddressModel | None:
    """
    Returns transaction history for an address with
    server-side filters and pagination
    """
    _method = "getTransactionsForAddress"
    _config: dict[str, str | int] = {"transactionDetails": transactionDetails, "limit": limit}
    if paginationToken is not None:
      _config["paginationToken"] = paginationToken
    _params = [address, _config]

    data = self._helius._makeRequest(_method, _params)
    return TransactionsForAddressModel(**data["result"]) if data else None

  def getTransfersByAddress(
    self,
    address: Pubkey,
    mint: str | None = None,
    limit: int = 1000,
    paginationToken: str | None = None,
  ) -> TransfersByAddressModel | None:
    """
    Returns token and native SOL transfer history
    for a wallet address
    """
    _method = "getTransfersByAddress"
    _config: dict[str, str | int] = {"limit": limit}
    if mint is not None:
      _config["mint"] = mint
    if paginationToken is not None:
      _config["paginationToken"] = paginationToken
    _params = [address, _config]

    data = self._helius._makeRequest(_method, _params)
    return TransfersByAddressModel(**data["result"]) if data else None

  def getSignatureStatuses(
    self, signatures: list[str], searchTransactionHistory: bool = False
  ) -> list | None:
    """
    Returns the statuses of a list of signatures
    """
    _method = "getSignatureStatuses"
    _params = [signatures, {"searchTransactionHistory": searchTransactionHistory}]

    data = self._helius._makeRequest(_method, _params)
    return TSignatureStatusesModel.validate_python(data["result"]["value"]) if data else None

  def getFeeForMessage(self, message: str) -> int | None:
    """
    Returns the fee for a message
    """
    _method = "getFeeForMessage"
    _params = [message]

    data = self._helius._makeRequest(_method, _params)
    return data["result"]["value"] if data else None

  def sendTransaction(self, transaction: str) -> str | None:
    """
    Submits a signed transaction to the cluster for processing
    """
    _method = "sendTransaction"
    _params = [transaction]

    data = self._helius._makeRequest(_method, _params)
    return data["result"] if data else None

  def simulateTransaction(self, transaction: str) -> SimulateTransactionModel | None:
    """
    Simulates the execution of a transaction
    """
    _method = "simulateTransaction"
    _params = [transaction]

    data = self._helius._makeRequest(_method, _params)
    return SimulateTransactionModel(**data["result"]["value"]) if data else None

  def requestAirdrop(self, pubKey: Pubkey, lamports: int) -> str | None:
    """
    Requests an airdrop of lamports to a Pubkey
    """
    _method = "requestAirdrop"
    _params = [pubKey, lamports]

    data = self._helius._makeRequest(_method, _params)
    return data["result"] if data else None
