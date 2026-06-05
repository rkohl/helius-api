from typing import Any
from pydantic import BaseModel, TypeAdapter


class TokenAmountModel(BaseModel):
  amount: str
  decimals: int
  uiAmount: float | None = None
  uiAmountString: str

class TokenAccountModel(BaseModel):
  class Account(BaseModel):
    lamports: int
    owner: str
    data: Any
    executable: bool
    rentEpoch: int
    space: int | None = None

  account: Account
  pubkey: str

TTokenAccountsModel = TypeAdapter(list[TokenAccountModel])

class TokenLargestAccountModel(BaseModel):
  address: str
  amount: str
  decimals: int
  uiAmount: float | None = None
  uiAmountString: str

TTokenLargestAccountsModel = TypeAdapter(list[TokenLargestAccountModel])
