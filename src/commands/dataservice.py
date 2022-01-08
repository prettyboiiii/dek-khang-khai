from src.services.transactionService import TransactionService
from src.utils.configs.app_settings import get_settings
from src.models.TransactionType import TransactionType
from src.services.memberService import MemberService
from datetime import datetime, timedelta
from decimal import Decimal, getcontext
import logging
import random
import discord

getcontext().prec = 6

class DataService():
    def __init__(self) -> None:
        self.member = MemberService()
        self.transaction = TransactionService()

    async def __createOrUpdateMember(self, contex, dcId, name):
        '''
        Create new member if not exit and update member name
        '''
        try:
            member = ""
            # Get member by dcId
            statusCode, getResult = self.member.get_member_by_dcid(dcId)
            # If Error
            if statusCode not in [200, 404]:
                logging.error(f'[DataService.__createOrUpdateMember] Query member : {getResult}')
                await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId)
                                                                    , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                return 

            # Get id from member
            if statusCode != 404:
                member = getResult

            # Insert new member if not found
            if statusCode == 404:
                data = {
                    "dcId":dcId,
                    "name": name,
                    "balance": 0.00,
                }
                statusCode, insertResult = self.member.insert_member(data)
            
                # If Error
                if statusCode not in [201]:
                    logging.error(f'[DataService.__createOrUpdateMember] Insert member : {insertResult}')
                    await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId)
                                                                    , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                    return 

                await contex.send("<@{}> คุณได้เปิดบัญชีเรียบร้อยแล้ว".format(dcId)
                                                                    , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                # Get id from member
                member = insertResult

            # Update name
            elif getResult.name != name:
                data = {
                    "name": name,
                    "update_at": datetime.utcnow()
                }
                statusCode, updateResult = self.member.update_member(getResult[0].id, data)

                # If Error
                if statusCode not in [204]:
                    logging.error(f'[DataService.__createOrUpdateMember] Update member : {updateResult}')
                    await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId)
                                                                    , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                    return

                member = updateResult
            
            return member
        except Exception as e:
            logging.error(f'[DataService.__createOrUpdateMember] : {e}')
            await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId)
                                                            , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
            return

    async def __insertNewTransaction(self, contex, dcId, type, amount, contributor=None):
        '''
        Insert trasaction
        '''
        try:
            # Get member by dcId
            statusCode, result = self.member.get_member_by_dcid(dcId)
            # If Error
            if statusCode not in [200, 404]:
                logging.error(f'[DataService.__insertNewTransaction] Query member : {result}')
                await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId)
                                                                    , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                return 

            if contributor is None:

                data = {
                    "mid": result.id,
                    "type": type,
                    "amount": amount,
                    "contributor": contributor,
                }

                statusCode, insertResult = self.transaction.insert_transaction(data)
                # If Error
                if statusCode not in [201]:
                    logging.error(f'[DataService.__insertNewTransaction] Insert transaction : {insertResult}')
                    await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId)
                                                                        , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                    return

                data = {
                    "balance": result.balance + Decimal(amount),
                    "update_at": datetime.utcnow()
                }

                statusCode, updateResult = self.member.update_member(result.id, data)
                # If Error
                if statusCode not in [204]:
                    logging.error(f'[DataService.__insertNewTransaction] Update member : {updateResult}')
                    await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId)
                                                                    , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                    return
        
            else:
                # Create transaction
                data = {
                    "mid": result.id,
                    "type": type,
                    "amount": amount,
                    "contributor": contributor.id,
                }

                statusCode, insertResult = self.transaction.insert_transaction(data)
                # If Error
                if statusCode not in [201]:
                    logging.error(f'[DataService.__insertNewTransaction] Insert transaction : {insertResult}')
                    await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId)
                                                                        , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                    return

                # Sender
                data = {
                    "balance": result.balance - Decimal(amount),
                    "update_at": datetime.utcnow()
                }

                statusCode, updateResult = self.member.update_member(result.id, data)
                # If Error
                if statusCode not in [204]:
                    logging.error(f'[DataService.__insertNewTransaction] Update member : {updateResult}')
                    await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId)
                                                                    , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                    return

                # Receiver
                # Get member by dcId
                statusCode, result = self.member.get_member_by_dcid(contributor.dcId)
                # If Error
                if statusCode not in [200, 404]:
                    logging.error(f'[DataService.__insertNewTransaction] Query member : {result}')
                    await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId)
                                                                    , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                    return 

                data = {
                    "balance": result.balance + Decimal(amount),
                    "update_at": datetime.utcnow()
                }

                statusCode, updateResult = self.member.update_member(result.id, data)
                # If Error
                if statusCode not in [204]:
                    logging.error(f'[DataService.__insertNewTransaction] Update member : {updateResult}')
                    await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId)
                                                                    , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                    return
            return 
        except Exception as e:
            logging.error(f'[DataService.__insertNewTransaction] : {e}')
            await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId)
                                                            , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
            return

    async def register(self, contex) -> None:
        '''
        Register new member
        '''
        # Delete input message
        await contex.message.delete(delay=20)
        author = contex.author
        dcId = str(author._user.id)
        name = author._user.name
        try:

            # Get member by dcId
            statusCode, result = self.member.get_member_by_dcid(dcId)
            # If Error
            if statusCode not in [200, 404]:
                logging.error(f'[DataService.register] Query member : {result}')
                await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId)
                                                                    , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                return 

            # Insert new member if not found
            if statusCode == 404:
                data = {
                    "dcId":dcId,
                    "name": name,
                    "balance": 0.00,
                }
                statusCode, result = self.member.insert_member(data)

                # If Error
                if statusCode not in [201]:
                    logging.error(f'[DataService.register] Insert member : {result}')
                    await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId)
                                                                    , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                    return 
                await contex.send("<@{}> คุณได้เปิดบัญชีเรียบร้อยแล้ว".format(dcId)
                                                                , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                return 
                
            # If member already exits just return message
            if statusCode != 404:
                await contex.send("<@{}> คุณได้เปิดบัญชีแล้ว".format(dcId)
                                                        , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                return

            return 
        except Exception as e:
            logging.error(f'[DataService.register] : {e}')
            await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId)
                                                            , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
            return

    async def daily(self, contex) -> None:
        '''
        Daily trasaction
        '''
        await contex.message.delete(delay=20)
        author = contex.author
        dcId = str(author._user.id)
        name = author._user.name

        try:

            member = await self.__createOrUpdateMember(contex, dcId, name)
            # Get trasaction by dcId and type
            statusCode, getResult = self.transaction.get_transaction_by_mid_and_type(member.id, TransactionType.DAILY.name)

            # If Error
            if statusCode not in [200, 404]:
                logging.error(f'[DataService.daily] Query transaction : {getResult}')
                await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId)
                                                                    , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                return

            daily_value = round(random.uniform(2,6), 6)

            if statusCode == 404:
                await self.__insertNewTransaction(contex, dcId, TransactionType.DAILY.name, daily_value, contributor=None)
                await contex.send("<@{}> คุณได้รับโบนัสรายวัน {} {}"
                                    .format(dcId, daily_value, get_settings().COIN_NAME)
                                    , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)

            if statusCode != 404:
                last_get = getResult[0].created_at
                diff = datetime.utcnow() - last_get
                days_diff = diff.days

                # Get bounus if daily
                if days_diff > 0:
                    await self.__insertNewTransaction(contex, dcId, TransactionType.DAILY.name, daily_value, contributor=None)
                    await contex.send("<@{}> คุณได้รับโบนัสรายวัน *{}* **{}**"
                                        .format(dcId, daily_value, get_settings().COIN_NAME)
                                        , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                    return 
                # Wait until
                else:
                    tomorrow = last_get + timedelta(days=1)
                    seconds_diff = (tomorrow - datetime.utcnow()).seconds
                    hours_diff   = divmod(seconds_diff, 3600)
                    hours = hours_diff[0]
                    minutes_diff = divmod(hours_diff[1], 60)
                    minutes = minutes_diff[0]
                    seconds = minutes_diff[1]
                    await contex.send("<@{}> คุณสามารถรับได้อีกครั้ง *{}* ชม. *{}* นาที *{}* วินาที"
                                        .format(dcId, hours, minutes, seconds)
                                        , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                    return
            return 
        except Exception as e:
            logging.error(f'[DataService.daily] : {e}')
            await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId)
                                                            , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
            return

    async def check(self, contex) -> None:
        '''
        Check balance of member
        '''
        author = contex.author
        dcId = str(author._user.id)
        name = author._user.name
        try:

            member = await self.__createOrUpdateMember(contex, dcId, name)

            await contex.send("<@{}> คุณมี *{}* **{}**"
                                .format(dcId, member.balance, get_settings().COIN_NAME))

            return
        except Exception as e:
            logging.error(f'[DataService.check] : {e}')
            await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId)
                                                            , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
            return

    async def send(self, contex, receiverI: discord.User, amount: Decimal):
        '''
        Send coin to one user to another user
        '''
        await contex.message.delete(delay=20)
        author = contex.author
        dcId = str(author._user.id)
        name = author._user.name
        try:

            # Check amount
            if amount < 0:
                await contex.send("<@{}> จำนวนเงินที่ส่งต้องมากว่า 0.00"
                                    .format(dcId), delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                return 

            member = await self.__createOrUpdateMember(contex, dcId, name)

            # Search for receiver
            statusCode, receiver = self.member.get_member_by_dcid(str(receiverI.id))
            if statusCode not in [200]:
                await contex.send("{} ผู้ใช้นี้ไม่มีในระบบ"
                                    .format(receiverI.id), delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                return

            # Balance less than amount
            if member.balance < amount:
                await contex.send("<@{}> คุณไม่มีเหรียญที่จะส่ง"
                                    .format(member.dcId), delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                return

            await self.__insertNewTransaction(contex, member.dcId, TransactionType.SEND.name, amount, 
                                                contributor=receiver)
            
            await contex.send("<@{}> คุณได้ส่ง *{}* **{}** ไปยัง <@{}>"
                                .format(member.dcId, amount, get_settings().COIN_NAME, receiver.dcId))

            return
            
        except Exception as e:
            logging.error(f'[DataService.send] : {e}')
            await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId)
                                                            , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
            return

    async def bet(self, contex, amount: Decimal):
        '''
        Bet 
        '''
        author = contex.author
        dcId = str(author._user.id)
        name = author._user.name
        try:
            # Check amount
            if amount < 0:
                await contex.message.delete(delay=20)
                await contex.send("<@{}> ค่าเดิมพันต้องมากว่า 0.00"
                                    .format(dcId), delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                return 

            member = await self.__createOrUpdateMember(contex, dcId, name)

            # Maximun bet value
            if amount > get_settings().MAX_BET:
                await contex.message.delete(delay=20)
                await contex.send("<@{}> คุณไม่สามารถเล่นมากกว่า *{}* **{}**"
                                    .format(dcId, get_settings().MAX_BET, get_settings().COIN_NAME)
                                    , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                return
            
            # Minimun bet value
            if amount < get_settings().MIN_BET:
                await contex.message.delete(delay=20)
                await contex.send("<@{}> คุณไม่สามารถเล่นน้อยกว่า *{}* **{}**"
                                    .format(dcId, get_settings().MIN_BET, get_settings().COIN_NAME)
                                    , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                return

            # Bet value more than balance of member
            if member.balance < amount:
                await contex.message.delete(delay=20)
                await contex.send("<@{}> คุณไม่มีเหรียญที่จะพนัน".format(dcId), delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                return

            if random.randint(0, 1):
                await contex.send("<@{}> คุณชนะการพนันได้รับ *{}* **{}**".format(dcId, amount, get_settings().COIN_NAME))
                await self.__insertNewTransaction(contex, member.dcId, TransactionType.BET.name, amount, contributor=None)
            else:
                await contex.send("<@{}> คุณแพ้การพนันเสีย *{}* **{}** ว้ายยยยย".format(dcId, amount, get_settings().COIN_NAME))
                await self.__insertNewTransaction(contex, member.dcId, TransactionType.BET.name, -1*amount, contributor=None)
            
            return

        except Exception as e:
            logging.error(f'[DataService.bet] : {e}')
            await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId)
                                                            , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
            return

    async def hourly(self, contex) -> None:
        '''
        Hourly trasaction
        '''
        await contex.message.delete(delay=20)
        author = contex.author
        dcId = str(author._user.id)
        name = author._user.name

        try:

            member = await self.__createOrUpdateMember(contex, dcId, name)
            # Get trasaction by dcId and type
            statusCode, getResult = self.transaction.get_transaction_by_mid_and_type(member.id, TransactionType.HOURLY.name)

            # If Error
            if statusCode not in [200, 404]:
                logging.error(f'[DataService.hourly] Query transaction : {getResult}')
                await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId)
                                                                    , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                return

            hourly_value = round(random.uniform(0.000001,2), 6)

            if statusCode == 404:
                await self.__insertNewTransaction(contex, dcId, TransactionType.HOURLY.name, hourly_value, contributor=None)
                await contex.send("<@{}> คุณได้รับโบนัสรายชั่วโมง {} {}"
                                    .format(dcId, hourly_value, get_settings().COIN_NAME)
                                    , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)

            if statusCode != 404:
                last_get = getResult[0].created_at
                diff = datetime.utcnow() - last_get
                hours_diff = diff.seconds / 3600

                # Get bounus if daily
                if hours_diff >= 1:
                    await self.__insertNewTransaction(contex, dcId, TransactionType.HOURLY.name, hourly_value, contributor=None)
                    await contex.send("<@{}> คุณได้รับโบนัสรายชั่วโมง *{}* **{}**"
                                        .format(dcId, hourly_value, get_settings().COIN_NAME)
                                        , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                    return 
                # Wait until
                else:
                    next_hour = last_get + timedelta(hours=1)
                    seconds_diff = (next_hour - datetime.utcnow()).seconds
                    hours_diff   = divmod(seconds_diff, 3600)
                    minutes_diff = divmod(hours_diff[1], 60)
                    minutes = minutes_diff[0]
                    seconds = minutes_diff[1]
                    await contex.send("<@{}> คุณสามารถรับได้อีกครั้ง *{}* นาที *{}* วินาที"
                                        .format(dcId, minutes, seconds)
                                        , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
                    return
            return 
        except Exception as e:
            logging.error(f'[DataService.daily] : {e}')
            await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId)
                                                            , delete_after=get_settings().SELF_MESSAGE_DELETE_TIME)
            return