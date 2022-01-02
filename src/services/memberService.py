from src.repositories.memberRepository import MemberRepository
from src.models.Entities import Member
from pony.orm import db_session
from typing import Tuple


class MemberService:
    '''
    for create logic from Member Respository
    '''

    def __init__(self):
        self.member = MemberRepository()

    @db_session
    def insert_member(self, data: dict) -> Tuple[int, Member]:
        '''
        Insert new Member to the dabase
        Member : Member<object>

        return log(Any), result(Any)
        '''
        # modify data
        if "id" in data.keys():
            data.pop('id')
        log, result = self.member.add(data)

        if log is not None:
            return -97678436, log
        return 201, result

    @db_session
    def get_member_by_id(self, id:str) -> Tuple[int, Member]:
        '''
        Get all Member from database

        return log(Any), result(Any)
        '''
        log, result = self.member.get_by_id(id)
        if log == "Not found":
            return 404, log
        if log is not None:
            return 500, log
        return 200, result

    @db_session
    def get_member_by_dcid(self, dcId: str) -> Tuple[int, Member]:
        '''
        Get Member from database by dcId

        return log(Any), result(Any)
        '''
        log, result = self.member.get_by_dcId(dcId)
        if log == "Not found":
            return 404, log
        if log is not None:
            return 500, log
        return 200, result

    @db_session
    def update_member(self, id: str, data: dict) -> Tuple[int, Member]:
        '''
        Update Member that exist in database by specific id from update user data
        id : str
        Member : Member<object>

        return log(Any), result(Any)
        '''
        # modify data
        if "id" in data.keys():
            data.pop("id")
        # check id is exist
        log, result = self.member.update(id, data)
        if log is not None:
            return -97678436, log
        return 204, result

    @db_session
    def delete_member(self, id) -> Tuple[int, str]:
        '''
        Delete Member from database by specific id
        id : str

        return log(Any), result(Any)
        '''
        # check ai config is exist
        log, result = self.member.delete(id)
        if log is not None:
            return -97678436, log
        return 200, result