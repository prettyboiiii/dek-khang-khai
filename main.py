from datetime import datetime, timedelta
from discord import FFmpegPCMAudio
from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv
from sqlite3 import Error
from constants import *
import sqlite3 as sql
from gtts import gTTS
import pandas as pd
import os.path
import discord
import random
import os

load_dotenv()

client = commands.Bot(command_prefix='.')
queue = []
coin_name = "ข้างไข่คอยด์"

def play_next(voiceChannel, voiceClient, ctx):
    voiceClient.play(discord.FFmpegPCMAudio(source="test.mp3"), after=lambda e: check_queue(voiceChannel, voiceClient, ctx))

def play(voiceChannel, voiceClient, ctx, message):
    tts = gTTS(text=str(message), lang='th', slow=True)
    tts.save('test.mp3')
    voiceClient.play(discord.FFmpegPCMAudio('noti_sound.mp3'), after=lambda e: play_next(voiceChannel, voiceClient, ctx))
        
def check_queue(voiceChannel, voiceClient, ctx):
    if len(queue) > 0:
        play(voiceChannel, voiceClient, ctx, queue.pop(0))

@client.command(pass_context=True)
async def p(ctx):
    # grab the user who sent the command
    channel = ctx.message.author.voice.channel
    # only play music if user is in a voice channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    source = FFmpegPCMAudio('test.mp3')
    player = voice.play(source)

@client.command()
async def reboot(ctx):
  os.system("pip3 install PyNaCl")
  await ctx.channel.send("reboot สำเร็จ")

@client.command(pass_context=True)
async def disconnect(ctx):
    voiceClient = discord.utils.get(client.voice_clients, guild=ctx.guild)
    await voiceClient.disconnect()
    
@client.command(pass_context=True)
async def dc(ctx):
    await disconnect(ctx)
    
def create_connection():
    conn = None
    try:
        conn = sql.connect('database.db')
        cursor = conn.cursor()
        create_file = open('create.sql', 'r').read()
        cursor.executescript(create_file)
        
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
        
@client.command(pass_context=True)
async def register(ctx):
    await ctx.message.delete(delay=5)
    author: discord.Member = ctx.author
    dc_id = author._user.id
    name = author._user.name
    try:
        conn = sql.connect('database.db')
        cursor = conn.cursor()
        member = pd.read_sql_query(f"SELECT * FROM members WHERE dc_id = {dc_id}", conn)
        if member.empty:
            cursor.execute("INSERT INTO members (dc_id, name, balance) VALUES (?, ?, ?)", (dc_id, name, 0))
            await ctx.send("<@{}> คุณได้เปิดบัญชีเรียบร้อยแล้ว".format(dc_id), delete_after=10)
        else:
            await ctx.send("<@{}> คุณได้เปิดบัญชีแล้ว".format(dc_id), delete_after=10)
        conn.commit()
    except Error as e:
        print(e)
        conn.rollback()
    finally:
        if conn:
            conn.close()
        
