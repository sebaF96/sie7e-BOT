import json
import requests
import time
from multiprocessing import Queue, Process
from cogs.dota.dota_models import Last, Total, Avg, Stats, Records
from constants import Fetcher as FConstants


def get_hero_dict() -> dict:
    response = requests.get(FConstants.API_HEROES_URL.value)
    full_hero_dict = json.loads(response.text)
    min_hero_dict = {}

    for hero in full_hero_dict:
        min_hero_dict[hero["id"]] = hero["localized_name"]

    return min_hero_dict


def get_hero_picture(icon=False) -> dict:
    response = requests.get(FConstants.DOTACONSTANTS_HEROES_URL.value)
    full_hero_dict = json.loads(response.text)
    base_url = FConstants.HEROPICTURE_BASE_URL.value

    min_hero_dict = {}

    if icon:
        for hero in full_hero_dict:
            min_hero_dict[int(full_hero_dict[hero]["id"])] = base_url + str(full_hero_dict[hero]['icon'])

        # Void Spirit icon in original URL is bugged, OpenDota web is using this url
        min_hero_dict[126] = "https://www.opendota.com/assets/images/dota2/heroes/126_icon.png"
        # SnapFire icon in original URL is bugged, OpenDota web is using this url
        min_hero_dict[128] = "https://www.opendota.com/assets/images/dota2/heroes/128_icon.png"

    else:
        for hero in full_hero_dict:
            min_hero_dict[int(full_hero_dict[hero]["id"])] = base_url + str(full_hero_dict[hero]['img'])

    return min_hero_dict


HERO_DICT = get_hero_dict()
HERO_PICTURE = get_hero_picture()
HERO_ICON = get_hero_picture(icon=True)


def get_player_steamid(player_id: int):
    response = requests.get(FConstants.API_PLAYERS_URL.value + str(player_id))
    steam_id = json.loads(response.text)["profile"]["steamid"]

    return steam_id


def get_nick(player_id: int):
    steam_api_url = FConstants.STEAM_API_URL.value
    steam_id = get_player_steamid(player_id)
    response = requests.get(steam_api_url + str(steam_id))
    steam_profile = json.loads(response.text)

    return steam_profile["response"]["players"][0]["personaname"]


def get_avatar_url(player_id: int):
    steam_api_url = FConstants.STEAM_API_URL.value

    steam_id = get_player_steamid(player_id)
    response = requests.get(steam_api_url + str(steam_id))
    steam_profile = json.loads(response.text)

    return steam_profile["response"]["players"][0]["avatarfull"]


def get_rank(player_id: int):
    odota_api_url = FConstants.API_PLAYERS_URL.value + str(player_id)
    odota_profile = json.loads(requests.get(odota_api_url).text)

    return odota_profile['rank_tier']


def is_radiant(player_slot: int) -> bool:
    return 0 <= player_slot <= 127


def format_duration(duration: int) -> str:
    seconds = duration % 60
    minutes = (duration - seconds) // 60
    if seconds < 10:
        seconds = '0' + str(seconds)

    return f"{minutes}:{seconds}"


def format_time_ago(timestamp):
    time_now = int(time.time())
    time_ago = time_now - timestamp - 500

    if time_ago < 0:
        return "recien."

    if time_ago >= 86400:
        days = round(time_ago / 86400)
        return f"hace {days}d aprox."

    if time_ago >= 3600:
        hours = round(time_ago / 3600)
        return f"hace {hours}h aprox."

    if time_ago >= 60:
        minutes = int(time_ago / 60)
        return f"hace {minutes} min aprox."

    return f"hace {time_ago} seg aprox."


def stats(player_id: int) -> Stats:
    response = requests.get(FConstants.API_PLAYERS_URL.value + str(player_id) + '/recentMatches')
    recent_matches = json.loads(response.text)
    # 4 is single draft, 22 all draft 
    recent_matches = [m for m in recent_matches if m["game_mode"] in [4, 22]]
    games = []

    for i in range(0, 5, 1):
        match = recent_matches[i]
        radiant = is_radiant(match["player_slot"])
        result = ":green_circle:   Gano" if radiant == match["radiant_win"] else ":red_circle:   Perdio"
        string = f"{result} con {HERO_DICT[match['hero_id']]} y salio {match['kills']}/{match['deaths']}/{match['assists']}"

        games.append(string)

    stats_obj = Stats(titulo="Ultimos 5 games de " + get_nick(player_id), thumbnail=get_avatar_url(player_id),
                      game0=games[0], game1=games[1], game2=games[2], game3=games[3], game4=games[4])

    return stats_obj


def refresh(player_id: int):
    requests.post(FConstants.API_PLAYERS_URL.value + str(player_id) + '/refresh')


