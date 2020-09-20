import requests
import json
import os
from constants import Constants

HEADERS = {'client-id': os.getenv('TWITCH_CLIENT'), 'Authorization': f"Bearer {os.getenv('TWITCH_OAUTH')}"}


def get_profile_image(streamer_channel):
    r = requests.get(Constants.HELIX_BASE_URL.value + f'users?login={streamer_channel}', headers=HEADERS)
    return json.loads(r.text)['data'][0]['profile_image_url']


def get_stream_info(streamer_channel):
    r = requests.get(Constants.HELIX_BASE_URL.value + f'streams?user_login={streamer_channel}', headers=HEADERS)
    data = json.loads(r.text)['data'][0]
    data['thumbnail_url'] = data['thumbnail_url'].replace('{width}', '388').replace('{height}', '219')
    #  print(data['thumbnail_url'].replace('{width}', '388').replace('{height}', '219'))
    return data


def get_game_info(game_id):
    r = requests.get(Constants.HELIX_BASE_URL.value + f'games?id={game_id}', headers=HEADERS)
    data = json.loads(r.text)['data'][0]
    game_photo_url = data['box_art_url'].replace('{width}', '189').replace('{height}', '252')
    game_name = data['name']

    return game_name, game_photo_url


class LiveStream:
    def __init__(self, streamer_channel):
        stream_info = get_stream_info(streamer_channel)

        self.__url = Constants.TWITCH_BASE_URL.value + streamer_channel
        self.__channel_name = streamer_channel
        self.__channel_photo_url = get_profile_image(streamer_channel)
        self.__title = stream_info['title']
        self.__viewers = stream_info['viewer_count']
        self.__thumbnail_url = stream_info['thumbnail_url']
        self.__game_id = stream_info['game_id']
        self.__game_name = get_game_info(self.__game_id)[0]
        self.__game_photo_url = get_game_info(self.__game_id)[1]


    @property
    def url(self):
        return self.__url

    @property
    def channel_name(self):
        return self.__channel_name

    @property
    def channel_photo_url(self):
        return self.__channel_photo_url

    @property
    def title(self):
        return self.__title

    @property
    def viewers(self):
        return self.__viewers

    @property
    def thumbnail_url(self):
        return self.__thumbnail_url

    @property
    def game_name(self):
        return self.__game_name

    @property
    def game_photo_url(self):
        return self.__game_photo_url


def is_live(streamer_channel: str) -> bool:
    response = requests.get(Constants.HELIX_BASE_URL.value + f'search/channels?query={streamer_channel}&first=1',
                            headers=HEADERS)

    response = json.loads(response.text)['data'][0]

    return response['is_live']


if __name__ == '__main__':
    channel = input('Channel name: ')
    stream = LiveStream(channel)

    print(stream.title)
    print(stream.game_name)
    print(stream.channel_photo_url)
    print(stream.thumbnail_url)