@client.command(pass_context=True)
async def daily(ctx):
    await ctx.message.delete(delay=5)
    author: discord.Member = ctx.author
    dc_id = author._user.id
    name = author._user.name
    try:
        conn = sql.connect('database.db')
        cursor = conn.cursor()
        member = pd.read_sql_query(f"SELECT * FROM members WHERE dc_id = {dc_id}", conn)
        ct_string = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        if member.empty:
            cursor.execute("INSERT INTO members (dc_id, name, balance) VALUES (?, ?, ?)", (dc_id, name, 0))
        elif member.iloc[0].name != name:      
            cursor.execute("UPDATE members SET name = ?, update_at = ? WHERE dc_id = ?", (name, ct_string, dc_id))
        last_tx  = pd.read_sql_query(f"SELECT * FROM transactions WHERE dc_id = {dc_id} AND type = {TransactionType.DAILY.value} ORDER BY created_at DESC", conn)
        daily_value = round(random.uniform(0.001,5), 6)
        if last_tx.empty:  
            cursor.execute("INSERT INTO transactions (dc_id, name, type, type_name, amount) VALUES (?, ?, ?, ?, ?)", (dc_id, name, TransactionType.DAILY.value, TransactionType.DAILY.name, daily_value))
            cursor.execute("UPDATE members SET balance = balance + ?, update_at = ? WHERE dc_id = ?", (daily_value, ct_string, dc_id))
            await ctx.send("<@{}> คุณได้รับโบนัสรายวัน {} {}".format(dc_id, daily_value, coin_name), delete_after=20)
        else:
            last_tx = last_tx.iloc[0]
            # ct stores current time
            last_get = datetime.strptime(last_tx.created_at, "%Y-%m-%d %H:%M:%S")
            ct = datetime.utcnow()
            # ct_string = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            diff = ct - last_get
            days_diff = diff.days
            
            tomorrow = last_get + timedelta(days=1)
            seconds_diff = (tomorrow - ct).seconds
            hours_diff   = divmod(seconds_diff, 3600)
            hours = hours_diff[0]
            minutes_diff = divmod(hours_diff[1], 60)
            minutes = minutes_diff[0]
            seconds = minutes_diff[1]
            
            if days_diff > 0:
                cursor.execute("INSERT INTO transactions (dc_id, name, type, type_name, amount) VALUES (?, ?, ?, ?, ?)", (dc_id, name, TransactionType.DAILY.value, TransactionType.DAILY.name, daily_value))
                cursor.execute("UPDATE members SET balance = balance + ?, update_at = ? WHERE dc_id = ?", (daily_value, ct_string, dc_id))
                await ctx.send("<@{}> คุณได้รับโบนัสรายวัน *{}* **{}**".format(dc_id, daily_value, coin_name), delete_after=20)
            else:
                await ctx.send("<@{}> คุณสามารถรับได้อีกครั้ง *{}* ชม. *{}* นาที *{}* วินาที".format(dc_id, hours, minutes, seconds), delete_after=60)

        conn.commit()

    except Error as e:
        print(e)
        conn.rollback()
    finally:
        if conn:
            conn.close()
        
@client.command(pass_context=True)
async def check(ctx):
    await ctx.message.delete(delay=5)
    author: discord.Member = ctx.author
    dc_id = author._user.id
    name = author._user.name
    try:
        conn = sql.connect('database.db')
        cursor = conn.cursor()
        member = pd.read_sql_query(f"SELECT * FROM members WHERE dc_id = {dc_id}", conn)
        if member.empty:
            cursor.execute("INSERT INTO members (dc_id, name, balance) VALUES (?, ?, ?)", (dc_id, name, 0))
        elif member.iloc[0].name != name:
            ct_string = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("UPDATE members SET name = ?, update_at = ? WHERE dc_id = ?", (name, ct_string, dc_id))
        balance = member.iloc[0].balance
        await ctx.send("<@{}> คุณมี *{}* **{}**".format(dc_id, balance, coin_name), delete_after=10)

        conn.commit()
    except Error as e:
        print(e)
        conn.rollback()
    finally:
        if conn:
            conn.close()

