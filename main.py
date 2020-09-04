import discord
from discord.ext import commands
import fetcher
from drawdota import save_build_image
import asyncio
from dotenv import load_dotenv
import os
import time
import datetime
from constants import Constants

load_dotenv()


def read_token():
    return os.getenv('BOT_TOKEN')


def read_players():
    import json
    with open("players.json", "r") as file:
        return json.loads(file.read())


def to_lower(argument: str):
    return argument.lower()


client = discord.Client()
players = read_players()
start_time = int(time.time())
bot = commands.Bot(command_prefix='!')
bot.remove_command('help')


@bot.event
async def on_ready():
    print('Ready')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("Tenes que mandar el player con este comando")


@bot.command()
async def hello(ctx):
    """Just says hello"""
    await ctx.send(f"Hello {ctx.author.name}")


@bot.command()
async def mute(ctx):
    """Mute all the members of the Among US channel"""
    if not ctx.guild:
        return

    author_roles = ctx.author.roles
    author_roles = [r.name for r in author_roles]

    if '@moderator' not in author_roles:
        await ctx.send('?')
        return

    voice_channel = bot.get_channel(Constants.AMONG_US_CHANNEL.value)
    members = voice_channel.members

    role = ctx.author.guild.get_role(Constants.MUTED_ROLE_ID.value)
    for m in members:
        await m.add_roles(role)

    await ctx.send('Ok :mute: :mute: :mute:')


@bot.command()
async def unmute(ctx):
    """Unmmute all the members of the Among US channel"""
    if not ctx.guild:
        return

    author_roles = ctx.author.roles
    author_roles = [r.name for r in author_roles]

    if '@moderator' not in author_roles:
        await ctx.send('?')
        return

    voice_channel = bot.get_channel(Constants.AMONG_US_CHANNEL.value)
    members = voice_channel.members

    role = ctx.author.guild.get_role(Constants.MUTED_ROLE_ID.value)

    for m in members:
        await m.remove_roles(role)

    await ctx.send('Ok :loud_sound: :loud_sound: :loud_sound:')


@bot.command()
async def stats(ctx, player: to_lower):
    """Shows last 5 games of that player"""

    if player not in players:
        await ctx.send(Constants.PLAYER_NOT_RECOGNIZED.value)
    else:
        try:
            stats_obj = fetcher.stats(players[player])
            embed = discord.Embed(title=stats_obj.get_titulo(),
                                  description=stats_obj.get_descripcion(),
                                  colour=discord.Color.light_grey())

            for i in range(0, 5, 1):
                embed.add_field(name=stats_obj.get_game(i), value=stats_obj.get_delimiter(), inline=False)

            embed.set_thumbnail(url=stats_obj.get_thumbnail())

            embed.set_footer(text=Constants.FOOTER_TEXT.value, icon_url=Constants.FOOTER_IMAGE_URL.value)
            await ctx.send(embed=embed)

        except KeyError:
            await ctx.send(Constants.PRIVATE_PROFILE.value)
        except AttributeError:
            pass


@bot.command(name='help')
async def help_info(ctx):
    await ctx.send(fetcher.show_help())


@bot.command()
async def refresh(ctx, player: to_lower):
    """Sends a POST request to refresh stats of the given player"""

    if player not in players:
        await ctx.send(Constants.PLAYER_NOT_RECOGNIZED.value)
    else:
        fetcher.refresh(players[player])
        await ctx.send("Ok")


@bot.command(name='players')
async def players_command(ctx):
    """Show the list of players that the bot knows with their in-game nicks"""
    string = str()
    for key in players:
        try:
            name = fetcher.get_nick(players[key])
            string += f"{key} **({name})**\n"
        except KeyError or TypeError:
            continue

    await ctx.send(string)


@bot.command()
async def wl(ctx, player: to_lower):
    """Shows the win-lose count in the last 20 games of the given player"""

    if player not in players:
        await ctx.send(Constants.PLAYER_NOT_RECOGNIZED.value)
    else:
        try:
            await ctx.send(fetcher.w_l(players[player]))
        except KeyError:
            await player.send(Constants.PRIVATE_PROFILE.value)


@bot.command()
async def last(ctx, player: to_lower):
    """Shows information about given player's last Dota match"""

    if player not in players:
        await ctx.send(Constants.PLAYER_NOT_RECOGNIZED.value)
        return

    try:
        last_game = fetcher.last(players[player])
        save_build_image(last_game.get_build())
        file = discord.File("last_match_items.png", filename="last.png")
        embed_colour = discord.Color.green() if last_game.get_wl().startswith(":green") else discord.Color.dark_red()

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


