import discord
import logging

class General():

    async def connect(self, client, contex) -> discord.VoiceClient:
        '''
        Command bot to connect to author voice channel
        '''
        try:
            channel = contex.message.author.voice.channel
            # If Auhtor is not on voice channel
            if not channel:
                await contex.send("You are not connected to a voice channel")
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