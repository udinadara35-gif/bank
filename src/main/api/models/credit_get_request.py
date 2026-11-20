from typing import Annotated

from main.api.generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel


class CreditGetRequest(BaseModel):
    accountId: int
    amount: Annotated[float, CreationRule(regex=r'[5-8][0-9]{3}$')]
    termMonths: Annotated[int, CreationRule(regex=r'^[1-5][0-9]{1}$')]