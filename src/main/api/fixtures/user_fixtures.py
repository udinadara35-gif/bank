import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.login_user_request import LoginUserRequest

#Создание банковского аккаунта
@pytest.fixture
def active_account_bank(api_manager):
    generate_user=RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(generate_user)

    login_request = LoginUserRequest(username=generate_user.username, password=generate_user.password)
    api_manager.admin_steps.login_user(login_request)

    account = api_manager.user_steps.create_account(generate_user)

    deposit_request = RandomModelGenerator.generate(DepositAccountRequest)
    deposit_request.accountId = account.id

    yield deposit_request



@pytest.fixture
def transfer_account_bank(api_manager):
    sender_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(sender_request)

    receiver_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(receiver_request)

    login_receiver = LoginUserRequest(username=receiver_request.username, password=receiver_request.password)
    api_manager.admin_steps.login_user(login_receiver)
    account_receiver = api_manager.user_steps.create_account(receiver_request)

    login_sender = LoginUserRequest(username=sender_request.username, password=sender_request.password)
    api_manager.admin_steps.login_user(login_sender)
    account_sender = api_manager.user_steps.create_account(sender_request)


    transfer_request = RandomModelGenerator.generate(TransferAccountRequest)
    transfer_request.fromAccountId = account_sender.id
    transfer_request.toAccountId = account_receiver.id

    deposit_request = RandomModelGenerator.generate(DepositAccountRequest)
    deposit_request.accountId = account_sender.id
    deposit_request.amount = transfer_request.amount + 1000

    api_manager.user_steps.deposit_account(deposit_request)

    yield transfer_request



@pytest.fixture
def credit_bank_account(api_manager, credit_role):
    user = RandomModelGenerator.generate(CreateUserRequest)
    user.role = credit_role
    api_manager.admin_steps.create_user(user)

    login_request = LoginUserRequest(username=user.username, password=user.password)
    api_manager.admin_steps.login_user(login_request)

    u = api_manager.user_steps.create_account(user)

    yield u


@pytest.fixture
def active_credit(api_manager, credit_bank_account):
    credit = api_manager.credit_steps.credit_request(credit_bank_account)
    yield credit