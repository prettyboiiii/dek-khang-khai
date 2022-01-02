from pony.orm import commit, db_session
from src.models.Entities import Transaction
from uuid import UUID


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
            return None, result.id
        except Exception as e:
            return str(e), None

    @db_session
    def get(self):
        '''
        Get all Transaction from database

        return log(Any), result(Any)
        '''
        try:
            Transactions = Transaction.select()
            results = [ Transaction for Transaction in Transactions ]
            return None, results
        except Exception as e:
            return str(e), None

    @db_session
    def get_by_dcId(self, dcId: str):
        '''
        Get Transaction from database by using dcId
        dcId : str

        return log(Any), result(Any)
        '''
        try:
            result = Transaction.get(dcId=dcId)
            return None, result
        except Exception as e:
            return str(e), None

    @db_session
    def update(self, id: str, data: dict):
        '''
        update Transaction object by specific id
        id : str
        data : AIConfig<dict>

        return log(Any), result(Any)
        '''
        try:
            result = Transaction.get(id=UUID(id))
            result.set(**data)
            commit()
            return None, result.id

        except Exception as e:
            return str(e), None

    @db_session
    def delete(self, id: str):
        '''
        delete ai_config object by id
        id : str

        return log(Any), result(Any)
        '''
        try:
            result = Transaction.get(id=id)
            result.delete()
            commit()
            return None, id
        except Exception as e:
            return str(e), None
