from typing import Literal, TypeAlias

Pubkey: TypeAlias = str
HTTPMethod = Literal["GET", "POST"]

from models.error import ErrorModel
from accounts import Accounts
from block import Block
from transactions import Transactions
from token import Token
from slot import Slot
from epoch import Epoch
from inflationRewards import InflationRewards
from systemInfo import SystemInfo


class Helius:
  """
  Helius RPC client for Solana that offers a variety 
  of features including enhanced transaction history, 
  token metadata, and more.
  https://www.helius.dev/docs/api-reference/rpc/http-methods

  The Helius class is the main entry point for interacting 
  with the Helius RPC API. It provides methods for retrieving 
  information about accounts, blocks, transactions, tokens, 
  slots, epochs, inflation and rewards, and system information.

  Attributes:
    apiKey (str): The API key for the Helius RPC API.
    jsonrpc (str): The JSON-RPC version to use. Defaults to "2.0".
    id (int): The ID to use for JSON-RPC requests. Defaults to 1.
    url (str): The base URL for the Helius RPC API. Defaults to "https://mainnet.helius-rpc.com".
  """

  def __init__(
    self, apiKey: str, jsonrpc: str | None = None, id: int | None = None, url: str | None = None
  ):
    self._apiKey = apiKey
    self._jsonrpc = jsonrpc if jsonrpc is None else "2.0"
    self._id = id if id is not None else 1
    self._baseURL = "https://mainnet.helius-rpc.com" if url is None else url

  @property
  def url(self) -> str:
    """
    Returns the URL for the Helius RPC API. The URL
    is constructed using the base URL and the API key.
    """
    return f"{self._baseURL}/?api-key={self._apiKey}"

  def _makeRequest(self, call: str, params: list) -> dict | None:
    """
    Private function to make a try/catch request to the
    Helius RPC API.
    Returns response data if the request was successful,
    otherwise returns None.

    Args:
      call (str): The RPC method to call.
      params (list): The parameters to pass to the RPC method.

    Returns:
      dict | None: The response from the RPC API, or None if the request failed.
    """
    from re
    headers = {"Content-Type": "application/json"}
    payload = {"jsonrpc": self._jsonrpc, "id": self._id, "method": call, "params": params}

    try:
      response = requests.post(self.url, json=payload, headers=headers, timeout=30)
      response.raise_for_status()
      data = response.json()
    except requests.exceptions.RequestException as e:
      print(f"Error making request: {e}")
      return None

    if "error" in data:
      error = ErrorModel(**data["error"])
      print(f"RPC error ({error.code}): {error.message}")
      return None

    return data

  @property
  def accounts(self) -> Accounts:
    """
    Accounts Endpoints (6):
      - getAccountInfo
      - getBalance
      - getProgramAccounts
      - getMultipleAccounts
      - getMinimumBalanceForRentExemption
      - getLargestAccounts
    """
    return Accounts(self)

  @property
  def block(self) -> Block:
    """
    Block Endpoints (9):
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
    return Block(self)

  @property
  def epoch(self) -> Epoch:
    """
    Epoch Endpoints (3):
      - getEpochInfo
      - getEpochSchedule
      - getLeaderSchedule
    """
    return Epoch(self)

  @property
  def inflationRewards(self) -> InflationRewards:
    """
    Inflation & Rewards Endpoints (3):
      - getInflationGovernor
      - getInflationRate
      - getInflationReward
    """
    return InflationRewards(self)

  @property
  def slot(self) -> Slot:
    """
    Slot Endpoints (7):
      - getSlot
      - getSlotLeader
      - getSlotLeaders
      - getMinimumLedgerSlot
      - getMaxRetransmitSlot
      - getMaxShredInsertSlot
      - getHighestSnapshotSlot
    """
    return Slot(self)

  @property
  def systemInfo(self) -> SystemInfo:
    """
    System Information Endpoints (11):
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
    return SystemInfo(self)

  @property
  def token(self) -> Token:
    """
    Token Endpoints (5):
      - getTokenAccountBalance
      - getTokenAccountsByOwner
      - getTokenAccountsByDelegate
      - getTokenLargestAccounts
      - getTokenSupply
    """
    return Token(self)

  @property
  def transactions(self) -> Transactions:
    """
    Transaction Endpoints (8):
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
    return Transactions(self)
