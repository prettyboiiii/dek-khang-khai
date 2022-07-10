from gtts import gTTS
from io import BytesIO
from src.commands.dataservice import DataService
from src.commands.general import General
from src.models.TransactionType import TransactionType
from src.providers.discord.FFmpegPCMAudio import FFmpegPCMAudio
from src.providers.queue.queue import Queue
from src.services.memberService import MemberService
from src.utils.configs.app_settings import get_settings
from src.utils.constants.constants import VIP_LIST, PASS_LIST, SPECIAL_WORD
import discord
import logging
import re

class Text2Speech():
    def __init__(self) -> None:
        self.general = General()
        self.q = Queue()
        self.member = MemberService()
        self.ds = DataService()

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
            # Init buffer
            buffer = BytesIO()
            # Covert text to speech
            t2p = gTTS(text=str(text), lang='th', slow=True)
            # Save sound as buffer
            t2p.write_to_fp(buffer)
            buffer.seek(0)

            return buffer
        except Exception as e:
            logging.error(f'[Text2Speech.__text2spech] : {e}')
            return None

    def __play_next(self, voice, source):
        try:
            # Play sound
            voice.play(discord.FFmpegPCMAudio(source="./src/utils/constants/noti_sound.mp3"), 
                        after=lambda e: voice.play(source, after=lambda e: self.__check_queue(voice)))
        except Exception as e:
            logging.error(f'[Text2Speech.__play_next] : {e}')

    def __check_queue(self, voice):
        '''
        Check queue is empty or not
        '''
        try:
            # If queue is not empty play next queue
            if self.q.size() > 0:
                self.__play_next(voice, self.q.dequeue())
        
        except Exception as e:
            logging.error(f'[Text2Speech.__check_queue] : {e}')

    async def play(self, client, contex) -> None:
        '''
        Command bot to speech from text
        '''
        author = contex.author
        dcId = str(author._user.id)
        name = author._user.name
        try:
            # Get text from message
            text = contex.message.content.split(" ")
            text.pop(0)
            text = " ".join(text)
            # check if there is member tag in text
            mentions = contex.message.mentions
            # replace member tag to empty string
            text = re.sub(r'<@!\d+>', "", text)

            for key, value in PASS_LIST.items():
                if key in text.lower():
                    text = value
            
            if str(contex.message.author) in VIP_LIST.keys():
                text = f'{VIP_LIST[str(contex.message.author)]}{SPECIAL_WORD}'

            # Calculate the amount of text
            len_text = len(text)
            amount = round(get_settings().PRICE * len_text, 6)
            member = await self.ds.createOrUpdateMember(contex, dcId, name)
            
            # donate more than balance of member
            if member.balance < amount:
                await contex.message.delete(delay=20)
                await contex.send("<@{}> คุณไม่มีเหรียญที่จะโดเนท".format(dcId), delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                return
            
            else:
                # Connect to voice channel
                voice = await self.connect(client, contex)
                if voice is None:
                    return None
                await contex.send("<@{}> ได้โดเนทเป็นจำนวน *{}* **{}**".format(dcId, amount, get_settings().COIN_NAME), delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                await self.ds.insertNewTransaction(contex, member.dcId, TransactionType.DONATE.name, -1*amount, contributor=None)
            
            member_list = []
            member_temp = []
            if len(mentions) == 0:
                # Get all id of member in voice channel
                member_list = voice.channel.members
                member_list = [member for member in member_list if str(member.id) != dcId and member.bot == False]
            else:
                member_list = mentions
                text = "โดเนทให้กับ " + ", ".join([member.nick if member.nick is not None else member.name for member in mentions]) + " ว่า " + text

            for member in member_list:
                log, result = self.member.get_member_by_dcid(str(member.id))
                if log not in [404, 500]:
                    member_temp.append(result)
            
            if len(member_temp) > 0:
                seperatedAmount = amount / len(member_temp)
                for receiver_member in member_temp:
                    await self.ds.insertNewTransaction(contex, dcId, TransactionType.DONATE.name, seperatedAmount, contributor=receiver_member)

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
            logging.error(f'[Text2Speech.play] : {e}')