from typing import List, Any
from main.api.steps.credit_steps import CreditSteps
from src.main.api.steps.user_steps import UserSteps
from main.api.steps.admin_steps import AdminSteps


class ApiManager:
    def __init__(self, created_obj: List[Any]):
        self.created_obj = created_obj
        self.admin_steps = AdminSteps(created_obj)
        self.user_steps = UserSteps(created_obj)
        self.credit_steps = CreditSteps(created_obj)


def create_user(create_user_request):
    return None


def admin_steps():
    return None


def credit_steps():
    return None