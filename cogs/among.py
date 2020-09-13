import discord
from constants import Constants
from discord.ext import commands


class AmongUS(commands.Cog):
    """Cog to group all Among US related commands"""

    def __init__(self, bot):
        self.__bot = bot
        self.__code = 'zzzz'

    @commands.has_role('@moderator')
    @commands.command(aliases=['m'])
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
    @commands.command(aliases=['u'])
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


    @commands.command(aliases=['codigo'])
    async def code(self, ctx, argument=None):
        """Set and sends the code if any and valid. Otherwise sends the old code setted"""
        if ctx.guild and argument is not None:
            await ctx.message.delete(delay=0.1)

        if argument is not None and len(argument) == 4 and argument.isalpha():
            self.__code = argument.lower()

        letters = [f':regional_indicator_{letter}:' for letter in self.__code]
        await ctx.send(f'{letters[0]} {letters[1]} {letters[2]} {letters[3]}')


    @commands.guild_only()
    @commands.command(aliases=['amongo', 'amongus'])
    async def among(self, ctx):
        """Sends the name of the users that are playing Among Us ATM"""

        members_among = [m for m in ctx.guild.members if m.activity is not None and m.activity.name == 'Among Us']

        embed = discord.Embed(title='Among US', color=discord.Colour.orange())
        embed.set_author(name='sie7e-BOT', icon_url=Constants.FOOTER_IMAGE_URL.value)
        embed.set_thumbnail(url=Constants.AMONG_US_IMAGE_URL.value)

        field_value = str()
        if len(members_among) > 0:
            for m in members_among:
                field_value += f'- {m.name}\n'
        else:
            field_value = 'Nadie'
        embed.add_field(name=f'Gente jugando a esta shit ({len(members_among)})', value=field_value)

        await ctx.send(embed=embed)
