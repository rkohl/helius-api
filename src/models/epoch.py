from pydantic import BaseModel, TypeAdapter


class EpochInfoModel(BaseModel):
  absoluteSlot: int
  blockHeight: int
  epoch: int
  slotIndex: int
  slotsInEpoch: int
  transactionCount: int | None = None

class EpochScheduleModel(BaseModel):
  slotsPerEpoch: int
  leaderScheduleSlotOffset: int
  warmup: bool
  firstNormalEpoch: int
  firstNormalSlot: int

TLeaderScheduleModel = TypeAdapter(dict[str, list[int]])
