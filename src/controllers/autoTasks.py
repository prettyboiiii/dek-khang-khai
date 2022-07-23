from discord import VoiceClient
from discord.ext import tasks
from src.commands.general import General
from src.utils.configs.app_settings import get_settings

class AutoTasks():
    def __init__(self, bot) -> None:
        self.general = General()
        self.bot = bot
        self.vc: VoiceClient = None

    async def setCountdownDisconnect(self, vc: VoiceClient):
        self.vc = vc
        if (self.countingDown.is_running()):
            self.countingDown.restart()
        else:
            self.countingDown.start()

    @tasks.loop(minutes=get_settings().AUTO_DISCONNECT_MINUTES)
    async def countingDown(self):
        self.countingDown.stop()
    
    @countingDown.before_loop
    async def beforeCountingDown(self):
        await self.bot.wait_until_ready()

    @countingDown.after_loop
    async def autoDisconnect(self):
        if self.countingDown.is_being_cancelled():
            return

        self.vc = await self.vc.disconnect()
