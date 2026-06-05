from __future__ import annotations
import base64
import dataclasses
from typing import Literal, Self, Protocol

type BasicTypes = str|int|bool
type BasicTypesList = list[BasicTypes]
type BasicTypesDict = dict[str, BasicTypes]

type Pubkey = str
type PublicKey = Pubkey
type Identity = Pubkey
"""
Pubkey is a type alias for str that represents a 
Solana public key
"""

type Mint = str
"""
Mint address
"""

type ProgramID = str
"""
Program ID
"""

type Hash = str
"""
A base-58 encoded string
"""

type Blockhash = Hash
"""
Blockhash to check validity status for, 
as a base-58 encoded string
"""

type Address = str
"""
Address is a type alias for str that represents a
Solana address
"""

type Addresses = list[Address]
"""
List of Addresses
"""

type Transaction = str
type Txn = Transaction
"""
Base-64 encoded serialized Solana transaction signature
"""

type Transactions = list[Transaction]
type Txns = Transactions
"""
List of Transactions
"""

type SearchTransactionHistory = bool
"""
Enable searching beyond recent status cache
to find older historical transactions
"""

type Epoch = int
type EpochNumber = Epoch
"""
Specific Solana epoch number
"""


type FilterType = str|int|bool

class Filter:
  def __init__(self, name: str, value: FilterType|list[FilterType]):
    self.name: str = name
    self.value = value

  @property
  def filtering(self) -> dict[str, FilterType|dict[str, FilterType]]:
    n: dict[str, FilterType|dict[str, FilterType]] = {}
    if isinstance(self.value, list):
      for value in self.value:
        if isinstance(value, Filter):
          n.update(value.filtering)
        else:
          n.update({self.name: value})
    else:
      n = {self.name: self.value}
    return n


type Filters = list[Filter]
type Filtering = Filter|Filters
"""
Filters
"""

type AccountFilter = Literal['circulating', 'nonCirculating']
"""
Filter results by account type 
"""

type ExcludeNonCirculatingAccounts = bool
"""
Option to exclude the detailed list of 
non-circulating SOL reserve accounts for 
faster response.
"""

type ShouldSkipPreflight = bool
"""
Skip the preflight transaction checks
"""

type Limit = int
"""
Limit to impose in query 
"""

type Commitment = Literal["processed", "confirmed", "finalized"]
type CommitmentPost = Literal["confirmed", "finalized"]
type CommitmentPre = Literal["processed"]
type CommitmentFinal = Literal["finalized"]
type Commitments = list[Commitment]
type AllCommitments = Commitment|CommitmentPre|CommitmentPost|CommitmentFinal|Commitments
"""
Commitment Level
"""

type PreflightCommitment = Commitment
"""
Commitment level to use for preflight
"""

type Encoding = Literal["base58", "base64", "base64+zstd", "jsonParsed", "json"]

type TransactionDetails = Literal["signatures", "full", "accounts", "none"]
"""
Level of transaction detail to return. If 
accounts are requested, transaction details only 
include signatures and an annotated list of accounts 
in each transaction.
"""

type IncludeRewards = bool
"""
Include and populate the rewards array.
"""

type IncludeAllTokenAccounts = bool
"""
Include all token accounts associated with the address
"""

type KeepUnstakedDelinquents = bool
"""
Include validators that have fallen behind 
but have no stake delegated to them.
"""

type ShouldInclude = bool
"""
Should Include in Response
"""

type ShouldReplace = bool
"""
Should Replace Existng
"""

type WithContext = bool
"""
Wrap the result in an RpcResponse JSON object.
"""

