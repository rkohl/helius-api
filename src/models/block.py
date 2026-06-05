from typing import Any
from pydantic import BaseModel, TypeAdapter


class RewardModel(BaseModel):
  pubkey: str
  lamports: int
  postBalance: int
  rewardType: str | None = None
  commission: int | None = None


class BlockModel(BaseModel):
  blockhash: str
  previousBlockhash: str
  parentSlot: int
  blockHeight: int | None = None
  blockTime: int | None = None
  transactions: list[Any] | None = None
  signatures: list[str] | None = None
  rewards: list[RewardModel] | None = None


TBlocksModel = TypeAdapter(list[int])


class BlockCommitmentModel(BaseModel):
  commitment: list[int] | None = None
  totalStake: int


class BlockProductionRangeModel(BaseModel):
  firstSlot: int
  lastSlot: int


class BlockProductionModel(BaseModel):
  byIdentity: dict[str, list[int]]
  range: BlockProductionRangeModel


class LatestBlockhashModel(BaseModel):
  blockhash: str
  lastValidBlockHeight: int
