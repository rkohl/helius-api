from pydantic import BaseModel, TypeAdapter


TSlotLeadersModel = TypeAdapter(list[str])

class HighestSnapshotSlotModel(BaseModel):
  full: int
  incremental: int | None = None
