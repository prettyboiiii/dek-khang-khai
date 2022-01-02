from src.services.transactionService import TransactionService
from src.utils.configs.app_settings import get_settings
from src.models.TransactionType import TransactionType
from src.services.memberService import MemberService
from datetime import datetime, timedelta
from decimal import Decimal
import logging
import random

class DataService():
    def __init__(self) -> None:
        self.member = MemberService()
        self.transaction = TransactionService()

    async def register(self, contex) -> None:
        '''
        Register new member
        '''
        # Delete input message
        await contex.message.delete(delay=20)
        author = contex.author
        dcId = str(author._user.id)
        name = author._user.name

        # Get member by dcId
        statusCode, result = self.member.get_member_by_dcid(dcId)
        # If Error
        if statusCode not in [200, 404]:
            logging.error(f'Query member error {result}')
            await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId), delete_after=10)
            return 

        # Insert new member if not found
        if statusCode == 404:
            data = {
                "dcId":dcId,
                "name": name,
                "balance": 0.00,
                "created_at": datetime.utcnow(),
                "update_at": datetime.utcnow()
            }
            statusCode, result = self.member.insert_member(data)

            # If Error
            if statusCode not in [201]:
                logging.error(f'Insert member error {result}')
                await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId), delete_after=10)
                return 
            await contex.send("<@{}> คุณได้เปิดบัญชีเรียบร้อยแล้ว".format(dcId), delete_after=10)
            return 
            
        # If member already exits just return message
        if statusCode != 404:
            await contex.send("<@{}> คุณได้เปิดบัญชีแล้ว".format(dcId), delete_after=10)
            return

    async def __insertNewTransaction(self, contex, dcId, type, amount):
        '''
        Insert trasaction
        '''
        # Get member by dcId
        statusCode, result = self.member.get_member_by_dcid(dcId)
        # If Error
        if statusCode not in [200, 404]:
            logging.error(f'Query member error {result}')
            await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId), delete_after=10)
            return 

        data = {
            "mid": result.id,
            "type": type,
            "amount": amount,
            "contributor": None,
            "created_at": datetime.utcnow(),
            "update_at": datetime.utcnow()
        }
        statusCode, insertResult = self.transaction.insert_transaction(data)
        if statusCode not in [201]:
            logging.error(f'Insert transaction error : {insertResult}')
            await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId), delete_after=10)
            return

        data = {
            "balance": result.balance + Decimal(amount),
            "update_at": datetime.utcnow()
        }

        statusCode, updateResult = self.member.update_member(result.id, data)
        if statusCode not in [204]:
            logging.error(f'Update member error : {updateResult}')
            await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId), delete_after=10)
            return 

        await contex.send("<@{}> คุณได้รับโบนัสรายวัน {} {}".format(dcId, amount, get_settings().COIN_NAME), delete_after=10)

    async def daily(self, contex) -> None:
        '''
        Daily trasaction
        '''
        await contex.message.delete(delay=20)
        author = contex.author
        dcId = str(author._user.id)
        name = author._user.name
        mid = ""

        # Get member by dcId
        statusCode, getResult = self.member.get_member_by_dcid(dcId)
        # If Error
        if statusCode not in [200, 404]:
            logging.error(f'Query member error : {getResult}')
            await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId), delete_after=10)
            return 

        # Get id from member
        if getResult is not None:
            mid = getResult.id

        # Insert new member if not found
        if statusCode == 404:
            data = {
                "dcId":dcId,
                "name": name,
                "balance": 0.00,
                "created_at": datetime.utcnow(),
                "update_at": datetime.utcnow()
            }
            statusCode, insertResult = self.member.insert_member(data)
        
            # If Error
            if statusCode not in [201]:
                logging.error(f'Insert member error : {insertResult}')
                await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId), delete_after=10)
                return 

            # Get id from member
            mid = insertResult

        # Update name
        elif getResult.name != name:
            data = {
                "name": name,
                "update_at": datetime.utcnow()
            }
            statusCode, updateResult = self.member.update_member(getResult.id, data)

            # If Error
            if statusCode not in [204]:
                logging.error(f'Update member error : {updateResult}')
                await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId), delete_after=10)
                return 

        # Get trasaction by dcId and type
        statusCode, getResult = self.transaction.get_transaction_by_mid_and_type(mid, TransactionType.DAILY.name)

        # If Error
        if statusCode not in [200, 404]:
            logging.error(f'Query transaction error : {getResult}')
            await contex.send("<@{}> เกิดข้อผิดพลาดโปรดลองใหม่อีกครั้ง".format(dcId), delete_after=10)
            return

        daily_value = round(random.uniform(0.001,5), 6)

        if statusCode == 404:
            await self.__insertNewTransaction(contex, dcId, TransactionType.DAILY.name, daily_value)
            
        if statusCode != 404:
            last_get = getResult[0].created_at
            diff = datetime.utcnow() - last_get
            days_diff = diff.days

            # Get bounus if daily
            if days_diff > 0:
                await self.__insertNewTransaction(contex, dcId, TransactionType.DAILY.name, daily_value)
                await contex.send("<@{}> คุณได้รับโบนัสรายวัน *{}* **{}**".format(dcId, daily_value, get_settings().COIN_NAME), delete_after=10)
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
                await contex.send("<@{}> คุณสามารถรับได้อีกครั้ง *{}* ชม. *{}* นาที *{}* วินาที".format(dcId, hours, minutes, seconds), delete_after=10)
                return 