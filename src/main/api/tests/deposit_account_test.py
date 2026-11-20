import pytest
from requests import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


@pytest.mark.api
class TestDepositAccount:
    def test_deposit_account_valid(self, db_session: Session, api_manager: ApiManager, active_account_bank):
        response = api_manager.user_steps.deposit_account(active_account_bank)

        assert response.id == active_account_bank.accountId, 'ID счета в ответе API не совпадает'
        assert response.balance == active_account_bank.amount, 'Баланс на аккаунте в ответе API не совпадет с суммой депозита'

        transaction_from_db = Transaction.get_transaction_by_to_account_and_type(db_session, active_account_bank.accountId, "deposit")
        assert transaction_from_db is not None, 'Транзакции депозита нет в БД'
        assert transaction_from_db.to_account_id == active_account_bank.accountId, 'ID счета в транзакции БД не совпадает'
        assert transaction_from_db.transaction_type == "deposit", 'Неверный тип транзакции в БД'
        assert transaction_from_db.amount == active_account_bank.amount, 'Сумма транзакции в БД не совпадает'



    @pytest.mark.parametrize(
        "amount", {
            (999),
            (9001)
        }
    )
    def test_deposit_account_invalid(self, db_session: Session, amount,api_manager: ApiManager, active_account_bank):
       api_manager.user_steps.deposit_account_invalid(active_account_bank, amount)

       transaction_from_db = Transaction.get_transaction_by_to_account_and_amount(db_session, active_account_bank.accountId, amount)
       assert transaction_from_db is None, 'Транзакция с невалидным депозитом записалась в БД, ошибка'