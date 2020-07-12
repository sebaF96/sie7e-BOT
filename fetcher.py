import json
import requests
import time
from objects import Last, Total, Avg


def get_hero_dict() -> dict:
    response = requests.get('https://api.opendota.com/api/heroes')
    full_hero_dict = json.loads(response.text)
    min_hero_dict = {}

    for hero in full_hero_dict:
        min_hero_dict[hero["id"]] = hero["localized_name"]

    return min_hero_dict


def get_hero_picture(icon=False) -> dict:
    base_url = "https://steamcdn-a.akamaihd.net"
    with open('heroes.json', 'r') as file:
        data = file.read()
        full_hero_dict = json.loads(data)
        min_hero_dict = {}

        if icon:
            for hero in full_hero_dict:
                min_hero_dict[int(full_hero_dict[hero]["id"])] = base_url + str(full_hero_dict[hero]['icon'])
        else:
            for hero in full_hero_dict:
                min_hero_dict[int(full_hero_dict[hero]["id"])] = base_url + str(full_hero_dict[hero]['img'])

        return min_hero_dict


HERO_DICT = get_hero_dict()
HERO_PICTURE = get_hero_picture()
HERO_ICON = get_hero_picture(icon=True)


def get_nick(player_id: int):
    if player_id == 275221784:
        return "Skywalker"

    response = requests.get('https://api.opendota.com/api/players/' + str(player_id))
    profile = json.loads(response.text)

    return profile["profile"]["personaname"]


def get_avatar_url(player_id: int):
    if player_id == 275221784:
        return "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/b6/b61deaa03441b6a4c3c641f9ca2eff76c94a2154_full.jpg"

    response = requests.get('https://api.opendota.com/api/players/' + str(player_id))
    profile = json.loads(response.text)

    return profile["profile"]["avatarfull"]


def is_radiant(player_slot: int) -> bool:
    return 0 <= player_slot <= 127


def format_duration(duration: int) -> str:
    seconds = duration % 60
    minutes = (duration - seconds) // 60
    if seconds < 10:
        seconds = '0' + str(seconds)

    return str(minutes) + ':' + str(seconds)


def format_time_ago(timestamp):
    time_now = int(time.time())
    time_ago = time_now - timestamp - 500

    if time_ago < 0:
        return "recien."

    if time_ago >= 86400:
        days = int(time_ago / 86400)
        return "hace " + str(days) + "d aprox."

    if time_ago >= 3600:
        hours = int(time_ago / 3600)
        return "hace " + str(hours) + "h aprox."

    if time_ago >= 60:
        minutes = int(time_ago / 60)
        return "hace " + str(minutes) + " min aprox."

    return "hace " + time_ago + " seg aprox."


def stats(player_id: int) -> str:
    response = requests.get('https://api.opendota.com/api/players/' + str(player_id) + '/recentMatches')
    recent_matches = json.loads(response.text)

    string = "**Ultimos 5 games de " + get_nick(player_id) + "\n"
    string += ("-" * 38) + "**"

    for match in recent_matches[:5]:
        radiant = is_radiant(match["player_slot"])
        wl = "\n:green_circle:   Gano" if radiant == match["radiant_win"] else " \n:red_circle:   Perdio "
        string += wl + " con **"
        string += HERO_DICT[match["hero_id"]] + "** y salio **"
        string += str(match["kills"]) + '/' + str(match["deaths"]) + '/' + str(match["assists"]) + '**'

    string += ""

    return string


def show_help() -> str:
    string = "** COMANDOS **\n"
    string += "**`!help`** --> muestra este mensaje\n"
    string += "**`!players`** --> muestra los players de los q podes ver la data\n"
    string += "**`!stats <player>`** --> muestra las ultimas 5 partidas de ese player\n"
    string += "**`!wl <player>`** --> muestra el W - L de las ultimas 20 partidas de ese player\n"
    string += "**`!refresh <player>`** --> actualiza las estadisticas de ese player\n"
    string += "**`!last <player>`** ---> muestra la ultima partida de ese player\n"
    string += "**`!avg <player>`** ---> muestra las estadisticas de ese player (ultimas 20 partidas)\n"
    string += "**`!total <player>`** ---> muestra los totales de ese player\n"
    string += "**`!wins`** ---> muestra un ranking de los mas ganadores en los ultimos 5 dias\n"
    string += "**`!random`** ---> te tira la img de un heroe random\n"

    return string


def refresh(player_id: int):
    r = requests.post(' https://api.opendota.com/api/players/' + str(player_id) + '/refresh')


def w_l(player_id: int) -> str:
    response = requests.get('https://api.opendota.com/api/players/' + str(player_id) + '/recentMatches')
    recent_matches = json.loads(response.text)
    wins = 0
    defeats = 0

    for match in recent_matches:
        if is_radiant(match['player_slot']) == match['radiant_win']:
            wins += 1
        else:
            defeats += 1
    string = "W - L de " + get_nick(player_id) + ": **" + str(wins) + " - " + str(defeats) + "**"

    return string


