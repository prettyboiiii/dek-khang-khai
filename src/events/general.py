from src.providers.databases.ponyORM import PonyORMService
from src.services.memberService import MemberService
import logging

m = MemberService()

class General():
    def __init__(self) -> None:
        self.po = PonyORMService()

    def on_ready(self, name) -> None:
        '''
        On bot ready
        '''
        logging.info('Bot have logged in as {0.user}'.format(name))