@dataclasses.dataclass
class Options:
  shouldReplace: ShouldReplace|None = None
  shouldInclude: ShouldInclude|None = None
  shouldExcludeNonCirculatingAccountsList: ExcludeNonCirculatingAccounts|None = None
  shouldKeepUnstakedDelinquents: KeepUnstakedDelinquents|None = None
  shouldIncludeAllTokenAccounts: IncludeAllTokenAccounts|None = None
  shouldIncludeRewards: IncludeRewards|None = None
  shouldShouldSkipPreflight: ShouldSkipPreflight|None = None
  shouldWithContext: WithContext|None = None


  def configure(self) -> dict[str, str|int]:
    c = {}
    if self.shouldReplace is not None:
      c["replace"] = self.shouldReplace
    if self.shouldInclude is not None:
      c["include"] = self.shouldInclude
    if self.shouldExcludeNonCirculatingAccountsList is not None:
      c["excludeNonCirculatingAccountsList"] = self.shouldExcludeNonCirculatingAccountsList
    if self.shouldKeepUnstakedDelinquents is not None:
      c["keepUnstakedDelinquents"] = self.shouldKeepUnstakedDelinquents
    if self.shouldIncludeAllTokenAccounts is not None:
      c["includeAllTokenAccounts"] = self.shouldIncludeAllTokenAccounts
    if self.shouldIncludeRewards is not None:
      c["includeRewards"] = self.shouldIncludeRewards
    if self.shouldShouldSkipPreflight is not None:
      c["skipPreflight"] = self.shouldShouldSkipPreflight
    if self.shouldWithContext is not None:
      c['withContext'] = self.shouldWithContext
    return c

@dataclasses.dataclass
class TransactionConfigs:
  details: TransactionDetails|None = None
  maxVersion: int|None = None
  rewards: IncludeRewards|None = None

  def configure(self) -> dict[str, str|int]:
    c = {}
    if self.details is not None:
      c["transactionDetails"] = self.details
    if self.maxVersion is not None:
      c["maxSupportedTransactionVersion"] = self.maxVersion
    if self.rewards is not None:
      c["rewards"] = self.rewards
    return c

@dataclasses.dataclass
class TokenConfigs:
  mint: Mint|None = None
  programId: ProgramID|None = None
  address: Address|None = None

  def configure(self) -> dict[str, str|int]:
    c = {}
    if self.mint is not None:
      c["mint"] = self.mint
    if self.programId is not None:
      c["programId"] = self.programId
    if self.address is not None:
      c["address"] = self.address
    return c

@dataclasses.dataclass
class Accounts:
  """
  Accounts represents a list of accounts metrics to query

  Args:
   - addresses: `Addresses` List of addresses to query
   - encoding: `Encoding` Encoding to use for the account data
   
  """
  
  addresses: Addresses = []
  """
  List of addresses to query
  """
  
  encoding: Encoding = "base64"
  """
  Encoding to use for the account data
  """

@dataclasses.dataclass
class Slice:
  """
  Slice represents a slice of data

  Args:
   - offset: `int` Byte offset from which to start reading
   - length: `int` Number of bytes to return
  """
  
  offset: int = 0
  """
  Byte offset from which to start reading
  """

  length: int = 0
  """
  Number of bytes to return
  """

@dataclasses.dataclass
class Slots:
  """
  Slots represents data for a slot
  """
  
  @dataclasses.dataclass
  class Range:
    """
    Range represents a range of slots
    """
    first: int
    """
    First slot in the range
    """
    last: int
    """
    Last slot in the range
    """

  slot: int|None = None
  """
  Current slot
  """

  starting: int|None = None
  """
  Starting slot
  """
  
  minContext:  int|None = None
  """
  The minimum slot that the request can be evaluated at
  """
  
  changedSince: int|None = None
  """
  Only return the account if it has been modified at 
  or after this slot number. If the account exists but 
  hasn't changed since the specified slot, the response 
  will contain status as 'unchanged'. If the account 
  does not exist, the response will contain 
  status as 'notFound'.
  """

  range: Range|None = None
  """
  Range of slots to query
  """
  
  delinquentDistance: int|None = None
  """
  Custom threshold of slots behind to mark 
  validators as delinquent or underperforming.
  """

class Configuratation(Protocol):
  
  @property
  def configure(self) -> dict[str, str|int|bool|list[str|int|bool]]:
    ...

