from main.api.foundation.endpoint import Endpoint
from main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from main.api.generators.model_generator import RandomModelGenerator
from main.api.models.create_user_request import CreateUserRequest
from main.api.models.deposit_account_request import DepositAccountRequest
from main.api.models.transfer_account_request import TransferAccountRequest
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.response_specs import ResponseSpecs
from main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response

    def deposit_account(self, deposit_account_request: DepositAccountRequest):

        response = ValidateCrudRequester(
            RequestSpecs.get_auth_headers(),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(deposit_account_request)
        return response

    def deposit_account_invalid(self,deposit_request, amount: float=None):
        request_data = RandomModelGenerator.generate(DepositAccountRequest)
        request_data.accountId = deposit_request.accountId

        if amount is not None:
            request_data.amount = amount

        CrudRequester(
            RequestSpecs.get_auth_headers(),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_bad()
        ).post(request_data)

    def transfer_accounts(self, transfer_account_request: TransferAccountRequest):

        response = ValidateCrudRequester(
            RequestSpecs.get_auth_headers(),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(transfer_account_request)
        return response


    def transfer_accounts_invalid(self, transfer_account_request: TransferAccountRequest, amount: float=None):

        if amount is not None:
            transfer_account_request.amount = amount

        CrudRequester(
            RequestSpecs.get_auth_headers(),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_bad()
        ).post(transfer_account_request)


