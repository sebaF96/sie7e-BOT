from discord.ext import commands
from constants import Constants


class AmongUS(commands.Cog):
    """Cog to group all Among US related commands"""

    def __init__(self, bot):
        self.__bot = bot

    @commands.has_role('@moderator')
    @commands.command()
    async def mute(self, ctx):
        """Mute all the members of the command author's current voice channel"""
        if not ctx.guild:
            return

        voice_channel = ctx.author.voice.channel
        members = voice_channel.members

        for m in members:
            await m.edit(mute=True)

        await ctx.send(':mute:')

    @commands.has_role('@moderator')
    @commands.command()
    async def unmute(self, ctx):
        """Unmute all the members of the command author's current voice channel"""
        if not ctx.guild:
            return

        voice_channel = ctx.author.voice.channel
        members = voice_channel.members

        for m in members:
            await m.edit(mute=False)

        await ctx.send(':loud_sound:')

    @commands.command()
    async def code(self, ctx, argument: str = None):
        """Sends the code with emojis if is a valid Among Us code"""
        argument = argument.lower()
        if ctx.guild:
            await ctx.message.delete()

        if argument is None or len(argument) != 4 or not argument.isalpha():
            return

        letters = [f':regional_indicator_{letter}:' for letter in argument]
        await ctx.send(f'{letters[0]} {letters[1]} {letters[2]} {letters[3]}')
