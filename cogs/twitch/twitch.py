import discord
from constants import Constants
from discord.ext import commands


class Streamer:
    def __init__(self, username, image_url):
        self.__username = username
        self.__image_url = image_url
        self.__twitch_channel = f'https://twitch.tv/{username}'

    @property
    def username(self):
        return self.__username

    @property
    def image_url(self):
        return self.__image_url

    @property
    def twitch_channel(self):
        return self.__twitch_channel


NICOLAS = Streamer('nicolasgimenez212', 'photo_url')

PANCHO = Streamer('pancho_toni', 'photo_url')


class Twitch(commands.Cog):

    def __init__(self, bot):
        self.__bot = bot
        self.__allowed_users = ['Noah-', 'pancho_toni']
        self.__streamers = ['pancho', 'nico']

    @commands.dm_only()
    @commands.command()
    async def twitch(self, ctx, streamer=None, *, game=None):
        """Sends and embed saying that x player is live on twitch"""
        if ctx.author.name not in self.__allowed_users or streamer not in self.__streamers or game is None:
            print('Unauthorized')
            return

        if streamer.lower() == 'nico':
            streamer = NICOLAS
        elif streamer.lower() == 'pancho':
            streamer = PANCHO

        embed = discord.Embed(title=f'{streamer.username} esta stremeando por Twitch!',
                              color=discord.Colour.purple(), description=streamer.twitch_channel)

        embed.set_author(name='sie7e-BOT', icon_url=Constants.FOOTER_IMAGE_URL.value)
        embed.set_image(url=streamer.image_url)
        embed.set_thumbnail(url='https://static-cdn.jtvnw.net/ttv-boxart/Among%20Us-144x192.jpg')
        embed.add_field(name='Jugando a', value=game.title(), inline=True)
        embed.add_field(name='Viewers', value='2')

        await ctx.send(embed=embed)

