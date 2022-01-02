from src.utils.configs.app_settings import get_settings
from src.utils.helpers.logging import setup_logging
from src.commands.text2speech import Text2Speech
from src.commands.dataservice import DataService
from src.events.general import General as GE
from discord.ext.commands import Bot

class Bot(Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=get_settings().PREFIX)
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
