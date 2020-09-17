import discord
import datetime
import asyncio
from discord.ext import commands


class Events(commands.Cog):

    def __init__(self, bot):
        self.__bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        game = discord.Activity(name="PokerStars", type=discord.ActivityType.playing, start=datetime.datetime.utcnow())
        await self.__bot.change_presence(status=discord.Status.online, activity=game)
        print('Ready')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Tenes que mandar el player con este comando")
        if isinstance(error, commands.errors.CommandNotFound):
            ...
        if isinstance(error, commands.errors.MissingRole):
            ...
        else:
            print(f'{error} [command {ctx.command}]')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = member.guild.system_channel
        cog = self.__bot.get_cog('Information')
        await asyncio.sleep(10)
        await cog.userinfo(ctx=channel, member=member)
