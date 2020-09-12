import discord
import datetime
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
