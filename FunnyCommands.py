import discord, os, sys, json, requests, datetime, numpy, random, base64, codecs
from discord.ext import commands, tasks
from colorama import Fore, init
from random import randint
init()

config = json.load(open(r"C:\Users\dboon\OneDrive\Documents\Moyai2022\config.json"))

prefix = config.get('prefix')
owner = config.get('owner')

class FunnyCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        sender = message.author
        dontLog = [770072464767713280, 639778083385376768, 675448036163452959, 280689427951386624]
        channel = self.client.get_channel(826913791979683903)
        if isinstance(message.channel, discord.DMChannel):
            if sender.id in dontLog:
                return
            else:
                if message.attachments:
                    file = message.attachments[0]
                    await channel.send(f"`{sender.id} | {sender}` sent an image/file: ")
                    await channel.send(file.url)
                elif message.content == '@everyone':
                    await channel.send(f"`{sender.id} | {sender}` sent: {message.content.replace('@everyone', '@/everyone')}")
                elif message.content == '@here':
                    await channel.send(f"`{sender.id} | {sender}` sent: {message.content.replace('@here', '@/here')}")
                else:
                    await channel.send(f"`{sender.id} | {sender}` sent: {message.content}")

    @commands.command()
    async def em(self, ctx, *, args):
        await ctx.message.delete()
        em = discord.Embed(description = f'{args}', colour = 0x0000)
        await ctx.send(embed=em)

    @commands.command()
    async def av(self, ctx, member: discord.User = None):
        await ctx.message.delete()
        if member is None:
            member = ctx.message.author
        em = discord.Embed(description="Avatar", colour=0x0000)
        em.set_author(name = f"{member.name}#{member.discriminator}")
        em.set_image(url = member.avatar_url)
        await ctx.send(embed=em)
        return

    @commands.command()
    async def spam(self, ctx, amount: int, *, message):
        await ctx.message.delete()
        for _i in range(amount):
            await ctx.send(message)

    @commands.command()
    async def zawarudo(self, ctx,):
        await ctx.message.delete()
        message = await ctx.send("**The World, time has frozen.**")

def setup(client):
    client.add_cog(FunnyCommands(client))