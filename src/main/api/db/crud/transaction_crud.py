from sqlalchemy.orm import Session
from src.main.api.db.models.transaction_table import Transaction


class TransactionCrudDb:
    #Для депозита и получения перевода (деньги пришла на счет)
    @staticmethod
    def get_transaction_by_to_account_and_amount(db: Session, account_id: int, amount: float) -> Transaction | None:
        return db.query(Transaction).filter_by(to_account_id=account_id, amount=amount).first()

    #Для отправки перевода и погашения кредита (деньги ушли со счета)
    @staticmethod
    def get_transaction_by_from_account_id(db: Session, account_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(from_account_id=account_id).first()

    # Для поиска депозита и входящего перевода (transfer_in)
    @staticmethod
    def get_transaction_by_to_account_and_type(db: Session, account_id: int, transaction_type: str) -> Transaction | None:
        return db.query(Transaction).filter_by(to_account_id=account_id, transaction_type=transaction_type).first()

    # Для поиска исходящего первода (transfer_out)
    @staticmethod
    def get_transaction_by_from_account_and_type(db: Session, account_id: int,transaction_type: str) -> Transaction | None:
        return db.query(Transaction).filter_by(from_account_id=account_id, transaction_type=transaction_type).first()

    # Найти крединтую транзакцию по credit_id
    @staticmethod
    def get_transaction_by_credit_id(db: Session, credit_id: int) -> Transaction| None:
        return db.query(Transaction).filter_by(credit_id=credit_id).first()