def w_l(player_id: int) -> str:
    response = requests.get(FConstants.API_PLAYERS_URL.value + str(player_id) + '/wl?limit=20')
    wl = json.loads(response.text)
    wins = wl["win"]
    defeats = wl["lose"]

    string = "W - L de " + get_nick(player_id) + ": **" + str(wins) + " - " + str(defeats) + "**"

    return string


def get_winrate(player_id: int) -> str:
    response = requests.get(FConstants.API_PLAYERS_URL.value + str(player_id) + '/wl')
    wl = json.loads(response.text)
    return str(round((wl["win"] / (wl["lose"] + wl["win"])) * 100, 2)).replace('.', ',') + "%"


def get_build(match_id: int, player_slot: int) -> list:
    r = requests.get(FConstants.API_MATCHES_URL.value + str(match_id))
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
    response = requests.get(FConstants.API_PLAYERS_URL.value + str(player_id) + '/recentMatches')
    recent_matches = json.loads(response.text)
    # 4 is single draft, 22 all draft
    recent_matches = [m for m in recent_matches if m["game_mode"] in [4, 22]]
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
    response = requests.get(FConstants.API_PLAYERS_URL.value + str(player_id) + '/totals?limit=20')
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
    response = requests.get(FConstants.API_PLAYERS_URL.value + str(player_id) + '/totals')
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


def fetch_wins(player_id, queue, date):
    r = requests.get(FConstants.API_PLAYERS_URL.value + str(player_id) + '/wl?date=' + date)
    wins = json.loads(r.text)["win"]

    try:
        player_name = get_nick(player_id)
        queue.put((player_name, str(wins)))
    except KeyError:
        pass


def wins_rank(players: dict, daily=False) -> str:
    date = "7" if not daily else "1"
    processes_list = []
    rank_list = []
    queue = Queue()

    for player in players:
        process = Process(target=fetch_wins, args=(players[player], queue, date))
        process.start()
        processes_list.append(process)

    for p in processes_list:
        p.join()

    while not queue.empty():
        rank_list.append(queue.get())

    rank_list.sort(key=lambda t: int(t[1]), reverse=True)

    string = "**Top victorias (7 dias) \n" if not daily else ":trophy:   **Top victorias HOY   :trophy: \n"
    string += ("-" * 30) + "** \n"

    string += ":first_place: **`" + rank_list[0][1] + " wins`** --> **" + str(rank_list[0][0]) + "** \n"
    string += ":second_place: **`" + rank_list[1][1] + " wins`** --> **" + str(rank_list[1][0]) + "** \n"
    string += ":third_place: **`" + rank_list[2][1] + " wins`** --> **" + str(rank_list[2][0]) + "** \n"
    string += "       **`" + rank_list[3][1] + " wins`** --> **" + str(rank_list[3][0]) + "** \n"

    if daily:
        winners_nick = [p[0] for p in rank_list if p[1] == rank_list[0][1]]
        string += "\n\n\n"
        for p in winners_nick:
            string += "**Well played " + p + "!** \n"

    return string


def get_playerssummary_url():
    with open("cogs/dota/players.json", 'r') as fd:
        base_url = FConstants.STEAM_API_URL.value
        my_players_dict = json.loads(fd.read())

        for idx, player_name in enumerate(my_players_dict):
            player_steam_id = get_player_steamid(my_players_dict[player_name])
            if idx == len(my_players_dict) - 1:
                base_url += str(player_steam_id)
                break

            base_url += str(player_steam_id) + ","
        return base_url


def get_on() -> (list, list):
    r = requests.get(get_playerssummary_url())
    actual_players_dict = json.loads(r.text)["response"]

    dota_players_nick = []
    online_players_nick = []

    for player_data in actual_players_dict["players"]:
        if player_data["personastate"] == 0:
            continue

        elif "gameextrainfo" not in player_data or player_data["gameextrainfo"] != "Dota 2":
            online_players_nick.append(player_data["personaname"])
        else:
            dota_players_nick.append(player_data["personaname"])

    return dota_players_nick, online_players_nick


def get_individual_vicio(player_id, queue_semana, queue_hoy):
    r = requests.get(FConstants.API_PLAYERS_URL.value + str(player_id) + '/wl?date=7')
    games_semana = json.loads(r.text)["win"] + json.loads(r.text)["lose"]

    if games_semana <= 3:
        return

    r = requests.get(FConstants.API_PLAYERS_URL.value + str(player_id) + '/wl?date=1')
    games_hoy = json.loads(r.text)["win"] + json.loads(r.text)["lose"]

    try:
        player_name = get_nick(player_id)
        queue_semana.put((player_name, games_semana))
        queue_hoy.put((player_name, games_hoy))
    except KeyError:
        pass


