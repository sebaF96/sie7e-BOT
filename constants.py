from enum import Enum
import os


class Constants(Enum):
    FOOTER_TEXT = "Cortesia de sie7e-BOT"
    FOOTER_IMAGE_URL = "https://steamcdn-a.akamaihd.net/apps/dota2/images/heroes/rattletrap_icon.png"
    PLAYER_NOT_RECOGNIZED = "Ni idea quien es ese. Tira !players para ver los que conozco"
    PRIVATE_PROFILE = "Tiene el perfil privado esa caquita"
    STEAM_IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/1024px" \
                      "-Steam_icon_logo.svg.png "
    DOTA2_IMAGE_URL = "https://deadlysurprise.github.io/d2LoadingScreens/d2logo.png"
    AMONG_US_IMAGE_URL = "https://cdn.discordapp.com/app-assets/477175586805252107/481347538054545418.png"
    TWITCH_BASE_URL = "https://www.twitch.tv/"
    HELIX_BASE_URL = "https://api.twitch.tv/helix/"

    HELP_COMMANDS = {"!serverinfo": "muestra informacion acerca del servidor",
                     "!userinfo <user>": "muestra informacion tuya o del usuario que mencionas con @",
                     "!stats <player>": "muestra las ultimas 5 partidas de ese player",
                     "!wl <player>": "muestra el W - L de las ultimas 20 partidas de ese player",
                     "!refresh <player>": "actualiza las estadisticas de ese player",
                     "!last <player>": "muestra la ultima partida de ese player",
                     "!avg <player>": "muestra las estadisticas de ese player (ultimas 20 partidas)",
                     "!total <player>": "muestra los totales de ese player",
                     "!records <player>": "muestra los records de ese player en distintos games",
                     "!wins": "muestra un ranking de los mas ganadores en los ultimos 7 dias",
                     "!on": "muestra una lista de los pibes que estan jugando Dota 2 en este momento",
                     "!vicio": "ranking de partidas jugadas hoy y en la semana",
                     "!lp": "muestra los players que han jugado mas recientemente"}


class Fetcher(Enum):
    # OpenDota API
    API_HEROES_URL = "https://api.opendota.com/api/heroes"
    API_PLAYERS_URL = "https://api.opendota.com/api/players/"
    API_MATCHES_URL = "https://api.opendota.com/api/matches/"
    RECORDS_URL_TAIL = "/matches?project=xp_per_min&project=gold_per_min&project=tower_damage&project=hero_damage" \
                       "&project=last_hits&project=start_time&project=kills&project=hero_id&project=denies&project" \
                       "=assists&project=deaths&project=hero_healing"

    # DotaConstants RAW data
    DOTACONSTANTS_HEROES_URL = "https://raw.githubusercontent.com/odota/dotaconstants/master/build/heroes.json"
    DOTACONSTANTS_ITEMS_URL = "https://raw.githubusercontent.com/odota/dotaconstants/master/build/items.json"

    # Steam
    HEROPICTURE_BASE_URL = "https://steamcdn-a.akamaihd.net"
    STEAM_API_URL = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + os.getenv('STEAM_APIKEY') + "&steamids="
