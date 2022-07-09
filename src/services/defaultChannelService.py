from src.repositories.defaultChannelRepository import DefaultChannelRepository
from src.models.Entities import DefaultChannel
from pony.orm import db_session
from typing import Tuple


class DefaultChannelService:
    '''
    for create logic from DefaultChannel Respository
    '''

    def __init__(self):
        self.defaultChannel = DefaultChannelRepository()

    @db_session
    def insert_defaultChannel(self, data: dict) -> Tuple[int, DefaultChannel]:
        '''
        Insert new DefaultChannel to the dabase
        DefaultChannel : DefaultChannel<object>

        return log(Any), result(Any)
        '''
        log, result = self.defaultChannel.add(data)

        if log is not None:
            return -97678436, log
        return 201, result

    @db_session
    def get_defaultChannel_by_id(self, id:str) -> Tuple[int, DefaultChannel]:
        '''
        Get One DefaultChannel from database

        return log(Any), result(Any)
        '''
        log, result = self.defaultChannel.get_by_id(id)
        if log == "Not found":
            return 404, log
        if log is not None:
            return 500, log
        return 200, result
    
    @db_session
    def update_defaultChannel(self, id: str, data: dict) -> Tuple[int, DefaultChannel]:
        '''
        Update DefaultChannel that exist in database by specific id from update user data
        id : str
        DefaultChannel : DefaultChannel<object>

        return log(Any), result(Any)
        '''
        # modify data
        if "id" in data.keys():
            data.pop("id")
        # check id is exist
        log, result = self.defaultChannel.update(id, data)
        if log is not None:
            return -97678436, log
        return 204, result

    @db_session
    def delete_defaultChannel(self, id) -> Tuple[int, str]:
        '''
        Delete DefaultChannel from database by specific id
        id : str

        return log(Any), result(Any)
        '''
        # check ai config is exist
        log, result = self.defaultChannel.delete(id)
        if log is not None:
            return -97678436, log
        return 200, result