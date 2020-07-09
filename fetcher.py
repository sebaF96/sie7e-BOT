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


def is_radiant(player_slot: int) -> bool:
    return 0 <= player_slot <= 128


def stats(player_id: int) -> str:
    response = requests.get('https://api.opendota.com/api/players/' + str(player_id) + '/recentMatches')
    recent_matches = json.loads(response.text)

    for match in recent_matches[:5]:
        radiant = is_radiant(match["player_slot"])
        wl = "Gano" if radiant == match["radiant_win"] else "Perdio"
        print(wl, end="  ")
        print(HERO_DICT[match["hero_id"]], end="  ")
        print(str(match["kills"]) + '/' + str(match["deaths"]) + '/' + str(match["assists"]))


stats(134129467)
