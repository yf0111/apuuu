import discord
import json
import random
from discord.ext import commands

#去讀取json的檔案、mode是read、有可能會有中文字所以encoding是utf8
with open('setting.json', mode = 'r' , encoding = 'utf8') as jfile:
    #呼叫jdata = 呼叫setting.json文件
    jdata = json.load(jfile)


#要新增指令前面要打的符號
bot = commands.Bot(command_prefix = '+') 

@bot.event #bot被啟動會觸發事件
async def on_ready(): #去啟動on_ready這函式
    print(">> bot is online <<")

@bot.command() #user打command
async def ping(ctx): #這邊的(ping)就是user要打的指令，可中文
    await ctx.send(f'{round(bot.latency*1000)} (ms)')  #ctx = user傳送的屬性(eg:誰、哪個伺服器、哪個頻道)

@bot.command()
async def 給我圖(ctx):
    random_pic = random.choice(jdata['test_pic'])
    pic = discord.File(random_pic)
    await ctx.send(file = pic)

@bot.command()
async def 給我貓貓(ctx):
    random_pic = random.choice(jdata['cat_pic'])
    pic = discord.File(random_pic)
    await ctx.send(file = pic)

@bot.command()
async def 給我梗圖(ctx):
    random_pic = random.choice(jdata['url_pic'])
    await ctx.send(random_pic)

bot.run(jdata["TOKEN"])
