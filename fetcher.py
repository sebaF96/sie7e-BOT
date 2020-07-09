import json
import requests


def get_hero_dict() -> dict:
    response = requests.get('https://api.opendota.com/api/heroes')
    full_hero_dict = json.loads(response.text)
    min_hero_dict = {}

    for hero in full_hero_dict:
        min_hero_dict[hero["id"]] = hero["localized_name"]

    return min_hero_dict


HERO_DICT = get_hero_dict()


def get_nick(player_id: int):
    response = requests.get('https://api.opendota.com/api/players/' + str(player_id))
    profile = json.loads(response.text)

    return profile["profile"]["personaname"]


def is_radiant(player_slot: int) -> bool:
    return 0 <= player_slot <= 127


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
    string += "**`!last <player>`** ---> muestra la ultima partida de ese player"


    return string

