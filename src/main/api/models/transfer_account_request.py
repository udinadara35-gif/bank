from typing import Annotated

from main.api.generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel



class TransferAccountRequest(BaseModel):
    fromAccountId: int
    toAccountId: int
    amount: Annotated[float, CreationRule(regex=r'^[1-7][0-9]{3}$')]
    