import discord
from discord.ext import commands
import fetcher
from dotenv import load_dotenv
import os
import time
import datetime
from constants import Constants
from cogs.dota import Dota2

load_dotenv()


def read_token():
    return os.getenv('BOT_TOKEN')


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


@bot.command()
async def mute(ctx):
    """Mute all the members of the Among US channel"""
    if not ctx.guild:
        return

    author_roles = ctx.author.roles
    author_roles = [r.name for r in author_roles]

    if '@moderator' not in author_roles:
        await ctx.send('?')
        return

    voice_channel = bot.get_channel(Constants.AMONG_US_CHANNEL.value)
    members = voice_channel.members

    role = ctx.author.guild.get_role(Constants.MUTED_ROLE_ID.value)
    for m in members:
        await m.add_roles(role)

    await ctx.send('Ok :mute: :mute: :mute:')


@bot.command()
async def unmute(ctx):
    """Unmmute all the members of the Among US channel"""
    if not ctx.guild:
        return

    author_roles = ctx.author.roles
    author_roles = [r.name for r in author_roles]

    if '@moderator' not in author_roles:
        await ctx.send('?')
        return

    voice_channel = bot.get_channel(Constants.AMONG_US_CHANNEL.value)
    members = voice_channel.members

    role = ctx.author.guild.get_role(Constants.MUTED_ROLE_ID.value)

    for m in members:
        await m.remove_roles(role)

    await ctx.send('Ok :loud_sound: :loud_sound: :loud_sound:')


@bot.command(name='help')
async def help_info(ctx):
    await ctx.send(fetcher.show_help())


if __name__ == '__main__':
    bot.add_cog(Dota2(bot))
    bot.run(read_token())
