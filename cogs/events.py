import discord
import datetime
import os
from discord.ext import commands
from constants import Constants


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

        # Dota commands that needs a player argument
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Tenes que mandar el player con este comando")

        # Misspelled commands, do nothing
        elif isinstance(error, commands.errors.CommandNotFound):
            pass

        # Commands that needs role permission
        elif isinstance(error, commands.errors.MissingRole):
            await ctx.send("?")

        # Commands with cooldown
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.message.add_reaction('🤔')
            await ctx.message.delete(delay=10)

        else:
            print(f'{error} [command {ctx.command}]')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """
        channel = member.guild.system_channel
        cog = self.__bot.get_cog('Information')
        await asyncio.sleep(10)
        await cog.userinfo(ctx=channel, member=member)
        """
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild or not str(message.guild.id) == os.getenv("DOTA2_GUILD_ID"):
            return
        elif message.content.startswith(";;") or message.author.id == Constants.FREDBOAT_ID.value:
            await message.delete(delay=420)