@bot.command()
async def avg(ctx, player: to_lower):
    """Shows avg stats of the given player in his last 20 matches"""

    if player not in players:
        await ctx.send(Constants.PLAYER_NOT_RECOGNIZED.value)
        return
    try:
        avg_obj = fetcher.avg(players[player])
        embed = discord.Embed(title=avg_obj.get_titulo(), colour=discord.Color.green(),
                              description="Estadisticas de las ultimas 20 partidas")

        embed.set_thumbnail(url=avg_obj.get_thumbnail())
        embed.add_field(name="Kills", value=avg_obj.get_kills())
        embed.add_field(name="Muertes", value=avg_obj.get_muertes())
        embed.add_field(name="Assists", value=avg_obj.get_assists())
        embed.add_field(name="OPM", value=avg_obj.get_opm())
        embed.add_field(name="EPM", value=avg_obj.get_epm())
        embed.add_field(name="Last Hits", value=avg_obj.get_lh())
        embed.add_field(name="Denegados", value=avg_obj.get_denegados())
        embed.add_field(name="Daño", value=avg_obj.get_dano())
        embed.add_field(name="Nivel", value=avg_obj.get_nivel())
        embed.set_footer(text=Constants.FOOTER_TEXT.value, icon_url=Constants.FOOTER_IMAGE_URL.value)

        await ctx.send(embed=embed)
    except KeyError:
        await ctx.send(Constants.PRIVATE_PROFILE.value)


@bot.command()
async def total(ctx, player: to_lower):
    if player not in players:
        await ctx.send(Constants.PLAYER_NOT_RECOGNIZED.value)
        return

    try:
        total_obj = fetcher.total(players[player])
        embed = discord.Embed(title=total_obj.get_titulo(), colour=discord.Color.purple(),
                              description="Contador de todas las partidas jugadas")

        embed.set_thumbnail(url=total_obj.get_thumbnail())
        embed.add_field(name="Partidas", value=total_obj.get_total_games())
        embed.add_field(name="Winrate", value=total_obj.get_winrate())
        embed.add_field(name="Kills", value=total_obj.get_kills())
        embed.add_field(name="Muertes", value=total_obj.get_muertes())
        embed.add_field(name="Assists", value=total_obj.get_assists())
        embed.add_field(name="Last Hits", value=total_obj.get_lh())
        embed.add_field(name="Denegados", value=total_obj.get_denegados())
        embed.add_field(name="Daño", value=total_obj.get_dano())
        embed.set_footer(text=Constants.FOOTER_TEXT.value, icon_url=Constants.FOOTER_IMAGE_URL.value)

        await ctx.send(embed=embed)
    except KeyError:
        await ctx.send(Constants.PRIVATE_PROFILE.value)


