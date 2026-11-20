import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


class TestRepayCreditUser:
    def test_repay_credit_user_valid(self, db_session: Session ,api_manager: ApiManager, active_credit):
        response = api_manager.credit_steps.repay_credit(active_credit)

        assert response.creditId == active_credit.creditId, 'ID кредита в ответе API при погашении не совпадает'

        credit_from_db = Credit.get_credit_by_id(db_session, active_credit.creditId)
        assert credit_from_db is not None, 'Кредит не найден в БД'
        assert credit_from_db.balance == 0.0, 'После полного погашения остаток долга в БД должен быть 0.0'

        transaction_from_db = Transaction.get_transaction_by_credit_id(db_session, active_credit.creditId)
        assert transaction_from_db is not None, 'Транзакции погашения кредита нет в БД'
        assert transaction_from_db.credit_id == active_credit.creditId, 'ID  кредита нет в БД'
        assert transaction_from_db.amount == active_credit.amount, 'Сумма погашения в транзакции БД не совпадает'




    @pytest.mark.parametrize(
        "amount, expected_spec",[
            (5600, ResponseSpecs.request_unprocessable()),
            (500, ResponseSpecs.request_unprocessable())
        ]
    )
    def test_repay_credit_user_invalid(self, db_session: Session, api_manager: ApiManager, active_credit, amount, expected_spec):
        api_manager.credit_steps.repay_credit_invalid(active_credit, amount, expected_spec)

        credit_from_db = Credit.get_credit_by_id(db_session, active_credit.creditId)
        assert credit_from_db.balance != 0.0, 'При невалидном погашении остаток долга в БД изменился'