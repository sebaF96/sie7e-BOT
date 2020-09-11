from enum import Enum
from config import STEAM_APIKEY


class Constants(Enum):
    FOOTER_TEXT = "Cortesia de sie7e-BOT"
    FOOTER_IMAGE_URL = "https://steamcdn-a.akamaihd.net/apps/dota2/images/heroes/rattletrap_icon.png"
    PLAYER_NOT_RECOGNIZED = "Ni idea quien es ese. Tira !players para ver los que conozco"
    PRIVATE_PROFILE = "Tiene el perfil privado esa caquita"
    STEAM_IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/1024px" \
                      "-Steam_icon_logo.svg.png "
    DOTA2_IMAGE_URL = "https://deadlysurprise.github.io/d2LoadingScreens/d2logo.png"

    HELP_MESSAGE = """** COMANDOS **
    **`!help`** --> muestra este mensaje
    **`!players`** --> muestra los players de los q podes ver la data
    **`!stats <player>`** --> muestra las ultimas 5 partidas de ese player
    **`!wl <player>`** --> muestra el W - L de las ultimas 20 partidas de ese player
    **`!refresh <player>`** --> actualiza las estadisticas de ese player
    **`!last <player>`** ---> muestra la ultima partida de ese player
    **`!avg <player>`** ---> muestra las estadisticas de ese player (ultimas 20 partidas)
    **`!total <player>`** ---> muestra los totales de ese player
    **`!records <player>`** ---> muestra los records de ese player en distintos games
    **`!wins`** ---> muestra un ranking de los mas ganadores en los ultimos 7 dias
    **`!on`** ---> muestra una lista de los pibes que estan jugando Dota 2 en este momento
    **`!vicio`** ---> ranking de partidas jugadas hoy y en la semana
    **`!lp`** ---> muestra los players que han jugado mas recientemente """


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

    # Steam
    HEROPICTURE_BASE_URL = "https://steamcdn-a.akamaihd.net"
    STEAM_API_URL = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + STEAM_APIKEY + "&steamids="
