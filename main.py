import discord
from discord import Webhook, AsyncWebhookAdapter, embeds
import aiohttp
import asyncio
import telebot

bot = telebot.TeleBot('')

async def foo(c, u, a, e, url):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
        text = "Автор: " + u + "\n" + c 
        bot.send_message(-1111111111111, text)
        await webhook.send(content=c, username=u, avatar_url=a, embeds=e)

class MessageBody:
    content = ""
    avatar = ""
    my_embeds = []
    def __init__(self, message): 
        self.my_embeds = []
        myFiles = []
        self.my_embeds.extend(message.embeds)
        for attachment in message.attachments:
            embed = embeds.Embed()
            print(attachment.content_type)
            if "image" in attachment.content_type:
                embed.set_image(url=attachment.url)
                self.my_embeds.append(embed)
            else:
                myFiles.append("File: " + attachment.filename + " -> " + attachment.url)        
        self.avatar="https://cdn.discordapp.com/avatars/" + str(message.author.id) + "/" + message.author.avatar + ".png"
        my_file_Content = "\n"
        for file in myFiles:
            my_file_Content = file + "\n"
        self.content = message.content + my_file_Content   

class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)
        
    async def on_message(self, message):
        
        #id канала из которого миррорить
        if message.channel.id == 1111111111111111111:
            test = MessageBody(message)
            text = "Автор: " + message.author.name + "\n" + test.content 
            #Отправка только в телеграмм
            bot.send_message(-1111111111111, text)

        if message.channel.id == 1111111111111111111:
            user = MessageBody(message)
            #Отправка только в дискорд
            url = "url web хука"
            task = asyncio.create_task(foo(c=user.content,u=message.author.name, a=user.avatar, e=user.my_embeds, url=url))
            await task    
                                                             
client = MyClient()
client.run('дискорд токен')
bot.polling(none_stop=True, interval=0)