def last(player_id: int) -> Last:
    response = requests.get('https://api.opendota.com/api/players/' + str(player_id) + '/recentMatches')
    recent_matches = json.loads(response.text)
    match = recent_matches[0]
    radiant = is_radiant(match['player_slot'])

    last_game = Last()

    last_game.set_hero_icon(HERO_ICON[match["hero_id"]])
    last_game.set_hero_img(HERO_PICTURE[match["hero_id"]])
    last_game.set_hero_name(HERO_DICT[match["hero_id"]])

    last_game.set_title("Ultimo game de " + get_nick(player_id))
    last_game.set_wl(":green_circle:   Victoria" if radiant == match["radiant_win"] else ":red_circle:   Derrota ")
    last_game.set_kda(str(match["kills"]) + '/' + str(match["deaths"]) + '/' + str(match["assists"]))
    last_game.set_duracion(format_duration(match["duration"]))
    last_game.set_lh(str(match["last_hits"]))
    last_game.set_opm(str(match["gold_per_min"]))
    last_game.set_epm(str(match["xp_per_min"]))
    last_game.set_dano(str("{:,}".format(match["hero_damage"]).replace(',', '.')))
    last_game.set_dano_t(str("{:,}".format(match["tower_damage"]).replace(',', '.')))
    last_game.set_curacion(str("{:,}".format(match["hero_healing"]).replace(',', '.')))
    last_game.set_time_ago(format_time_ago(match['start_time'] + match['duration']))

    return last_game


def avg(player_id: int) -> str:
    response = requests.get('https://api.opendota.com/api/players/' + str(player_id) + '/totals?limit=20')
    totals = json.loads(response.text)

    string = "**Promedios de " + get_nick(player_id) + " (ultimas 20)\n"
    string += ("-" * 40) + "** \n"

    string += "** Kills: ** `" + str(totals[0]["sum"] / 20).replace('.', ',') + "`\n"
    string += "** Muertes: ** `" + str(totals[1]["sum"] / 20).replace('.', ',') + "`\n"
    string += "** Assists: ** `" + str(totals[2]["sum"] / 20).replace('.', ',') + "`\n"
    string += "** OPM: ** `" + str(round(totals[4]["sum"] / 20)) + "`\n"
    string += "** EPM: ** `" + str(round(totals[5]["sum"] / 20)) + "`\n"
    string += "** Last Hits: ** `" + str(round(totals[6]["sum"] / 20)) + "`\n"
    string += "** Denegados: ** `" + str(round(totals[7]["sum"] / 20)) + "`\n"
    string += "** Daño: ** `" + str("{:,}".format(round(totals[11]["sum"] / 20)).replace(',', '.')) + "`\n"
    string += "** Nivel: ** `" + str(round(totals[10]["sum"] / 20)) + "`\n"

    string += ""

    return string


def total(player_id: int) -> Total:
    response = requests.get('https://api.opendota.com/api/players/' + str(player_id) + '/totals')
    totals = json.loads(response.text)

    total_obj = Total(titulo="Totales de " + get_nick(player_id), thumbnail=get_avatar_url(player_id),
                      kills=str("{:,}".format(totals[0]["sum"]).replace(',', '.')),
                      muertes=str("{:,}".format(totals[1]["sum"]).replace(',', '.')),
                      assists=str("{:,}".format(totals[2]["sum"]).replace(',', '.')),
                      lh=str("{:,}".format(totals[6]["sum"]).replace(',', '.')),
                      denegados=str("{:,}".format(totals[7]["sum"]).replace(',', '.')),
                      dano=str("{:,}".format(totals[11]["sum"]).replace(',', '.')))

    return total_obj


def wins_rank(players: dict) -> str:
    rank_list = []

    for player in players:
        r = requests.get('https://api.opendota.com/api/players/' + str(players[player]) + '/wl?date=7')
        wins = json.loads(r.text)["win"]

        try:
            player_name = get_nick(players[player])
        except KeyError:
            continue

        rank_list.append((player_name, str(wins)))

    rank_list.sort(key=lambda t: int(t[1]), reverse=True)

    string = "**Top victorias (5 dias) \n"
    string += ("-" * 30) + "** \n"

    string += ":first_place: **`" + rank_list[0][1] + " wins`** --> **" + str(rank_list[0][0]) + "** \n"
    string += ":second_place: **`" + rank_list[1][1] + " wins`** --> **" + str(rank_list[1][0]) + "** \n"
    string += ":third_place: **`" + rank_list[2][1] + " wins`** --> **" + str(rank_list[2][0]) + "** \n"
    string += "       **`" + rank_list[3][1] + " wins`** --> **" + str(rank_list[3][0]) + "** \n"
    string += "       **`" + rank_list[4][1] + " wins`** --> **" + str(rank_list[4][0]) + "** \n"
    string += "       **`" + rank_list[5][1] + " wins`** --> **" + str(rank_list[5][0]) + "** \n"

    return string
