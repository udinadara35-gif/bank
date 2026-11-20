import pytest
from sqlalchemy.orm import Session
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.classes.api_manager import ApiManager
from src.main.api.specs.response_specs import ResponseSpecs



@pytest.mark.api
class TestCreditUser:
    def test_credit_user_valid(self, db_session: Session , api_manager: ApiManager, credit_bank_account):
        response = api_manager.credit_steps.credit_request(credit_bank_account)

        assert response.id == credit_bank_account.id, 'ID кредитного аакаунта в ответе API при оформлении кредита не совпадает'

        credit_from_db = Credit.get_credit_by_account_id(db_session, credit_bank_account.id)
        assert credit_from_db is not None, 'Созданного кредита нет в БД, ошибка'
        assert credit_from_db.account_id == credit_bank_account.id, 'ID счета в кредите БД не совпадает'
        assert credit_from_db.amount == response.amount, 'Сумма кредита в БД не совпадает'
        assert credit_from_db.balance == -response.amount, 'Остаток долга по кредиту не совпадает в БД'




    @pytest.mark.parametrize(
        "amount, expected_spec, credit_role", [
            (4999,ResponseSpecs.request_bad(),"ROLE_CREDIT_SECRET"),
            (15001,  ResponseSpecs.request_bad(),"ROLE_CREDIT_SECRET"),
            (5500, ResponseSpecs.request_forbidden(),"ROLE_USER")
        ]
    )
    def test_credit_user_invalid(self, db_session: Session ,api_manager: ApiManager, amount, expected_spec, credit_role, credit_bank_account):
        api_manager.credit_steps.credit_request_invalid(credit_bank_account, amount, expected_spec)


        credit_from_db = Credit.get_credit_by_account_id(db_session, credit_bank_account.id)
        assert credit_from_db is None, 'При невалидном запросе кредита в БД создалась запись'
