import json
import requests
import time
from objects import Last, Total, Avg, Stats
from dotenv import load_dotenv
import os


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

    if player_id == 145875771:
        return "statham"

    response = requests.get('https://api.opendota.com/api/players/' + str(player_id))
    profile = json.loads(response.text)

    return profile["profile"]["personaname"]


def get_avatar_url(player_id: int):
    if player_id == 275221784:
        return "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/b6" \
               "/b61deaa03441b6a4c3c641f9ca2eff76c94a2154_full.jpg "

    if player_id == 145875771:
        return "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/81" \
               "/81dcd9de02c6d4859b9f6f8f6cb3342bc49d6fcf_full.jpg "

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


def stats(player_id: int) -> Stats:
    response = requests.get('https://api.opendota.com/api/players/' + str(player_id) + '/recentMatches')
    recent_matches = json.loads(response.text)
    games = []

    for i in range(0, 5, 1):
        match = recent_matches[i]
        radiant = is_radiant(match["player_slot"])
        string = ":green_circle:   Gano" if radiant == match["radiant_win"] else ":red_circle:   Perdio"
        string += " con "
        string += HERO_DICT[match["hero_id"]] + " y salio "
        string += str(match["kills"]) + '/' + str(match["deaths"]) + '/' + str(match["assists"])

        games.append(string)

    stats_obj = Stats(titulo="Ultimos 5 games de " + get_nick(player_id), thumbnail=get_avatar_url(player_id),
                      game0=games[0], game1=games[1], game2=games[2], game3=games[3], game4=games[4])

    return stats_obj


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
    string += "**`!on`** ---> muestra una lista de los pibes que estan jugando Dota 2 en este momento\n"

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


def get_winrate(player_id: int) -> str:
    response = requests.get('https://api.opendota.com/api/players/' + str(player_id) + '/wl')
    wl = json.loads(response.text)
    return str(round((wl["win"] / (wl["lose"] + wl["win"])) * 100, 2)).replace('.', ',') + "%"


def get_build(match_id: int, player_slot: int) -> list:
    r = requests.get("https://api.opendota.com/api/matches/" + str(match_id))
    full_match = json.loads(r.text)
    build = []

    for player_n in full_match["players"]:
        if player_n["player_slot"] == player_slot:
            build.append(player_n["item_0"])
            build.append(player_n["item_1"])
            build.append(player_n["item_2"])
            build.append(player_n["item_3"])
            build.append(player_n["item_4"])
            build.append(player_n["item_5"])

            return build


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
    last_game.set_build(get_build(match["match_id"], match["player_slot"]))

    return last_game


def avg(player_id: int) -> Avg:
    response = requests.get('https://api.opendota.com/api/players/' + str(player_id) + '/totals?limit=20')
    totals = json.loads(response.text)

    avg_obj = Avg(titulo="Promedios de " + get_nick(player_id), thumbnail=get_avatar_url(player_id),
                  kills=str(totals[0]["sum"] / 20).replace('.', ','),
                  muertes=str(totals[1]["sum"] / 20).replace('.', ','),
                  assists=str(totals[2]["sum"] / 20).replace('.', ','),
                  opm=str(round(totals[4]["sum"] / 20)),
                  epm=str(round(totals[5]["sum"] / 20)),
                  lh=str(round(totals[6]["sum"] / 20)),
                  denegados=str(round(totals[7]["sum"] / 20)),
                  dano=str("{:,}".format(round(totals[11]["sum"] / 20)).replace(',', '.')),
                  nivel=str(round(totals[10]["sum"] / 20)))

    return avg_obj


def total(player_id: int) -> Total:
    response = requests.get('https://api.opendota.com/api/players/' + str(player_id) + '/totals')
    totals = json.loads(response.text)

    total_obj = Total(titulo="Totales de " + get_nick(player_id), thumbnail=get_avatar_url(player_id),
                      kills=str("{:,}".format(totals[0]["sum"]).replace(',', '.')),
                      muertes=str("{:,}".format(totals[1]["sum"]).replace(',', '.')),
                      assists=str("{:,}".format(totals[2]["sum"]).replace(',', '.')),
                      lh=str("{:,}".format(totals[6]["sum"]).replace(',', '.')),
                      denegados=str("{:,}".format(totals[7]["sum"]).replace(',', '.')),
                      dano=str("{:,}".format(totals[11]["sum"]).replace(',', '.')),
                      total_games=str("{:,}".format(totals[0]["n"]).replace(',', '.')),
                      winrate=get_winrate(player_id))

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


def get_joke() -> dict:
    r = requests.get("https://sv443.net/jokeapi/v2/joke/Miscellaneous,Dark")
    joke = json.loads(r.text)

    return joke


def get_playerssummary_url():
    with open("steam_ids.json", 'r') as fd:
        load_dotenv()
        base_url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + os.getenv(
            "STEAM_APIKEY") + "&steamids="
        my_players_dict = json.loads(fd.read())

        for idx, player in enumerate(my_players_dict["players"]):
            if idx == len(my_players_dict["players"]) - 1:
                base_url += str(player["steam_id"])
                break

            base_url += str(player["steam_id"]) + ","
        return base_url


base_url = get_playerssummary_url()


def get_on() -> list:
    r = requests.get(base_url)
    actual_players_dict = json.loads(r.text)["response"]

    online_players_nick = []

    for player_data in actual_players_dict["players"]:
        if player_data["personastate"] == 0 or "gameextrainfo" not in player_data:
            continue

        elif player_data["gameextrainfo"] != "Dota 2":
            continue

        online_players_nick.append(player_data["personaname"])

    return online_players_nick
