from src.commands.dataservice import DataService
from src.utils.configs.app_settings import get_settings
import discord
import logging

class General():
    def __init__(self) -> None:
        self.ds = DataService()

    async def connect(self, client, contex) -> discord.VoiceClient:
        '''
        Command bot to connect to author voice channel
        '''
        try:
            channel = contex.message.author.voice.channel
            # If Auhtor is not on voice channel
            if not channel:
                await contex.send("You are not connected to a voice channel", delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                return
            # Connet bot to voice channel
            voice = discord.utils.get(client.voice_clients, guild=contex.guild)
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                logging.info("Connect to {} voice channel".format(channel))
                voice = await channel.connect()
            
            return voice
        except Exception as e:
            logging.error(f'[General.connect] : {e}')
            return None

    async def disconnect(self, client, contex) -> None:
        '''
        Command bot to disconnet from author voice channel
        '''
        try:
            voiceClient = discord.utils.get(client.voice_clients, guild=contex.guild)
            await voiceClient.disconnect()
            logging.info("Disconnet from {} voice channel".format(contex.message.author.voice.channel))
        except Exception as e:
            logging.error(f'[General.disconnect] : {e}')
            
    async def sendMessageToDefaultChannels(self, client: discord.Client, message: str, delete_after: bool = False):
        for guild in client.guilds:
            default_channel = await self.ds.getDefaultChannelByGuildId(guild, str(guild.id))
            if (delete_after):
                await default_channel.send(message, delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
            else:
                await default_channel.send(message)
            