from typing import Protocol
from typing import Optional
from main.api.models.base_model import BaseModel
from requests import Response



#проверка типов
class CrudEndpoint(Protocol):
    def post(self, model: Optional[BaseModel]) -> BaseModel | Response:...
    def get(self, user_id: int) -> BaseModel | Response:...
    def delete(self, user_id: int) -> BaseModel | Response:...

