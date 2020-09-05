import discord
import fetcher
import os
import time
import datetime
from discord.ext import commands
from dotenv import load_dotenv
from cogs.dota import Dota2
from cogs.among import AmongUS

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

start_time = int(time.time())
bot = commands.Bot(command_prefix='!')
bot.remove_command('help')


@bot.event
async def on_ready():
    game = discord.Activity(
        name="PokerStars",
        type=discord.ActivityType.playing,
        start=datetime.datetime.utcnow())

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
    await ctx.send(fetcher.show_help())


if __name__ == '__main__':
    bot.add_cog(Dota2(bot))
    bot.add_cog(AmongUS(bot))

    bot.run(BOT_TOKEN)
