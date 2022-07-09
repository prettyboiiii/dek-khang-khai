from decimal import Decimal
from src.utils.configs.app_settings import get_settings
from src.utils.helpers.logging import setup_logging
from src.commands.text2speech import Text2Speech
from src.commands.dataservice import DataService
from src.events.general import General as GE
from discord.ext.commands import Bot
import discord
import logging

intents = discord.Intents.default()
intents.members = True

class Bot(Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=get_settings().PREFIX, intents=intents)
        self.ge = GE()
        self.t2p = Text2Speech()
        self.ds = DataService()
        self.add_commands()

    async def on_ready(self):
        setup_logging()
        self.ge.on_ready(self)
    
    def add_commands(self):
        @self.command(name="p", pass_context=True)
        async def text2speech(contex):
            await self.t2p.play(self, contex)

        @self.command(pass_context=True)
        async def connect(contex):
            await self.t2p.connect(self, contex)
        
        @self.command(pass_context=True)
        async def disconnect(contex):
            await self.t2p.disconnect(self, contex)
        
        @self.command(pass_context=True)
        async def register(contex):
            await self.ds.register(contex)

        @self.command(pass_context=True)
        async def daily(contex):
            await self.ds.daily(contex)

        @self.command(pass_context=True)
        async def check(contex):
            await self.ds.check(contex)

        @self.command(pass_context=True)
        async def send(contex, receiver: discord.User, amount):
            try:
                Decimal(amount)
                await self.ds.send(contex, receiver, Decimal(amount))
            except ValueError:
                await contex.send("<@{}> ใส่ค่าจำนวนเงินที่ส่งเป็นเลขจำนวนจริง และ ต้องมากว่า 0.00"
                                    .format(str(contex.author._user.id)), 
                                    delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                return 
            except Exception as e:
                logging.error(f'[Bot.send] : {e}')
                await contex.send("<@{}> คำสั่งเกิดข้อผิดพลาดกรุณาใส่ .send @[ผู้รับเงิน] [จำนวนเงินที่ให้ (เลขจำนวนจริงที่มากว่า 0)]"
                                    .format(str(contex.author._user.id)), 
                                    delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                return 

        @self.command(pass_context=True)
        async def bet(contex, amount):
            try:
                Decimal(amount)
                await self.ds.bet(contex, Decimal(amount))
            except ValueError:
                await contex.send("<@{}> ใส่ค่าเดิมพันเป็นเลขจำนวนจริง และ ต้องมากว่า 0.00"
                                    .format(str(contex.author._user.id)), 
                                    delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                return 

            except Exception as e:
                logging.error(f'[Bot.bet] : {e}')
                await contex.send("<@{}> คำสั่งเกิดข้อผิดพลาดกรุณาใส่ .bet [เงินเดิมพัน (เลขจำนวนจริงที่มากว่า 0)]"
                                    .format(str(contex.author._user.id)), 
                                    delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                return 

        @self.command(pass_context=True)
        async def hourly(contex):
            await self.ds.hourly(contex)

