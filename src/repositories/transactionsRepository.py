from pony.orm import commit, db_session, rollback, desc
from src.models.Entities import Transaction
from uuid import UUID
from typing import Tuple


class TransactionRepository:
    '''
    TransactionRepository
    - to manage, create, update, delete and get Transaction in database
    '''
    @db_session
    def add(self, data: dict):
        '''
        Insert Transaction to database
        data : Transaction<dict>

        return log(Any), result(Any)
        '''
        try:
            result = Transaction(**data)
            commit()
            return None, result
        except Exception as e:
            rollback()
            return str(e), None

    @db_session
    def get_by_id(self, id:str) -> Tuple[Transaction]:
        '''
        Get all Transaction from database

        return log(Any), result(Any)
        '''
        try:
            results = Transaction.select(id=id)
            if results is None:
                return "Not found", None
            return None, results
        except Exception as e:
            rollback()
            return str(e), None

    def get_by_mid_and_type(self, mid:str, type: str) -> Tuple[Transaction]:
        '''
        Get Transaction from database by mid and type ,also include order by create at

        return log(Any), result(Any)
        '''
        try:
            results = Transaction.select(mid=mid, type=type)
            if len(list(results)) == 0:
                return "Not found", None
            return None, list(results.order_by(desc(Transaction.created_at))[:1])
        except Exception as e:
            rollback()
            return str(e), None

    @db_session
    def update(self, id: str, data: dict):
        '''
        update Transaction object by id
        id : str
        data : AIConfig<dict>

        return log(Any), result(Any)
        '''
        try:
            result = Transaction.get(id=id)
            result.set(**data)
            commit()
            return None, result
        except Exception as e:
            rollback()
            return str(e), None

    @db_session
    def delete(self, id: str):
        '''
        delete Transaction object by id
        id : str

        return log(Any), result(Any)
        '''
        try:
            result = Transaction.get(id=id)
            result.delete()
            commit()
            return None, id
        except Exception as e:
            rollback()
            return str(e), None
