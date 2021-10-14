import discord
import json
import random
from note import getPATH
from note import Notes
from discord.ext import commands

#去讀取json的檔案、mode是read、有可能會有中文字所以encoding是utf8
with open('setting.json', mode = 'r' , encoding = 'utf8') as jfile:
    #呼叫pic_json = 呼叫setting.json文件
    setting = json.load(jfile)


#要新增指令前面要打的符號
bot = commands.Bot(command_prefix = '+') 

@bot.event #bot被啟動會觸發事件
async def on_ready(): #去啟動on_ready這函式
    print(f">> bot is online as {bot.user}<<")

bot.remove_command("help")
@bot.command()
async def help(ctx):
    await ctx.send("""\n\n🐱------------------------------------🐱\n
* +help　-　shows this help message 
* +ping　-　shows this server's ping
* +meow　-　shows ramdon meowmeow
* +AllNote　-　shows all available notes
* +showNote <name>　-　shows <note_name>
* +writeNote <name> <content>　-　write note ! Use ''+writeNote <name> <content>'' to write it !
* +deleteNote <name>　-　 delete note ! Use ''+deleteNote <name>'' to delete it !  \n\n
🐱------------------------------------🐱""")

@bot.command() #user打command
async def ping(ctx): #這邊的(ping)就是user要打的指令，可中文
    await ctx.send(f'{round(bot.latency*1000)} (ms)')  #ctx = user傳送的屬性(eg:誰、哪個伺服器、哪個頻道)

@bot.command()
async def meow(ctx):
    random_pic = random.choice(setting['cat_pic'])
    pic = discord.File(random_pic)
    await ctx.send(file = pic)


@bot.command()
async def AllNote(ctx):
    notes = Notes(getPATH(ctx)).getAllData()
    if notes:
        message = "Availabe Note : \n\n"
        for name in notes.keys():
            message += f"+ {name}\n"

    else:
        message = "There are NO notes !"
    
    await ctx.send(message)

@bot.command()
async def showNote(ctx,name):
    editedName = name.replace(" ","_")
    content = Notes(getPATH(ctx)).get(editedName)
    if content:
        message = content
    else:
        message = f"note name {editedName} doesn't exist."
    await ctx.send(message)

@showNote.error
async def note_error(ctx,error):
    await ctx.send("`+showNote <note_name>`")

@bot.command()
async def writeNote(ctx,*,args):
    try:
        (name , content) = args.split(maxsplit=1)
    except ValueError:
        await ctx.send("You must provide some content !")
        return
    editedName = name.lower()
    editContent = content.strip()
    if len(editedName)>20 :#len -> return對象長度
        await ctx.send("Note name can't exceed 20 characters.")
        return
    
    #write to file
    notes = Notes(getPATH)
    notes.write(editedName,editContent)
    print(f"wtite note *{editedName}* on server *{ctx.guild.name}*({ctx.guild.id}) : {editContent} ")

    await ctx.send(f"Successfully wrote note *{editedName}* ! ")

@writeNote.error
async def writeNote_error(ctx,error):
    print(f"error on +writeNote : {error}")
    await ctx.send("Use `+writeNote <note_name> <content>` to add !")


@bot.command()
async def deleteNote(ctx,name):
    editedName = name.lower()
    notes = Notes(getPATH(ctx))
    
    if notes.delete(editedName):
        message = f"Note *{name}* successfully deleted ! "
        print(f"Delete note *{editedName}* on server *{ctx.guild.name}*({ctx.guild.id}) ")
    else:
        message = f"Note *{name}* doesn't exist."
    await ctx.send(message)

@deleteNote.error
async def deleteNote_error(ctx,error):
    print(f"error on +deleteNote {error}")
    await ctx.send("Use `+deleteNote <name>` to delete !")
    

bot.run(setting["TOKEN"])