from pydantic import BaseModel, TypeAdapter


class InflationGovernorModel(BaseModel):
  initial: float
  terminal: float
  taper: float
  foundation: float
  foundationTerm: float

class InflationRateModel(BaseModel):
  total: float
  validator: float
  foundation: float
  epoch: int

class InflationRewardModel(BaseModel):
  epoch: int
  effectiveSlot: int
  amount: int
  postBalance: int
  commission: int | None = None

TInflationRewardModel = TypeAdapter(list[InflationRewardModel | None])
