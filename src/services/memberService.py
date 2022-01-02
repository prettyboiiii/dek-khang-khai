from src.repositories.memberRepository import MemberRepository
from pony.orm import db_session


class MemberService:
    '''
    for create logic from Member Respository
    '''

    def __init__(self):
        self.member = MemberRepository()

    @db_session
    def insert_member(self, data: dict):
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
    def get_member(self):
        '''
        Get all Member from database

        return log(Any), result(Any)
        '''
        log, result = self.member.get()
        if log is not None:
            return -97678436, log
        return 200, result

    @db_session
    def get_member_by_dcid(self, dcId: str):
        '''
        Get Member from database by dcId

        return log(Any), result(Any)
        '''
        log, result = self.member.get_by_dcId(dcId)
        if log is not None:
            return 500, log
        return 200, result

    @db_session
    def update_member(self, id: str, data: dict):
        '''
        Update Member that exist in database by specific id from update user data
        id : str
        Member : Member<object>

        return log(Any), result(Any)
        '''
        # modify data
        data.pop("id")
        # check id is exist
        log, result = self.member.update(id, data)
        if log is not None:
            return -97678436, log
        return 204, result

    @db_session
    def delete_member(self, id):
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
