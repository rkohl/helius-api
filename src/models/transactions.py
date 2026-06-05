from typing import Any
from pydantic import BaseModel, TypeAdapter


class TransactionModel(BaseModel):
  slot: int
  blockTime: int | None = None
  transaction: Any
  meta: Any | None = None
  version: Any | None = None


class SignatureInfoModel(BaseModel):
  signature: str
  slot: int
  err: Any | None = None
  memo: str | None = None
  blockTime: int | None = None
  confirmationStatus: str | None = None


TSignaturesForAddressModel = TypeAdapter(list[SignatureInfoModel])


class TransactionsForAddressSignatureModel(BaseModel):
  signature: str
  slot: int
  transactionIndex: int | None = None
  err: Any | None = None
  memo: str | None = None
  blockTime: int | None = None
  confirmationStatus: str | None = None


class TransactionsForAddressModel(BaseModel):
  data: list[Any]
  paginationToken: str | None = None


class TransferModel(BaseModel):
  signature: str
  slot: int
  blockTime: int | None = None
  type: str
  fromUserAccount: str | None = None
  toUserAccount: str | None = None
  fromTokenAccount: str | None = None
  toTokenAccount: str | None = None
  mint: str | None = None
  amount: str
  decimals: int
  uiAmount: str | None = None
  confirmationStatus: str | None = None
  transactionIdx: int | None = None
  instructionIdx: int | None = None
  innerInstructionIdx: int | None = None


class TransfersByAddressModel(BaseModel):
  data: list[TransferModel]
  paginationToken: str | None = None


class SignatureStatusModel(BaseModel):
  slot: int
  confirmations: int | None = None
  err: Any | None = None
  confirmationStatus: str | None = None


TSignatureStatusesModel = TypeAdapter(list[SignatureStatusModel | None])


class SimulateTransactionModel(BaseModel):
  err: Any | None = None
  logs: list[str] | None = None
  accounts: list[Any] | None = None
  unitsConsumed: int | None = None
  returnData: Any | None = None
