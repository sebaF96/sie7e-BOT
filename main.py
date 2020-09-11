import discord
import os
import time
import datetime
from constants import Constants
from discord.ext import commands
from cogs.dota import Dota2
from cogs.among import AmongUS
from config import BOT_TOKEN


STEAM_APIKEY = os.getenv('STEAM_APIKEY')
start_time = int(time.time())
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"))
bot.remove_command('help')


@bot.event
async def on_ready():
    game = discord.Activity(name="PokerStars", type=discord.ActivityType.playing, start=datetime.datetime.utcnow())
    await bot.change_presence(status=discord.Status.online, activity=game)
    print('Ready')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("Tenes que mandar el player con este comando")


@bot.command()
async def hello(ctx):
    """Just says hello"""
    await ctx.send(f"Hello {ctx.author.name}")


@bot.command(name='help')
async def help_info(ctx):
    await ctx.send(Constants.HELP_MESSAGE.value)


@bot.command()
async def uptime(ctx):
    formatted_uptime = datetime.timedelta(seconds=int(time.time() - start_time))
    await ctx.send(f"I have been running for {formatted_uptime}")


if __name__ == '__main__':
    bot.add_cog(Dota2(bot))
    bot.add_cog(AmongUS(bot))

    bot.run(BOT_TOKEN)
