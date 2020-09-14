import discord
from cogs.dota import fetcher, drawdota
from discord.ext import commands
from constants import Constants


def read_players():
    import json
    with open("cogs/dota/players.json", "r") as file:
        return json.loads(file.read())


def to_lower(argument: str):
    return argument.lower()


class Dota2(commands.Cog):
    """Cog to group all Dota 2 related commands"""

    def __init__(self, bot):
        self.__bot = bot
        self.__players = read_players()

    @commands.command()
    async def stats(self, ctx, player: to_lower):
        """Shows last 5 games of that player"""

        if player not in self.__players:
            await ctx.send(Constants.PLAYER_NOT_RECOGNIZED.value)
        else:
            try:
                player_stats = fetcher.stats(self.__players[player])
                embed = discord.Embed(title=player_stats.get_titulo(),
                                      description=player_stats.get_descripcion(),
                                      colour=discord.Color.light_grey())

                for i in range(0, 5, 1):
                    embed.add_field(name=player_stats.get_game(i), value=player_stats.get_delimiter(), inline=False)

                embed.set_thumbnail(url=player_stats.get_thumbnail())

                embed.set_footer(text=Constants.FOOTER_TEXT.value, icon_url=Constants.FOOTER_IMAGE_URL.value)
                await ctx.send(embed=embed)

            except KeyError:
                await ctx.send(Constants.PRIVATE_PROFILE.value)
            except AttributeError:
                pass

    @commands.command()
    async def refresh(self, ctx, player: to_lower):
        """Sends a POST request to refresh stats of the given player"""

        if player not in self.__players:
            await ctx.send(Constants.PLAYER_NOT_RECOGNIZED.value)
        else:
            fetcher.refresh(self.__players[player])
            await ctx.send("Ok")

    @commands.command(name='players')
    async def players_command(self, ctx):
        """Show the list of players that the bot knows with their in-game nicks"""
        string = str()
        for key in self.__players:
            try:
                name = fetcher.get_nick(self.__players[key])
                string += f"{key} **({name})**\n"
            except KeyError or TypeError:
                continue

        await ctx.send(string)

    @commands.command()
    async def wl(self, ctx, player: to_lower):
        """Shows the win-lose count in the last 20 games of the given player"""

        if player not in self.__players:
            await ctx.send(Constants.PLAYER_NOT_RECOGNIZED.value)
        else:
            try:
                await ctx.send(fetcher.w_l(self.__players[player]))
            except KeyError:
                await player.send(Constants.PRIVATE_PROFILE.value)

    @commands.command()
    async def last(self, ctx, player: to_lower):
        """Shows information about given player's last Dota match"""

        if player not in self.__players:
            await ctx.send(Constants.PLAYER_NOT_RECOGNIZED.value)
            return

        try:
            last_game = fetcher.last(self.__players[player])
            drawdota.save_build_image(last_game.get_build())
            file = discord.File("cogs/dota/last_match_items.png", filename="last.png")
            embed_colour = discord.Color.green() if last_game.get_wl().startswith(
                ":green") else discord.Color.dark_red()

            embed = discord.Embed(colour=embed_colour, title=last_game.get_title(), description=last_game.get_wl())
            embed.set_author(name=last_game.get_hero_name(), icon_url=last_game.get_hero_icon())
            embed.add_field(name="KDA", value=last_game.get_kda())
            embed.add_field(name="Duracion", value=last_game.get_duracion())
            embed.add_field(name="Last Hits", value=last_game.get_lh())
            embed.add_field(name="OPM", value=last_game.get_opm())
            embed.add_field(name="EPM", value=last_game.get_epm())
            embed.add_field(name="Daño", value=last_game.get_dano())
            embed.add_field(name="Daño a torres", value=last_game.get_dano_t())
            embed.add_field(name="Curacion", value=last_game.get_curacion())
            embed.set_footer(text=last_game.get_time_ago())
            embed.set_thumbnail(url=last_game.get_hero_img())
            embed.set_image(url="attachment://last.png")

            await ctx.send(embed=embed, file=file)

        except KeyError:
            await ctx.send(Constants.PRIVATE_PROFILE.value)

    @commands.command()
    async def avg(self, ctx, player: to_lower):
        """Shows avg stats of the given player in his last 20 matches"""

        if player not in self.__players:
            await ctx.send(Constants.PLAYER_NOT_RECOGNIZED.value)
            return
        try:
            player_avg = fetcher.avg(self.__players[player])
            embed = discord.Embed(title=player_avg.get_titulo(), colour=discord.Color.green(),
                                  description="Estadisticas de las ultimas 20 partidas")

            embed.set_thumbnail(url=player_avg.get_thumbnail())
            embed.add_field(name="Kills", value=player_avg.get_kills())
            embed.add_field(name="Muertes", value=player_avg.get_muertes())
            embed.add_field(name="Assists", value=player_avg.get_assists())
            embed.add_field(name="OPM", value=player_avg.get_opm())
            embed.add_field(name="EPM", value=player_avg.get_epm())
            embed.add_field(name="Last Hits", value=player_avg.get_lh())
            embed.add_field(name="Denegados", value=player_avg.get_denegados())
            embed.add_field(name="Daño", value=player_avg.get_dano())
            embed.add_field(name="Nivel", value=player_avg.get_nivel())
            embed.set_footer(text=Constants.FOOTER_TEXT.value, icon_url=Constants.FOOTER_IMAGE_URL.value)

            await ctx.send(embed=embed)
        except KeyError:
            await ctx.send(Constants.PRIVATE_PROFILE.value)

    @commands.command(aliases=['totals', 'totales'])
    async def total(self, ctx, player: to_lower):
        """Shows the all-time statistics of the given player"""

        if player not in self.__players:
            await ctx.send(Constants.PLAYER_NOT_RECOGNIZED.value)
            return
        try:
            player_total = fetcher.total(self.__players[player])
            embed = discord.Embed(title=player_total.get_titulo(), colour=discord.Color.purple(),
                                  description="Contador de todas las partidas jugadas")

            embed.set_thumbnail(url=player_total.get_thumbnail())
            embed.add_field(name="Partidas", value=player_total.get_total_games())
            embed.add_field(name="Winrate", value=player_total.get_winrate())
            embed.add_field(name="Kills", value=player_total.get_kills())
            embed.add_field(name="Muertes", value=player_total.get_muertes())
            embed.add_field(name="Assists", value=player_total.get_assists())
            embed.add_field(name="Last Hits", value=player_total.get_lh())
            embed.add_field(name="Denegados", value=player_total.get_denegados())
            embed.add_field(name="Daño", value=player_total.get_dano())
            embed.set_footer(text=Constants.FOOTER_TEXT.value, icon_url=Constants.FOOTER_IMAGE_URL.value)

            await ctx.send(embed=embed)
        except KeyError:
            await ctx.send(Constants.PRIVATE_PROFILE.value)

    @commands.command(aliases=['win'])
    async def wins(self, ctx):
        """Shows a ranking of wins in the last 7 days"""

        await ctx.channel.send(fetcher.wins_rank(self.__players))

    @commands.command()
    async def on(self, ctx):
        """Shows people online on Steam and playing Dota at the momment"""

        dota_players, online_players = fetcher.get_on()

        embed = discord.Embed(colour=discord.Color.dark_blue(), title="Jugadores Online",
                              description="Players que estan conectados en este momento")

        embed.set_thumbnail(url=Constants.DOTA2_IMAGE_URL.value)
        embed.set_author(name="Steam", icon_url=Constants.STEAM_IMAGE_URL.value)
        embed.set_footer(text=Constants.FOOTER_TEXT.value, icon_url=Constants.FOOTER_IMAGE_URL.value)

        dota_players_string = str() if len(dota_players) > 0 else "Nadie\n\n"
        online_players_string = str() if len(online_players) > 0 else "Nadie\n\n"

        for player_nick in dota_players:
            dota_players_string += ":green_circle:    " + player_nick + "\n\n"

        for player_nick in online_players:
            online_players_string += ":blue_circle:    " + player_nick + "\n\n"

        embed.add_field(name="Jugando Dota 2", value=dota_players_string, inline=False)
        embed.add_field(name="Conectado en Steam", value=online_players_string, inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=['vicios'])
    async def vicio(self, ctx):
        """Shows a weekly and daily ranking of games played"""

        await ctx.send("Contando partidas de cada vicio... :hourglass_flowing_sand:", delete_after=3)
        vicios_hoy, vicios_semana = fetcher.get_vicios(self.__players)

        embed = discord.Embed(colour=discord.Color.dark_blue(), title="Vicios",
                              description="Ranking de partidas jugadas")
        embed.set_thumbnail(url=Constants.DOTA2_IMAGE_URL.value)
        embed.set_footer(text=Constants.FOOTER_TEXT.value, icon_url=Constants.FOOTER_IMAGE_URL.value)

        vicios_hoy_str = str()
        vicios_semana_str = str()

        for p in vicios_hoy:
            player_name, games_played = p[0], p[1]
            vicios_hoy_str += f"- {player_name} ({games_played} games)\n\n"
        for p in vicios_semana:
            player_name, games_played = p[0], p[1]
            vicios_semana_str += f"- {player_name} ({games_played} games)\n\n"

        embed.add_field(name="Top vicios HOY", value=vicios_hoy_str, inline=False)
        embed.add_field(name="Top vicios SEMANA", value=vicios_semana_str, inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=['records'])
    async def record(self, ctx, player: to_lower):
        """Shows all-time records of the given player"""

        if player not in self.__players:
            await player.send(Constants.PLAYER_NOT_RECOGNIZED.value)
            return

        try:
            player_records = fetcher.get_records(self.__players[player])
            embed = discord.Embed(title=player_records.get_titulo(), colour=discord.Color.blue(),
                                  description="Records de todas las partidas jugadas")

            embed.set_thumbnail(url=player_records.get_thumbnail())
            embed.add_field(name="Kills", value=player_records.get_kills(), inline=False)
            embed.add_field(name="OPM", value=player_records.get_opm(), inline=False)
            embed.add_field(name="EPM", value=player_records.get_epm(), inline=False)
            embed.add_field(name="Last Hits", value=player_records.get_last_hits(), inline=False)
            embed.add_field(name="Denegados", value=player_records.get_denies(), inline=False)
            embed.add_field(name="Duracion", value=player_records.get_duration(), inline=False)
            embed.add_field(name="Assists", value=player_records.get_assists(), inline=False)
            embed.add_field(name="Daño", value=player_records.get_hero_damage(), inline=False)
            embed.add_field(name="Daño a torres", value=player_records.get_tower_damage(), inline=False)
            embed.add_field(name="Curacion", value=player_records.get_hero_healing(), inline=False)

            embed.set_footer(text=Constants.FOOTER_TEXT.value, icon_url=Constants.FOOTER_IMAGE_URL.value)

            await ctx.send(embed=embed)
        except KeyError:
            await ctx.send(Constants.PRIVATE_PROFILE.value)

    @commands.command(aliases=['lg'])
    async def lp(self, ctx):
        """Shows 5 most recent games of any known player"""

        lp_list = fetcher.get_last_played(self.__players)
        embed = discord.Embed(colour=discord.Color.blue(), title="Ultima partida jugada",
                              description="Lista de players que han terminado una partida recientemente")

        embed.set_thumbnail(url=Constants.DOTA2_IMAGE_URL.value)
        embed.set_author(name="Steam", icon_url=Constants.STEAM_IMAGE_URL.value)
        embed.set_footer(text=Constants.FOOTER_TEXT.value, icon_url=Constants.FOOTER_IMAGE_URL.value)

        for p in lp_list:
            embed.add_field(name=p[0], value=p[2], inline=False)

        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command(aliases=['displaydayliwinners', 'ddw'])
    async def winners(self, ctx):
        """Daily ranking of winners"""

        if ctx.guild:
            await ctx.message.delete()
        await ctx.send(fetcher.wins_rank(self.__players, daily=True))
