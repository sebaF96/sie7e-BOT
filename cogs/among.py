from discord.ext import commands
from constants import Constants


class AmongUS(commands.Cog):
    """Cog to group all Among US related commands"""
    def __init__(self, bot):
        self.__bot = bot

    @commands.command()
    async def mute(self, ctx):
        """Mute all the members of the Among US channel"""
        if not ctx.guild:
            return

        author_roles = ctx.author.roles
        author_roles = [r.name for r in author_roles]

        if '@moderator' not in author_roles:
            await ctx.send('?')
            return

        voice_channel = self.__bot.get_channel(Constants.AMONG_US_CHANNEL.value)
        members = voice_channel.members

        role = ctx.author.guild.get_role(Constants.MUTED_ROLE_ID.value)
        for m in members:
            await m.add_roles(role)

        await ctx.send('Ok :mute: :mute: :mute:')

    @commands.command()
    async def unmute(self, ctx):
        """Unmmute all the members of the Among US channel"""
        if not ctx.guild:
            return

        author_roles = ctx.author.roles
        author_roles = [r.name for r in author_roles]

        if '@moderator' not in author_roles:
            await ctx.send('?')
            return

        voice_channel = self.__bot.get_channel(Constants.AMONG_US_CHANNEL.value)
        members = voice_channel.members

        role = ctx.author.guild.get_role(Constants.MUTED_ROLE_ID.value)

        for m in members:
            await m.remove_roles(role)

        await ctx.send('Ok :loud_sound: :loud_sound: :loud_sound:')

    @commands.command()
    async def spam(self, ctx):
        """Coming soon"""
        ...