@client.command(pass_context=True)
async def send(ctx, receiver: discord.User, amount: float):
    await ctx.message.delete(delay=5)
    author: discord.Member = ctx.author
    dc_id = author._user.id
    name = author._user.name
    try:
        conn = sql.connect('database.db')
        cursor = conn.cursor()
        member = pd.read_sql_query(f"SELECT * FROM members WHERE dc_id = {dc_id}", conn)
        ct_string = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        if member.empty:
            cursor.execute("INSERT INTO members (dc_id, name, balance) VALUES (?, ?, ?)", (dc_id, name, 0))
        if member.iloc[0].name != name:
            cursor.execute("UPDATE members SET name = ?, update_at = ? WHERE dc_id = ?", (name, ct_string, dc_id))
        member = member.iloc[0]
        receiver_id = receiver.id
        receiver = pd.read_sql_query(f"SELECT * FROM members WHERE dc_id = {receiver_id}", conn)
        if receiver.empty:
            await ctx.send("<@{}> ผู้ใช้นี้ไม่มีในระบบ".format(receiver_id), delete_after=10)
            return
        receiver = receiver.iloc[0]
        if member.balance < amount:
            await ctx.send("<@{}> คุณไม่มีเหรียญที่จะส่ง".format(dc_id), delete_after=10)
            return
        
        cursor.execute("INSERT INTO transactions (dc_id, name, type, type_name, amount, contributor) VALUES (?, ?, ?, ?, ?, ?)", (dc_id, name, TransactionType.SEND.value, TransactionType.SEND.name, -amount, receiver_id))
        cursor.execute("INSERT INTO transactions (dc_id, name, type, type_name, amount, contributor) VALUES (?, ?, ?, ?, ?, ?)", (receiver_id, receiver.name, TransactionType.RECEIVE.value, TransactionType.RECEIVE.name, amount, dc_id))
        cursor.execute("UPDATE members SET balance = balance - ?, update_at = ? WHERE dc_id = ?", (amount, ct_string, dc_id))
        cursor.execute("UPDATE members SET balance = balance + ?, update_at = ? WHERE dc_id = ?", (amount, ct_string, receiver_id))
        
        await ctx.send("<@{}> คุณได้ส่ง *{}* **{}** ไปยัง <@{}>".format(dc_id, amount, coin_name, receiver_id))
        
        conn.commit()
    except Error as e:
        print(e)
        conn.rollback()
    finally:
        if conn:
            conn.close()
            
@client.command(pass_context=True)
async def bet(ctx, amount: float):
    await ctx.message.delete(delay=5)
    author: discord.Member = ctx.author
    dc_id = author._user.id
    name = author._user.name
    max_bet = 20.0
    min_bet = 0.5
    try:
        conn = sql.connect('database.db')
        cursor = conn.cursor()
        member = pd.read_sql_query(f"SELECT * FROM members WHERE dc_id = {dc_id}", conn)
        ct_string = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        if member.empty:
            cursor.execute("INSERT INTO members (dc_id, name, balance) VALUES (?, ?, ?)", (dc_id, name, 0))
        if member.iloc[0].name != name:
            cursor.execute("UPDATE members SET name = ?, update_at = ? WHERE dc_id = ?", (name, ct_string, dc_id))
        member = member.iloc[0]
        if amount > max_bet:
            await ctx.send("<@{}> คุณไม่สามารถเล่นมากกว่า *{}* **{}**".format(dc_id, max_bet, coin_name), delete_after=10)
            return
        elif amount < min_bet:
            await ctx.send("<@{}> คุณไม่สามารถเล่นน้อยกว่า *{}* **{}**".format(dc_id, min_bet, coin_name), delete_after=10)
        elif member.balance < amount:
            await ctx.send("<@{}> คุณไม่มีเหรียญที่จะพนัน".format(dc_id), delete_after=10)
            return
        else:
            if random.randint(0, 1) == 1:
                await ctx.send("<@{}> คุณชนะการพนันได้รับ *{}* **{}**".format(dc_id, amount, coin_name))
                cursor.execute("UPDATE members SET balance = balance + ?, update_at = ? WHERE dc_id = ?", (amount, ct_string, dc_id))
                cursor.execute("INSERT INTO transactions (dc_id, name, type, type_name, amount) VALUES (?, ?, ?, ?, ?)", (dc_id, name, TransactionType.BET.value, TransactionType.BET.name, amount))
            else:
                await ctx.send("<@{}> คุณแพ้การพนันเสีย *{}* **{}** ว้ายยยยย".format(dc_id, amount, coin_name))
                cursor.execute("UPDATE members SET balance = balance - ?, update_at = ? WHERE dc_id = ?", (amount, ct_string, dc_id))
                cursor.execute("INSERT INTO transactions (dc_id, name, type, type_name, amount) VALUES (?, ?, ?, ?, ?)", (dc_id, name, TransactionType.BET.value, TransactionType.BET.name, -amount))
        conn.commit()
          
    except Error as e:
        print(e)
        conn.rollback()
    finally:
        if conn:
            conn.close()
    
@client.event
async def on_ready():
    create_connection()
    print('We have logged in as {0.user}'.format(client))


TOKEN = os.environ['TOKEN']
# keep_alive()
client.run(TOKEN)