from enum import Enum


class Constants(Enum):
    FOOTER_TEXT = "Cortesia de sie7e-BOT"
    FOOTER_IMAGE_URL = "https://steamcdn-a.akamaihd.net/apps/dota2/images/heroes/rattletrap_icon.png"
    PLAYER_NOT_RECOGNIZED = "Ni idea quien es ese. Tira !players para ver los que conozco"
    PRIVATE_PROFILE = "Tiene el perfil privado esa caquita"
    STEAM_IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/1024px" \
                      "-Steam_icon_logo.svg.png "
    DOTA2_IMAGE_URL = "https://deadlysurprise.github.io/d2LoadingScreens/d2logo.png"
    ADMIN_PRIVATE_CHANNEL = 730953382935920745
    AMONG_US_CHANNEL = 747932473958072361
    MUTED_ROLE_ID = 748248561501601864

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