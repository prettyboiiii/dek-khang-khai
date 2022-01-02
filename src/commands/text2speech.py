from typing import Sized
from src.providers.discord.FFmpegPCMAudio import FFmpegPCMAudio
from src.providers.discord.queue import Queue
from src.commands.general import General
from io import BytesIO
from gtts import gTTS
import discord
import logging

class Text2Speech():
    def __init__(self) -> None:
        self.general = General()
        self.q = Queue()

    async def connect(self, client, contex) -> discord.VoiceClient:
        '''
        Connect to voice channel by using command from General
        '''
        voice = await self.general.connect(client, contex)
        return voice

    async def disconnect(self, client, contex) -> None:
        '''
        Disconnect from voice channel by using command from General
        '''
        await self.general.disconnect(client, contex)

    def __text2spech(self, text) -> BytesIO:
        try:
            # Init buffe
            buffer = BytesIO()
            # Covert text to speech
            t2p = gTTS(text=str(text), lang='th', slow=True)
            # Save sound as buffer
            t2p.write_to_fp(buffer)
            buffer.seek(0)

            return buffer
        except Exception as e:
            logging.error(e)
            return None

    def __play_next(self, voice, source):
        try:
            voice.play(source, after=lambda e: self.__check_queue(voice))
        except Exception as e:
            logging.error(f'Text2speech __play_next error : {e}')
    def __check_queue(self, voice):
        try:
            if self.q.size() > 0:
                self.__play_next(voice, self.q.dequeue())
        
        except Exception as e:
            logging.error(f'Text2speech __check_queue error : {e}')

    async def play(self, client, contex) -> None:
        '''
        Speech from text
        '''
        try:
            vip_list = {
                "Rung69#5581": "นิว",
                "Lamron#9045": "หมิว"
            }
            # Get text from message
            text = contex.message.content.split(" ")
            text.pop(0)
            text = " ".join(text)

            if "เต้" in text:
                text = "เต้สุดเท่ และ หล่อ"
            
            if str(contex.message.author) in vip_list.keys():
                text = f'{vip_list[str(contex.message.author)]}กระจอก'

            # Connect to voice channel
            voice = await self.connect(client, contex)
            if voice is None:
                return None

            # Covert text to speech
            buffer = self.__text2spech(text)
            if buffer is None:
                return None

            # Play sound from buffer
            source = FFmpegPCMAudio(buffer.read(), pipe = True)
            if not voice.is_playing():
                self.__play_next(voice, source)
            else:
                self.q.enqueue(source)

            await contex.message.delete(delay=5)
        except Exception as e:
            logging.error(f'Text2speech play error : {e}')