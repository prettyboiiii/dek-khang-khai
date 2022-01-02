from src.providers.databases.ponyORM import PonyORMService
from src.services.memberService import MemberService
from datetime import datetime
import logging

m = MemberService()

class General():
    def __init__(self) -> None:
        self.po = PonyORMService()

    def on_ready(self, name) -> None:
        '''
        On bot ready
        '''
        data = {
            "dcId":"d2d2d2",
            "name": "test",
            "balance": 10.00,
            "created_at": datetime.now(),
            "update_at": datetime.now()
        }
        x = m.insert_member(data)
        print(x)
        logging.info('Bot have logged in as {0.user}'.format(name))