class Configurator(Configuratation):

  def __init__(self, 
               commitment: AllCommitments|None = None, 
               encoding: Encoding|None = None,
               slice: Slice|None = None, 
               slot: Slots|None = None,
               limit: Limit|None = None,
               identity: Identity|None = None,
               filters: Filter|Filters|None = None,
               configs: list[Options|TokenConfigs|TransactionConfigs]|None = None):
    self.commitment = commitment
    self.encoding = encoding
    self.slice = slice
    self.slot = slot
    self.limit = limit
    self.identity = identity
    self.configs = configs if configs is not None else []
    self.filters = filters

  @property
  def configure(self) -> dict[str, str|int|bool|list[str|int|bool]]:
    c = {}
    if self.commitment is not None:
      if isinstance(self.commitment, list):
       c["commitment"] = [commitment for commitment in self.commitment]
      else:
       c["commitment"] = self.commitment

    if self.encoding is not None:
      c["encoding"] = self.encoding
    
    if self.slice is not None:
      s = {}
      if self.slice.offset is not None:
        s["offset"] = self.slice.offset
      if self.slice.length is not None:
        s["length"] = self.slice.length
      if 0 < len(s):
         c["dataSlice"] = s

    if self.slot is not None:
     if self.slot.slot is not None:
       c["slot"] = self.slot.slot
     if self.slot.starting is not None:
       c["start_slot"] = self.slot.starting
     if self.slot.minContext is not None:
       c["minContextSlot"] = self.slot.minContext
     if self.slot.changedSince is not None:
       c["changedSinceSlot"] = self.slot.changedSince
     if self.slot.range is not None:
       c["range"] = {
         "firstSlot": self.slot.range.first,
         "lastSlot": self.slot.range.last
       }
     if self.slot.delinquentDistance is not None:
       c["delinquentSlotDistance"] = self.slot.delinquentDistance

    if self.limit is not None:
      c["limit"] = self.limit

    if self.identity is not None:
      c["identity"] = self.identity

    if 0 < len(self.configs) :
      for config in self.configs:
        c.update(config.configure())

    if self.filters is not None:
      f = []
      if isinstance(self.filters, list):
        for filter in self.filters:
          if isinstance(filter, Filter):
            f.append(filter.filtering)
          if isinstance(filter, dict):
            f.append(filter)
      else:
        f.append(self.filters.filtering)
      c["filters"] = [f]

    return c

class BasicConfigurator(Configuratation):

  def __init__(self, 
               commitment: AllCommitments|None = None, 
               slice: Slice|None = None, 
               slot: Slots|None = None,
               limit: Limit|None = None
              ):
    self.commitment = commitment
    self.slice = slice
    self.slot = slot
    self.limit = limit
  
  @property
  def configure(self) -> dict[str, str|int|bool|list[str|int|bool]]:
    c = {}
    if self.commitment is not None:
      if isinstance(self.commitment, list):
       c["commitment"] = [commitment for commitment in self.commitment]
      else:
       c["commitment"] = self.commitment
  
    if self.slice is not None:
      s = {}
      if self.slice.offset is not None:
        s["offset"] = self.slice.offset
      if self.slice.length is not None:
        s["length"] = self.slice.length
      if 0 < len(s):
         c["dataSlice"] = s
  
    if self.slot is not None:
     if self.slot.slot is not None:
       c["slot"] = self.slot.slot
     if self.slot.starting is not None:
       c["start_slot"] = self.slot.starting
     if self.slot.minContext is not None:
       c["minContextSlot"] = self.slot.minContext
     if self.slot.changedSince is not None:
       c["changedSinceSlot"] = self.slot.changedSince
     if self.slot.range is not None:
       c["range"] = {
         "firstSlot": self.slot.range.first,
         "lastSlot": self.slot.range.last
       }
     if self.slot.delinquentDistance is not None:
       c["delinquentSlotDistance"] = self.slot.delinquentDistance
  
    if self.limit is not None:
      c["limit"] = self.limit
  
  
    return c

class SlotSliceConfigurator(Configuratation):

  def __init__(self, slice: Slice|None = None, slot: Slots|None = None):
    self.slice = slice
    self.slot = slot
  
  @property
  def configure(self) -> dict[str, str|int|bool|list[str|int|bool]]:
    c = {}
  
    if self.slice is not None:
      s = {}
      if self.slice.offset is not None:
        s["offset"] = self.slice.offset
      if self.slice.length is not None:
        s["length"] = self.slice.length
      if 0 < len(s):
         c["dataSlice"] = s
  
    if self.slot is not None:
     if self.slot.slot is not None:
       c["slot"] = self.slot.slot
     if self.slot.starting is not None:
       c["start_slot"] = self.slot.starting
     if self.slot.minContext is not None:
       c["minContextSlot"] = self.slot.minContext
     if self.slot.changedSince is not None:
       c["changedSinceSlot"] = self.slot.changedSince
     if self.slot.range is not None:
       c["range"] = {
         "firstSlot": self.slot.range.first,
         "lastSlot": self.slot.range.last
       }
     if self.slot.delinquentDistance is not None:
       c["delinquentSlotDistance"] = self.slot.delinquentDistance
  
    return c
  