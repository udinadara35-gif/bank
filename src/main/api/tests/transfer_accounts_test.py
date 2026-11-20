import pytest
from sqlalchemy.orm import Session
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.classes.api_manager import ApiManager



@pytest.mark.api
class TestTransferAccounts:
    def test_transfer_accounts_valid(self, db_session: Session,api_manager: ApiManager, transfer_account_bank):
        response = api_manager.user_steps.transfer_accounts(transfer_account_bank)

        assert response.toAccountId == transfer_account_bank.toAccountId, 'ID аккаунта получателя не совпадает в ответе API '

        sender = Transaction.get_transaction_by_from_account_and_type(db_session, transfer_account_bank.fromAccountId,
                                                                      "transfer")

        assert sender is not None, 'Транзакции transfer нет в БД у отправителя, ошибка'
        assert sender.from_account_id == transfer_account_bank.fromAccountId, 'ID счета отправителя в БД не совпадает, ошибка'
        assert sender.transaction_type == "transfer", 'Неверный тип транзакции, ошибка'
        assert sender.amount == transfer_account_bank.amount, 'Сумма списания в БД не сопадает, ошибка'

        receiver = Transaction.get_transaction_by_to_account_and_type(db_session, transfer_account_bank.toAccountId,
                                                                        transaction_type="transfer")

        assert receiver is not None, 'Транзакции transfer нет в БД у получателя, ошибка'
        assert receiver.to_account_id == transfer_account_bank.toAccountId, 'ID счета получателя в БД не совпадает, ошибка'
        assert receiver.transaction_type == "transfer", 'Неверный тип транзакции, ошибка'
        assert receiver.amount == transfer_account_bank.amount, 'Сумма списания в БД не совпадает'






    @pytest.mark.parametrize(
        "invalid_amount", {
            (450),
            (10500)
        }
    )
    def test_transfer_accounts_invalid(self, db_session: Session ,invalid_amount, api_manager: ApiManager, transfer_account_bank):
        api_manager.user_steps.transfer_accounts_invalid(transfer_account_bank, invalid_amount)

        transaction_from_db = Transaction.get_transaction_by_from_account_and_type(db_session, transfer_account_bank.fromAccountId, transaction_type="transfer")

        assert transaction_from_db is None, 'При невалидном переводе транзакция записалась в БД, ошибка'



