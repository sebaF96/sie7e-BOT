import discord
from discord.ext import commands
import cogs.twitch.helix as helix
from constants import Constants


class Twitch(commands.Cog):

    def __init__(self, bot):
        self.__bot = bot

    @commands.dm_only()
    @commands.command()
    @commands.is_owner()
    async def twitch(self, ctx, streamer=None):
        """Sends and embed saying that x player is live on twitch"""
        if streamer is None:
            return

        if helix.is_live(streamer):
            stream = helix.LiveStream(streamer)
            url = stream.url

            embed = discord.Embed(title=url, url=url, color=0x97197d)
            embed.set_author(name=f"{streamer} esta en vivo!", url=url, icon_url=Constants.TWITCH_LOGO_URL.value)
            embed.set_thumbnail(url=stream.channel_photo_url)
            embed.add_field(name="Titulo", value=stream.title, inline=False)
            embed.add_field(name="Jugando a", value=stream.game_name, inline=False)
            #  embed.add_field(name="Viewers", value=stream.viewers, inline=False)
            #  embed.add_field(name="En vivo desde", value="Hoy 10:28", inline=False)
            embed.set_image(url=stream.thumbnail_url)

            await ctx.send(embed=embed)

        else:
            await ctx.send('No live')