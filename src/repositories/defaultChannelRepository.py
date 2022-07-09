from pony.orm import commit, db_session, rollback
from src.models.Entities import DefaultChannel
from typing import Tuple


class DefaultChannelRepository:
    '''
    DefaultChannelRepository
    - to manage, create, update, delete and get DefaultChannel in database
    '''
    @db_session
    def add(self, data: dict) -> Tuple[str, DefaultChannel]:
        '''
        Insert defaultChannel to database
        data : DefaultChannel<dict>

        return log(Any), result(Any)
        '''
        try:
            result = DefaultChannel(**data)
            commit()
            return None, result
        except Exception as e:
            rollback()
            return str(e), None

    @db_session
    def get_by_id(self, id: str) -> Tuple[str, DefaultChannel]:
        '''
        Get all DefaultChannel from database

        return log(Any), result(Any)
        '''
        try:
            results = DefaultChannel.select(id=id)
            if len(list(results)) == 0:
                return "Not found", None
            return None, list(results)[0]
        except Exception as e:
            rollback()
            return str(e), None

    @db_session
    def update(self, id: str, data: dict) -> Tuple[str, DefaultChannel]:
        '''
        update DefaultChannel object by specific id
        id : str
        data : AIConfig<dict>

        return log(Any), result(Any)
        '''
        try:
            result: DefaultChannel = DefaultChannel.get(id=id)
            result.set(**data)
            commit()
            return None, result
        except Exception as e:
            rollback()
            return str(e), None

    @db_session
    def delete(self, id: str) -> Tuple[str, str]:
        '''
        delete ai_config object by id
        id : str

        return log(Any), result(Any)
        '''
        try:
            result: DefaultChannel = DefaultChannel.get(id=id)
            result.delete()
            commit()
            return None, id
        except Exception as e:
            rollback()
            return str(e), None
