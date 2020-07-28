import discord
from fetcher import stats, show_help, refresh, get_nick, w_l, last, avg, total, wins_rank, get_joke, get_on,\
    get_vicios, get_records, get_last_played
from drawdota import save_build_image
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()


def read_token():
    return os.getenv('BOT_TOKEN')


client = discord.Client()

players = {'gonza': 324686074, 'seba': 179677205, 'gena': 134129467, 'pancho': 137703388, 'yair': 156552375,
           'pela': 130817647, 'jorge': 153309908,
           'chino': 135179013, 'statham': 145875771, 'lucas': 275221784, 'snoop': 354096578, 'negro': 140411170,
           'dobby': 190501988}


@client.event
async def on_message(message):

    if message.author == client.user or not message.content.startswith("!"):
        return

    command = message.content.split()[0].lower()
    argument = message.content.split()[1].lower() if len(message.content.split()) > 1 else None

    if command.startswith('!hello'):
        await message.channel.send('Hello noob')

    if command.startswith('!stats') and argument:
        if argument not in players:
            await message.channel.send("Ni idea quien es ese. Tira !players para ver los que conozco")
        else:
            try:
                stats_obj = stats(players[argument])
                embed = discord.Embed(title=stats_obj.get_titulo(), description=stats_obj.get_descripcion(),
                                      colour=discord.Color.light_grey())

                for i in range(0, 5, 1):
                    embed.add_field(name=stats_obj.get_game(i), value=stats_obj.get_delimiter(), inline=False)

                embed.set_thumbnail(url=stats_obj.get_thumbnail())

                embed.set_footer(text="Cortesia de sie7e-BOT",
                                 icon_url="https://steamcdn-a.akamaihd.net/apps/dota2/images/heroes/rattletrap_icon.png")
                await message.channel.send(embed=embed)

            except KeyError:
                await message.channel.send("Tiene el perfil privado esa caquita")

    if command.startswith('!help') or command.startswith('!commands'):
        await message.channel.send(show_help())

    if command.startswith('!refresh') and argument:
        if argument not in players:
            await message.channel.send("Ni idea quien es ese. Tira !players para ver los que conozco")
        else:
            refresh(players[argument])
            await message.channel.send("Ok")

    if command.startswith('!players'):
        string = ""
        for key in players:
            try:
                name = get_nick(players[key])
                string += key + " **(" + str(name) + ")**\n"
            except KeyError or TypeError:
                continue

        await message.channel.send(string)

    if command.startswith('!wl') and argument:
        if argument not in players:
            await message.channel.send("Ni idea quien es ese. Tira !players para ver los que conozco")
        else:
            try:
                await message.channel.send(w_l(players[argument]))
            except KeyError:
                await message.channel.send("Tiene el perfil privado esa caquita")

    if command.startswith('!last') and argument:
        if argument not in players:
            await message.channel.send("Ni idea quien es ese. Tira !players para ver los que conozco")
        else:
            try:

                last_game = last(players[argument])

                save_build_image(last_game.get_build())
                file = discord.File("last_match_items.png", filename="image.png")

                embed = discord.Embed(
                    colour=discord.Color.green() if last_game.get_wl().startswith(
                        ":green") else discord.Color.dark_red(),
                    title=last_game.get_title(),
                    description=last_game.get_wl())
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
                embed.set_image(url="attachment://image.png")

                await message.channel.send(embed=embed, file=file)

            except KeyError:
                await message.channel.send("Tiene el perfil privado esa caquita")

    if command.startswith('!avg') and argument:
        if argument not in players:
            await message.channel.send("Ni idea quien es ese. Tira !players para ver los que conozco")
        else:
            try:
                avg_obj = avg(players[argument])
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
                embed.set_footer(text="Cortesia de sie7e-BOT",
                                 icon_url="https://steamcdn-a.akamaihd.net/apps/dota2/images/heroes/rattletrap_icon.png")

                await message.channel.send(embed=embed)
            except KeyError:
                await message.channel.send("Tiene el perfil privado esa caquita")

    if command.startswith('!total') and argument:
        if argument not in players:
            await message.channel.send("Ni idea quien es ese. Tira !players para ver los que conozco")
        else:
            try:
                total_obj = total(players[argument])
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
                embed.set_footer(text="Cortesia de sie7e-BOT",
                                 icon_url="https://steamcdn-a.akamaihd.net/apps/dota2/images/heroes/rattletrap_icon.png")

                await message.channel.send(embed=embed)
            except KeyError:
                await message.channel.send("Tiene el perfil privado esa caquita")

    if command.startswith('!wins'):
        string = wins_rank(players)

        await message.channel.send(string)

    if command.startswith("!joke"):
        await message.channel.purge(limit=1)
        joke = get_joke()
        if joke["type"] == "single":
            await message.channel.send(joke["joke"])
        else:
            await message.channel.send(joke["setup"])

            await asyncio.sleep(10)

            await message.channel.send(joke["delivery"])

    if command.startswith("!on"):
        dota_players, online_players = get_on()

        embed = discord.Embed(colour=discord.Color.dark_blue(), title="Jugadores Online",
                              description="Players que estan conectados en este momento")
        embed.set_thumbnail(
            url="https://deadlysurprise.github.io/d2LoadingScreens/d2logo.png")

        embed.set_author(name="Steam", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/"
                                                "Steam_icon_logo.svg/1024px-Steam_icon_logo.svg.png")
        embed.set_footer(text="Cortesia de sie7e-BOT",
                         icon_url="https://steamcdn-a.akamaihd.net/apps/dota2/images/heroes/rattletrap_icon.png")


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

        vicios_hoy, vicios_semana = get_vicios(players)
        embed = discord.Embed(colour=discord.Color.dark_blue(), title="Vicios",
                              description="Ranking de partidas jugadas")
        embed.set_thumbnail(
            url="https://deadlysurprise.github.io/d2LoadingScreens/d2logo.png")

        embed.set_footer(text="Cortesia de sie7e-BOT",
                         icon_url="https://steamcdn-a.akamaihd.net/apps/dota2/images/heroes/rattletrap_icon.png")

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
            await message.channel.send("Ni idea quien es ese. Tira !players para ver los que conozco")
        else:
            try:
                records_obj = get_records(players[argument])
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

                embed.set_footer(text="Cortesia de sie7e-BOT",
                                 icon_url="https://steamcdn-a.akamaihd.net/apps/dota2/images/heroes/rattletrap_icon.png")

                await message.channel.send(embed=embed)
            except KeyError:
                await message.channel.send("Tiene el perfil privado esa caquita")

    if command.startswith('!lp') or command.startswith("!lg"):
        lista = get_last_played(players)
        embed = discord.Embed(colour=discord.Color.blue(), title="Ultima partida jugada",
                              description="Lista de players que han terminado una partida recientemente")
        embed.set_thumbnail(
            url="https://deadlysurprise.github.io/d2LoadingScreens/d2logo.png")

        embed.set_author(name="Steam", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/"
                                                "Steam_icon_logo.svg/1024px-Steam_icon_logo.svg.png")
        embed.set_footer(text="Cortesia de sie7e-BOT",
                         icon_url="https://steamcdn-a.akamaihd.net/apps/dota2/images/heroes/rattletrap_icon.png")

        for p in lista:
            embed.add_field(name=p[0], value=p[2], inline=False)

        await message.channel.send(embed=embed)

    if command.startswith("!displaydayliwinners"):
        await message.channel.purge(limit=1)
        string = wins_rank(players, daily=True)

        await message.channel.send(string)

    if command.startswith("!rtcgoinglive"):
        await message.channel.purge(limit=1)
        string = "Arteezy esta transmitiendo en directo por Twitch. Veanlo y aprendan algo"
        string += "\n\nhttps://www.twitch.tv/Arteezy"

        await message.channel.send(string)




client.run(read_token())
