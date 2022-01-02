from pony.orm import commit, db_session
from src.models.Entities import Member
from uuid import UUID


class MemberRepository:
    '''
    MemberRepository
    - to manage, create, update, delete and get Member in database
    '''
    @db_session
    def add(self, data: dict):
        '''
        Insert member to database
        data : Member<dict>

        return log(Any), result(Any)
        '''
        try:
            result = Member(**data)
            commit()
            return None, result.id
        except Exception as e:
            return str(e), None

    @db_session
    def get(self):
        '''
        Get all Member from database

        return log(Any), result(Any)
        '''
        try:
            members = Member.select()
            results = [ member for member in members ]
            return None, results
        except Exception as e:
            return str(e), None

    @db_session
    def get_by_dcId(self, dcId: str):
        '''
        Get Member from database by using dcId
        dcId : str

        return log(Any), result(Any)
        '''
        try:
            result = Member.get(dcId=dcId)
            return None, result
        except Exception as e:
            return str(e), None

    @db_session
    def update(self, id: str, data: dict):
        '''
        update Member object by specific id
        id : str
        data : AIConfig<dict>

        return log(Any), result(Any)
        '''
        try:
            result = Member.get(id=UUID(id))
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
            result = Member.get(id=id)
            result.delete()
            commit()
            return None, id
        except Exception as e:
            return str(e), None
