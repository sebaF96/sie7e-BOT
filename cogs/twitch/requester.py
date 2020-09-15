import requests
import json
import os

HEADERS = {'client-id': os.getenv('TWITCH_CLIENT'), 'Authorization': os.getenv('TWITCH_OAUTH')}
NICO_ID = 457947320
PANCHO_ID = 200690631


TITLE = ""
GAME_NAME = ""
VIEWERS_COUNT = ""
PLAYER_PROFILE_URL = ""
GAME_ID = 0
GAME_PHOTO_URL = ""


def is_live(channel_name: str) -> bool:
    response = requests.get(f'https://api.twitch.tv/helix/search/channels?query={channel_name}&first=1',
                            headers=HEADERS)

    response = json.loads(response.text)['data'][0]

    return response['is_live']


def get_stream_info(stramer_id):
    r = requests.get(f'https://api.twitch.tv/helix/streams?user_login={stramer_id}', headers=HEADERS)
    data = json.loads(r.text)
    return data


if __name__ == '__main__':
    channel = input('Channel name: ')
    print(is_live(channel))
    print('\n\n')
    print(get_stream_info(channel))
