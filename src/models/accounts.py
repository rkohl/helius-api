from pydantic import BaseModel, TypeAdapter


class AccountInfoModel(BaseModel):
  lamports: int
  owner: str
  data: list[str]
  executable: bool
  rentEpoch: int
  space: int


class AccountBalanceModel(BaseModel):
  class Context(BaseModel):
    slot: int

  context: Context
  value: int


class ProgramAccountsModel(BaseModel):
  class Account(BaseModel):
    lamports: int
    owner: str
    data: list[str]
    executable: bool
    rentEpoch: int
    space: int

  account: Account
  pubkey: str


TProgramAccountsModel = TypeAdapter(list[ProgramAccountsModel])

TMultipleAccountsModel = TypeAdapter(list[AccountInfoModel | None])


class LargestAccountsModel(BaseModel):
  lamports: int
  address: str


TLargestAccountsModel = TypeAdapter(list[LargestAccountsModel])
