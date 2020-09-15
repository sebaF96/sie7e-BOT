import discord
from discord.ext import commands
import random


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["ri", "role"], no_pm=True)
    @commands.guild_only()
    async def roleinfo(self, ctx, *, role: discord.Role):
        """Shows information about a role"""
        guild = ctx.guild

        since_created = (ctx.message.created_at - role.created_at).days
        role_created = role.created_at.strftime("%d %b %Y %H:%M")
        created_on = "{} ({} days ago!)".format(role_created, since_created)
        members = ''
        i = 0
        for user in role.members:
            members += f'{user.name}, '
            i += 1
            if i > 30:
                break

        if str(role.colour) == "#000000":
            colour = "default"
            color = ("#%06x" % random.randint(0, 0xFFFFFF))
            color = int(colour[1:], 16)
        else:
            colour = str(role.colour).upper()
            color = role.colour

        em = discord.Embed(colour=color)
        em.set_author(name=role.name)
        em.add_field(name="Users", value=str(len(role.members)))
        em.add_field(name="Mentionable", value=role.mentionable)
        em.add_field(name="Hoist", value=role.hoist)
        em.add_field(name="Position", value=role.position)
        em.add_field(name="Managed", value=role.managed)
        em.add_field(name="Colour", value=colour)
        em.add_field(name='Creation Date', value=created_on)
        em.add_field(name='Members', value=members[:-2], inline=False)
        em.set_footer(text=f'Role ID: {role.id}')

        await ctx.send(embed=em)



    @commands.command(aliases=['server', 'si', 'svi'], no_pm=True)
    @commands.guild_only()
    async def serverinfo(self, ctx):
        """See information about the server."""
        server = ctx.guild
        total_users = len(server.members)
        online = len([m for m in server.members if m.status != discord.Status.offline])
        text_channels = len([x for x in server.channels if isinstance(x, discord.TextChannel)])
        voice_channels = len([x for x in server.channels if isinstance(x, discord.VoiceChannel)])
        categories = len(server.channels) - text_channels - voice_channels
        passed = (ctx.message.created_at - server.created_at).days
        created_at = "Creado {}. Hace mas de {} dias!".format(server.created_at.strftime("%d %b %Y %H:%M"), passed)

        data = discord.Embed(description=created_at, colour=ctx.author.color)
        data.add_field(name="Region", value=str(server.region))
        data.add_field(name="Usuarios", value="{}/{}".format(online, total_users))
        data.add_field(name="Canales de texto", value=text_channels)
        data.add_field(name="Canales de voz", value=voice_channels)
        data.add_field(name="Categorias", value=categories)
        data.add_field(name="Roles", value=len(server.roles))
        data.add_field(name="Owner", value=str(server.owner))
        data.set_footer(text="Server ID: " + str(server.id))
        data.set_author(name=server.name, icon_url=None or server.icon_url)
        data.set_thumbnail(url=None or server.icon_url)

        await ctx.send(embed=data)


    @commands.command(aliases=['ui'], no_pm=True)
    @commands.guild_only()
    async def userinfo(self, ctx, *, member: discord.Member = None):
        """Get information about a member of a server"""
        server = ctx.guild
        user = member or ctx.message.author
        avi = user.avatar_url

        if user.desktop_status != discord.Status.offline:
            status = 'Connected from Desktop'
        elif user.mobile_status != discord.Status.offline:
            status = 'Connected from Mobile'
        elif user.web_status != discord.Status.offline:
            status = 'Connected from Web'
        else:
            status = 'Disconnected'

        member_number = sorted(server.members, key=lambda m: m.joined_at).index(user) + 1

        em = discord.Embed(colour=user.colour, description=status)

        userinfo_value = f"- Account created {user.created_at.__format__('%A, %d. %B %Y')}\n" \
                         f"- Profile: {user.mention}\n" \
                         f"- ID: {user.id}"

        em.add_field(name='User info', value=userinfo_value, inline=False)

        memberinfo_value = f"- Member since {user.joined_at.__format__('%A, %d. %B %Y')}\n" \
                           f"- Member n° {member_number}\n" \
                           f"- Top role: {user.top_role.mention if user.top_role.name != '@everyone' else 'None'}"

        em.add_field(name='Member info', value=memberinfo_value, inline=False)

        em.set_thumbnail(url=avi)
        em.set_author(name=user, icon_url=server.icon_url)

        await ctx.send(embed=em)


