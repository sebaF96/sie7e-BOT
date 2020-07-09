import json
import requests


def is_radiant(player_slot: int) -> bool:
    return 0 <= player_slot <= 128



def fetch(player_id: int) -> str:
    response = requests.get('https://api.opendota.com/api/players/' + str(player_id) + '/recentMatches')
    recent_matches = json.loads(response.text)

    for i in range(5):
        radiant = is_radiant(recent_matches[i]["player_slot"])
        wl = "Gano" if radiant == recent_matches[i]["radiant_win"] else "Perdio"
        print(wl, end="  ")
        print(str(recent_matches[i]["kills"]) + '/' + str(recent_matches[i]["deaths"]) + '/' + str(recent_matches[i]["assists"]))


fetch(134129467)