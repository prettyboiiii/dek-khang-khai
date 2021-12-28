import os
import discord
from discord import message, VoiceClient
from discord.ext import commands
import os.path
from gtts import gTTS as gTTS
from time import sleep

client = commands.Bot(command_prefix='.')
queue = []    

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
async def p(ctx): #คำสั่งอ่านข้อความ input 
    # print all the messages after the command
    message = ctx.message.content.split(" ")
    message.pop(0)
    message = " ".join(message)
    author = ctx.author
    voiceChannel = discord.utils.get(ctx.guild.voice_channels,
                                     name=str(author.voice.channel))
    voiceClient: VoiceClient = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if (voiceClient == None):
        await voiceChannel.connect()
        voiceClient = discord.utils.get(client.voice_clients, guild=ctx.guild)
    elif (voiceClient != None):
        if not (voiceClient.is_connected()):
            await voiceChannel.connect()
            voiceClient = discord.utils.get(client.voice_clients,
                                            guild=ctx.guild)
    
    await ctx.message.delete(delay=5)
    if (voiceClient.is_playing()):
        queue.append(message)
    else:
        play(voiceChannel, voiceClient, ctx, message)

@client.command()
async def mos(ctx):
    author = ctx.author
    voiceChannel = discord.utils.get(ctx.guild.voice_channels,
                                     name=str(author.voice.channel))
    voiceClient = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voiceFile = os.path.isfile('mos.mp3')
    if not voiceFile:
        tts = gTTS(text='มอสดีแต่เย็ด เล่นกระจอก าาาาาาาาาาาาาาาาาาาาาาาาาา',
                   lang='th',
                   slow=True)
        tts.save('mos.mp3')
    if (voiceClient == None):
        await voiceChannel.connect()
        voiceClient = discord.utils.get(client.voice_clients, guild=ctx.guild)
    elif (voiceClient != None):
        if not (voiceClient.is_connected()):
            await voiceChannel.connect()
            voiceClient = discord.utils.get(client.voice_clients,
                                            guild=ctx.guild)
    print(voiceClient.is_connected())
    await voiceClient.play(discord.FFmpegPCMAudio(source="mos.mp3"))

@client.command()
async def reboot(ctx):
  os.system("pip3 install PyNaCl")
  await ctx.channel.send("reboot สำเร็จ")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


TOKEN = os.environ['TOKEN']
# keep_alive()
client.run(TOKEN)