@client.event
async def on_message(message):
    if message.author == client.user or not message.content.startswith("!"):
        return

    if not message.guild and message.channel.recipient.name != 'Noah-':
        await client.get_channel(Constants.ADMIN_PRIVATE_CHANNEL.value).send(
            str(message.author.name) + " Said: " + message.content)

    command = message.content.split()[0].lower()
    argument = message.content.split()[1].lower() if len(message.content.split()) > 1 else None



    if command.startswith('!wins'):
        string = fetcher.wins_rank(players)

        await message.channel.send(string)

    if command.startswith("!joke"):
        await message.channel.purge(limit=1)
        joke = fetcher.get_joke()
        if joke["type"] == "single":
            await message.channel.send(joke["joke"])
        else:
            await message.channel.send(joke["setup"])

            await asyncio.sleep(10)

            await message.channel.send(joke["delivery"])

    if command.startswith("!on"):
        dota_players, online_players = fetcher.get_on()

        embed = discord.Embed(colour=discord.Color.dark_blue(), title="Jugadores Online",
                              description="Players que estan conectados en este momento")
        embed.set_thumbnail(url=Constants.DOTA2_IMAGE_URL.value)

        embed.set_author(name="Steam", icon_url=Constants.STEAM_IMAGE_URL.value)

        embed.set_footer(text=Constants.FOOTER_TEXT.value, icon_url=Constants.FOOTER_IMAGE_URL.value)

        dota_players_string = "" if len(dota_players) > 0 else "Nadie\n\n"
        online_players_string = "" if len(online_players) > 0 else "Nadie\n\n"

        for player_nick in dota_players:
            dota_players_string += ":green_circle:    " + player_nick + "\n\n"

        for player_nick in online_players:
            online_players_string += ":blue_circle:    " + player_nick + "\n\n"

        embed.add_field(name="Jugando Dota 2", value=dota_players_string, inline=False)
        embed.add_field(name="Conectado en Steam", value=online_players_string, inline=False)

        await message.channel.send(embed=embed)

    if command.startswith("!vicio"):
        await(await message.channel.send("Contando partidas de cada vicio... :hourglass_flowing_sand:")).delete(delay=1)

        vicios_hoy, vicios_semana = fetcher.get_vicios(players)
        embed = discord.Embed(colour=discord.Color.dark_blue(), title="Vicios",
                              description="Ranking de partidas jugadas")
        embed.set_thumbnail(url=Constants.DOTA2_IMAGE_URL.value)

        embed.set_footer(text=Constants.FOOTER_TEXT.value, icon_url=Constants.FOOTER_IMAGE_URL.value)

        vicios_hoy_str = ""
        vicios_semana_str = ""

        for p in vicios_hoy:
            vicios_hoy_str += "- " + p[0] + " (" + str(p[1]) + " games)\n\n"
        for p in vicios_semana:
            vicios_semana_str += "- " + p[0] + " (" + str(p[1]) + " games)\n\n"

        embed.add_field(name="Top vicios HOY", value=vicios_hoy_str, inline=False)
        embed.add_field(name="Top vicios SEMANA", value=vicios_semana_str, inline=False)

        await message.channel.send(embed=embed)

    if command.startswith('!record') and argument:
        if argument not in players:
            await message.channel.send(Constants.PLAYER_NOT_RECOGNIZED.value)
        else:
            try:
                records_obj = fetcher.get_records(players[argument])
                embed = discord.Embed(title=records_obj.get_titulo(), colour=discord.Color.blue(),
                                      description="Records de todas las partidas jugadas")
                embed.set_thumbnail(url=records_obj.get_thumbnail())

                embed.add_field(name="Kills", value=records_obj.get_kills(), inline=False)
                embed.add_field(name="OPM", value=records_obj.get_opm(), inline=False)
                embed.add_field(name="EPM", value=records_obj.get_epm(), inline=False)
                embed.add_field(name="Last Hits", value=records_obj.get_last_hits(), inline=False)
                embed.add_field(name="Denegados", value=records_obj.get_denies(), inline=False)
                embed.add_field(name="Duracion", value=records_obj.get_duration(), inline=False)
                embed.add_field(name="Assists", value=records_obj.get_assists(), inline=False)
                embed.add_field(name="Daño", value=records_obj.get_hero_damage(), inline=False)
                embed.add_field(name="Daño a torres", value=records_obj.get_tower_damage(), inline=False)
                embed.add_field(name="Curacion", value=records_obj.get_hero_healing(), inline=False)

                embed.set_footer(text=Constants.FOOTER_TEXT.value, icon_url=Constants.FOOTER_IMAGE_URL.value)

                await message.channel.send(embed=embed)
            except KeyError:
                await message.channel.send(Constants.PRIVATE_PROFILE.value)

    if command.startswith('!lp') or command.startswith("!lg"):
        lista = fetcher.get_last_played(players)
        embed = discord.Embed(colour=discord.Color.blue(), title="Ultima partida jugada",
                              description="Lista de players que han terminado una partida recientemente")
        embed.set_thumbnail(url=Constants.DOTA2_IMAGE_URL.value)

        embed.set_author(name="Steam", icon_url=Constants.STEAM_IMAGE_URL.value)
        embed.set_footer(text=Constants.FOOTER_TEXT.value, icon_url=Constants.FOOTER_IMAGE_URL.value)

        for p in lista:
            embed.add_field(name=p[0], value=p[2], inline=False)

        await message.channel.send(embed=embed)

    if command.startswith("!displaydailywinners"):
        await message.channel.purge(limit=1)
        string = fetcher.wins_rank(players, daily=True)

        await message.channel.send(string)

    if command.startswith("!uptime"):
        string = "I have been running for "
        string += str(datetime.timedelta(seconds=int(time.time() - start_time)))
        await message.channel.send(string)


if __name__ == '__main__':
    bot.run(read_token())
