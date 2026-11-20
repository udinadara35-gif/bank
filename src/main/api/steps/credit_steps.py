from main.api.foundation.endpoint import Endpoint
from main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from main.api.generators.model_generator import RandomModelGenerator
from main.api.models.credit_get_request import CreditGetRequest
from main.api.models.credit_get_response import CreditGetResponse
from main.api.models.repay_credit_request import RepayCreditRequest
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.response_specs import ResponseSpecs
from main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.steps.base_steps import BaseSteps
import random




class CreditSteps(BaseSteps):
    def credit_request(self, credit_bank_account):

        request_data = RandomModelGenerator.generate(CreditGetRequest)
        request_data.accountId = credit_bank_account.id
        request_data.amount = round(random.uniform(5000, 15000), 2)

        response = ValidateCrudRequester(
            RequestSpecs.get_auth_headers(),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_created()
        ).post(request_data)
        return response

    def credit_request_invalid(self, credit_bank_account, amount: float, response_specs):
        request_data = RandomModelGenerator.generate(CreditGetRequest)
        request_data.accountId = credit_bank_account.id
        request_data.amount = amount

        CrudRequester(
            RequestSpecs.get_auth_headers(),
            Endpoint.CREDIT_REQUEST,
            response_specs,
        ).post(request_data)

    def repay_credit(self, credit: CreditGetResponse):
        request_data = RandomModelGenerator.generate(RepayCreditRequest)
        request_data.creditId = credit.creditId
        request_data.accountId = credit.id
        request_data.amount = credit.amount

        response = ValidateCrudRequester(
            RequestSpecs.get_auth_headers(),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok()
        ).post(request_data)
        return response

    def repay_credit_invalid(self, credit: CreditGetResponse, amount: float, response_specs):
        request_data = RandomModelGenerator.generate(RepayCreditRequest)
        request_data.creditId = credit.creditId
        request_data.accountId = credit.id
        request_data.amount = amount

        CrudRequester(
            RequestSpecs.get_auth_headers(),
            Endpoint.CREDIT_REPAY,
            response_specs,
        ).post(request_data)
