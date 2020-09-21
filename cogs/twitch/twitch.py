import discord
import cogs.twitch.helix as helix
from discord.ext import commands, tasks
from constants import Constants


class Twitch(commands.Cog):

    def __init__(self, bot):
        self.__bot = bot
        self.__followed_channels = ['pancho_toni']
        self.twitch_notifier.start()


    async def twitch(self, ctx, streamer=None):
        """Sends and embed saying that x player is live on twitch"""
        if streamer is None:
            return

        if helix.is_live(streamer):
            stream = helix.LiveStream(streamer)

            embed = discord.Embed(title=stream.url, url=stream.url, color=0x97197d)
            embed.set_author(name=f"{streamer} esta en vivo!", url=stream.url, icon_url=Constants.TWITCH_LOGO_URL.value)
            embed.set_thumbnail(url=stream.channel_photo_url)
            embed.add_field(name="Titulo", value=stream.title, inline=False)
            embed.add_field(name="Jugando a", value=stream.game_name, inline=False)
            #  embed.add_field(name="Viewers", value=stream.viewers, inline=False)
            #  embed.add_field(name="En vivo desde", value="Hoy 10:28", inline=False)
            embed.set_image(url=stream.thumbnail_url)
            embed.set_footer(text='Cortesia de sie7e-BOT', icon_url=Constants.FOOTER_IMAGE_URL.value)

            content = f"Che @everyone vayan a ver al {streamer} que esta stremeando breo"

            await ctx.send(content=content, embed=embed)

    @tasks.loop(minutes=10.0)
    async def twitch_notifier(self):

        for streamer in self.__followed_channels:
            if helix.is_live(streamer):
                print(f'{streamer} is live!')

                # DotA 2 guild's general channel
                discord_channel = await self.__bot.fetch_channel(755095399680704605)
                await self.twitch(ctx=discord_channel, streamer=streamer)
                self.__followed_channels.remove(streamer)

        if not self.__followed_channels:
            print('Ending task')
            self.twitch_notifier.cancel()


    @twitch_notifier.before_loop
    async def before_notifier(self):
        await self.__bot.wait_until_ready()
