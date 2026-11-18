from typing import Annotated

from main.api.generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel


class DepositAccountRequest(BaseModel):
    accountId: int
    amount: Annotated[float,CreationRule(regex=r'^[1-8][0-9]{3}$')]
