from src.repositories.transactionsRepository import TransactionRepository
from pony.orm import db_session
from uuid import UUID

class TransactionService:
    '''
    for create logic from transaction Respository
    '''

    def __init__(self):
        self.transaction = TransactionRepository()

    @db_session
    def insert_transaction(self, data: dict):
        '''
        Insert new transaction to the dabase
        transaction : transaction<object>transaction

        return log(Any), result(Any)
        '''
        # modify data
        if "id" in data.keys():
            data.pop('id')
        log, result = self.transaction.add(data)

        if log is not None:
            return -97678436, log
        return 201, result

    @db_session
    def get_transaction_by_id(self, id:str):
        '''
        Get all transaction from database

        return log(Any), result(Any)
        '''
        log, result = self.transaction.get_by_id(id)
        if log == "Not found":
            return 404, log
        if log is not None:
            return -97678436, log
        return 200, result

    @db_session
    def get_transaction_by_id(self, id: str):
        '''
        Get transaction from database by dcId

        return log(Any), result(Any)
        '''
        log, result = self.transaction.get_by_dcId(id)
        if log == "Not found":
            return 404, log
        if log is not None:
            return 500, log
        return 200, result

    @db_session
    def get_transaction_by_mid_and_type(self, mid: str, type: str):
        '''
        Get transaction from database by dcId

        return log(Any), result(Any)
        '''
        log, result = self.transaction.get_by_mid_and_type(mid, type)
        if log == "Not found":
            return 404, log
        if log is not None:
            return 500, log
        return 200, result

    @db_session
    def update_transaction(self, id: str, data: dict):
        '''
        Update transaction that exist in database by specific id from update user data
        id : str
        transaction : transaction<object>

        return log(Any), result(Any)
        '''
        # modify data
        data.pop("id")
        # check id is exist
        log, result = self.transaction.update(id, data)
        if log is not None:
            return -97678436, log
        return 204, result

    @db_session
    def delete_transaction(self, id):
        '''
        Delete transaction from database by specific id
        id : str

        return log(Any), result(Any)
        '''
        # check ai config is exist
        log, result = self.transaction.delete(id)
        if log is not None:
            return -97678436, log
        return 200, result
