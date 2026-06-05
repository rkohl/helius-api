from typing import Any
from pydantic import BaseModel


class ErrorModel(BaseModel):
  code: int
  message: str
  data: Any | None = None