def get_vicios(players):
    vicios_hoy, vicios_semana, processes_list = [], [], []
    queue_semana, queue_hoy = Queue(), Queue()

    for player in players:
        process = Process(target=get_individual_vicio, args=(players[player], queue_semana, queue_hoy))
        process.start()
        processes_list.append(process)

    for p in processes_list:
        p.join()

    while not queue_hoy.empty():
        vicios_hoy.append(queue_hoy.get())

    # Using 2 individuals whiles for preventing some kind of error if one player is
    # inserted in one Queue and not in the another one

    while not queue_semana.empty():
        vicios_semana.append(queue_semana.get())

    vicios_semana.sort(key=lambda x: x[1], reverse=True)
    vicios_hoy.sort(key=lambda x: x[1], reverse=True)

    return vicios_hoy[:4], vicios_semana[:4]


def get_records(player_id):
    record = Records(titulo=f"Records de {get_nick(player_id)}", thumbnail=get_avatar_url(player_id))

    url = FConstants.API_PLAYERS_URL.value + str(player_id) + FConstants.RECORDS_URL_TAIL.value

    games_list = json.loads(requests.get(url).text)

    kills_game = sorted(games_list, key=lambda x: x["kills"], reverse=True)[0]
    record.set_kills(f"{kills_game['kills']} ({HERO_DICT[kills_game['hero_id']]})")

    opm_game = sorted(games_list, key=lambda x: x["gold_per_min"], reverse=True)[0]
    record.set_opm(f"{opm_game['gold_per_min']} ({HERO_DICT[opm_game['hero_id']]})")

    epm_game = sorted(games_list, key=lambda x: x["xp_per_min"], reverse=True)[0]
    record.set_epm(f"{epm_game['xp_per_min']} ({HERO_DICT[epm_game['hero_id']]})")

    duration_game = sorted(games_list, key=lambda x: x["duration"], reverse=True)[0]
    record.set_duration(f"{format_duration(duration_game['duration'])} ({HERO_DICT[duration_game['hero_id']]})")

    assists_game = sorted(games_list, key=lambda x: x["assists"], reverse=True)[0]
    record.set_assists(f"{assists_game['assists']} ({HERO_DICT[assists_game['hero_id']]})")

    lh_game = sorted(games_list, key=lambda x: x["last_hits"], reverse=True)[0]
    record.set_last_hits(f"{lh_game['last_hits']} ({HERO_DICT[lh_game['hero_id']]})")

    damage_game = \
    sorted([g for g in games_list if g["hero_damage"] is not None], key=lambda x: x["hero_damage"], reverse=True)[0]
    record.set_hero_damage(str("{:,}".format(damage_game["hero_damage"]).replace(',', '.')) + " (" + HERO_DICT[
        damage_game["hero_id"]] + ")")

    tower_damage_game = \
    sorted([g for g in games_list if g["tower_damage"] is not None], key=lambda x: x["tower_damage"], reverse=True)[0]
    record.set_tower_damage(str("{:,}".format(tower_damage_game["tower_damage"]).replace(',', '.')) + " (" + HERO_DICT[
        tower_damage_game["hero_id"]] + ")")

    heal_game = \
    sorted([g for g in games_list if g["hero_healing"] is not None], key=lambda x: x["hero_healing"], reverse=True)[0]
    record.set_hero_healing(
        str("{:,}".format(heal_game["hero_healing"]).replace(',', '.')) + " (" + HERO_DICT[heal_game["hero_id"]] + ")")

    denies_game = sorted(games_list, key=lambda x: x["denies"], reverse=True)[0]
    record.set_denies(f"{denies_game['denies']} ({HERO_DICT[denies_game['hero_id']]})")

    return record


def get_player_last_time(player_id, queue):
    response = requests.get(FConstants.API_PLAYERS_URL.value + str(player_id) + '/recentMatches')
    recent_matches = json.loads(response.text)

    match = recent_matches[0]
    radiant = is_radiant(match['player_slot'])

    player_nick = ":green_circle:   " if radiant == match["radiant_win"] else ":red_circle:   "
    player_nick += get_nick(player_id)
    player_timestamp = match["start_time"] + match["duration"]
    player_time_ago = format_time_ago(player_timestamp)

    player_tuple = (player_nick, player_timestamp, player_time_ago)

    queue.put(player_tuple)


def get_last_played(players) -> list:
    queue = Queue()
    processes_list = []
    players_timestamps = []

    for player in players:
        process = Process(target=get_player_last_time, args=(players[player], queue))
        process.start()
        processes_list.append(process)

    for p in processes_list:
        p.join()

    while not queue.empty():
        players_timestamps.append(queue.get())

    players_timestamps.sort(key=lambda p: p[1], reverse=True)

    return players_timestamps[:5]
