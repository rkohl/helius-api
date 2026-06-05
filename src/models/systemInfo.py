from pydantic import BaseModel, Field, TypeAdapter


class IdentityModel(BaseModel):
  identity: str

class VersionModel(BaseModel):
  solanaCore: str = Field(alias="solana-core")
  featureSet: int | None = Field(default=None, alias="feature-set")

class ClusterNodeModel(BaseModel):
  pubkey: str
  gossip: str | None = None
  tpu: str | None = None
  rpc: str | None = None
  version: str | None = None
  featureSet: int | None = None
  shredVersion: int | None = None

TClusterNodesModel = TypeAdapter(list[ClusterNodeModel])

class PerformanceSampleModel(BaseModel):
  slot: int
  numTransactions: int
  numSlots: int
  samplePeriodSecs: int
  numNonVoteTransactions: int | None = None

TPerformanceSamplesModel = TypeAdapter(list[PerformanceSampleModel])

class PrioritizationFeeModel(BaseModel):
  slot: int
  prioritizationFee: int

TPrioritizationFeesModel = TypeAdapter(list[PrioritizationFeeModel])

class VoteAccountModel(BaseModel):
  votePubkey: str
  nodePubkey: str
  activatedStake: int
  epochVoteAccount: bool
  commission: int
  lastVote: int
  epochCredits: list[list[int]]
  rootSlot: int | None = None

class VoteAccountsModel(BaseModel):
  current: list[VoteAccountModel]
  delinquent: list[VoteAccountModel]

class SupplyModel(BaseModel):
  total: int
  circulating: int
  nonCirculating: int
  nonCirculatingAccounts: list[str]
