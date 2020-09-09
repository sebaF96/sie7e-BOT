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

        await ctx.send('Ok :mute: :mute: :mute:')


    @commands.has_role('@moderator')
    @commands.command()
    async def unmute(self, ctx):
        """Unmute all the members of the Among US channel"""
        if not ctx.guild:
            return

        voice_channel = ctx.author.voice.channel
        members = voice_channel.members

        for m in members:
            await m.edit(mute=False)

        await ctx.send('Ok :loud_sound: :loud_sound: :loud_sound:')

    @commands.command()
    async def spam(self, ctx):
        """Coming soon"""
        ...
