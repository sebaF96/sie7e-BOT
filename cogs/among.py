from discord.ext import commands


class AmongUS(commands.Cog):
    """Cog to group all Among US related commands"""

    def __init__(self, bot):
        self.__bot = bot
        self.__code = 'zzzz'

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

        await ctx.message.delete(delay=10)
        await ctx.send(':mute:', delete_after=15)

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

        await ctx.message.delete(delay=10)
        await ctx.send(':loud_sound:', delete_after=15)


    @commands.command()
    async def code(self, ctx, argument=None):
        """Set and sends the code if any and valid. Otherwise sends the old code setted"""
        if ctx.guild and argument is not None:
            await ctx.message.delete(delay=0.1)

        if argument is not None and len(argument) == 4 and argument.isalpha():
            self.__code = argument.lower()

        letters = [f':regional_indicator_{letter}:' for letter in self.__code]
        await ctx.send(f'{letters[0]} {letters[1]} {letters[2]} {letters[3]}')
