import discord
from discord.ext import commands
from constants import Constants


class Information(commands.Cog):
    def __init__(self, bot):
        self.__bot = bot

    @commands.command(aliases=['help', 'commands', 'comandos'])
    async def help_command(self, ctx):
        embed = discord.Embed(title='Comandos de sie7e-BOT', color=discord.Color.blue())

        embed.set_author(name='sie7e-BOT', icon_url=Constants.FOOTER_IMAGE_URL.value)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)

        for command, message in Constants.HELP_COMMANDS.value.items():
            embed.add_field(name=f'**`{command}`**', value=f'{message}', inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=['server', 'si', 'svi'], no_pm=True)
    @commands.guild_only()
    async def serverinfo(self, ctx):
        """See information about the server."""

        # Channels count
        text_channels = len([x for x in ctx.guild.channels if isinstance(x, discord.TextChannel)])
        voice_channels = len([x for x in ctx.guild.channels if isinstance(x, discord.VoiceChannel)])
        categories = len(ctx.guild.channels) - text_channels - voice_channels

        # Members count
        total_members = len(ctx.guild.members)
        bots = len([b for b in ctx.guild.members if b.bot])
        moderators_count = len([m for m in ctx.guild.members if m.top_role.name == '@moderator'])
        roles = len(ctx.guild.roles)

        # Member statuses
        online = len([m for m in ctx.guild.members if m.status == discord.Status.online])
        idle = len([m for m in ctx.guild.members if m.status == discord.Status.idle])
        do_not_disturb = len([m for m in ctx.guild.members if m.status == discord.Status.do_not_disturb])
        offline = len([m for m in ctx.guild.members if m.status == discord.Status.offline])

        server_info = f"- Created {ctx.guild.created_at.strftime('%d %b %Y')}\n- Region: {ctx.guild.region}"
        channels_count = f"- Text channels: {text_channels}\n- Voice channels: {voice_channels}\n- Categories: {categories}"
        member_counts = f"- Members: {total_members}\n- Bots: {bots}\n- Moderators: {moderators_count}\n- Roles: {roles}"
        member_statuses = f""":green_circle: {online} :yellow_circle: {idle} :red_circle: {do_not_disturb} :white_circle: {offline}"""

        embed = discord.Embed(colour=discord.Colour.orange())
        embed.add_field(name='Server information', value=server_info, inline=False)
        embed.add_field(name="Channels count", value=channels_count, inline=False)
        embed.add_field(name="Members count", value=member_counts, inline=False)
        embed.add_field(name="Members statuses", value=member_statuses, inline=False)

        embed.set_thumbnail(url=None or ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=['ui'], no_pm=True)
    @commands.guild_only()
    async def userinfo(self, ctx, *, member: discord.Member = None):
        """Get information about a member of a server"""
        server = ctx.guild
        user = member or ctx.message.author

        if user.desktop_status != discord.Status.offline:
            status = 'Connected from Desktop'
        elif user.mobile_status != discord.Status.offline:
            status = 'Connected from Mobile'
        elif user.web_status != discord.Status.offline:
            status = 'Connected from Web'
        else:
            status = 'Disconnected'

        member_number = sorted(server.members, key=lambda m: m.joined_at).index(user) + 1
        userinfo_value = f"- Account created {user.created_at.__format__('%d %b %Y')}\n- Profile: {user.mention}\n- ID: {user.id}"""
        memberinfo_value = f"- Member since {user.joined_at.__format__('%d %b %Y')}\n- Member n° {member_number}\n- Top role: {user.top_role.mention if user.top_role.name != '@everyone' else 'None'}"

        em = discord.Embed(colour=user.colour)
        em.set_thumbnail(url=user.avatar_url)
        em.set_author(name=user, icon_url=server.icon_url)
        em.add_field(name='User info', value=userinfo_value, inline=False)
        em.add_field(name='Member info', value=memberinfo_value, inline=False)
        em.add_field(name='Status', value=status)

        await ctx.send(embed=em)
