from pony.orm import commit, db_session, rollback
from src.models.Entities import Member
from typing import Tuple


class MemberRepository:
    '''
    MemberRepository
    - to manage, create, update, delete and get Member in database
    '''
    @db_session
    def add(self, data: dict) -> Tuple[str, Member]:
        '''
        Insert member to database
        data : Member<dict>

        return log(Any), result(Any)
        '''
        try:
            result = Member(**data)
            commit()
            return None, result
        except Exception as e:
            rollback()
            return str(e), None

    @db_session
    def get_by_id(self, id: str) -> Tuple[str, Member]:
        '''
        Get all Member from database

        return log(Any), result(Any)
        '''
        try:
            results = Member.select(id=id)
            if len(list(results)) == 0:
                return "Not found", None
            return None, list(results)[0]
        except Exception as e:
            rollback()
            return str(e), None

    @db_session
    def get_by_dcId(self, dcId: str) -> Tuple[str, Member]:
        '''
        Get Member from database by using dcId
        dcId : str

        return log(Any), result(Any)
        '''
        try:
            results = Member.get(dcId=dcId)
            if results is None:
                return "Not found", None
            return None, results
        except Exception as e:
            rollback()
            return str(e), None

    @db_session
    def update(self, id: str, data: dict) -> Tuple[str, Member]:
        '''
        update Member object by specific id
        id : str
        data : AIConfig<dict>

        return log(Any), result(Any)
        '''
        try:
            result: Member = Member.get(id=id)
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
            result: Member = Member.get(id=id)
            result.delete()
            commit()
            return None, id
        except Exception as e:
            rollback()
            return str(e), None
