import datetime
import time
from constants import Constants
from discord.ext import commands


class Misc(commands.Cog):

    def __init__(self, bot, start_time):
        self.__bot = bot
        self.__start_time = start_time

    @commands.command()
    async def hello(self, ctx):
        """Just says hello"""
        await ctx.send(f"Hello {ctx.author.name}")

    @commands.command(name='help')
    async def help_command(self, ctx):
        """Custom help command"""
        # TODO: Make it prettier
        await ctx.send(Constants.HELP_MESSAGE.value)

    @commands.command()
    async def uptime(self, ctx):
        """How long the bot has been running?"""
        formatted_uptime = datetime.timedelta(seconds=int(time.time() - self.__start_time))
        await ctx.send(f"I have been running for {formatted_uptime}")

    @commands.is_owner()
    @commands.command()
    async def say(self, ctx, *, msg):
        await ctx.message.delete(delay=0.1)
        await ctx.send(f"{msg}")
