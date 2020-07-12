class Last:
    def __init__(self, hero="", title="", wl="", kda="", duracion="", lh="", opm="", epm="", dano="", dano_t="", curacion="", time_ago="", hero_img="", hero_icon=""):
        self.__hero__name = hero
        self.__title = title
        self.__wl = wl
        self.__kda = kda
        self.__duracion = duracion
        self.__lh = lh
        self.__opm = opm
        self.__epm = epm
        self.__dano = dano
        self.__dano_t = dano_t
        self.__curacion = curacion
        self.__time_ago = time_ago
        self.__hero_img = hero_img
        self.__hero_icon = hero_icon

    def get_title(self) -> str:
        return self.__title

    def set_title(self, title: str):
        self.__title = title

    def get_wl(self) -> str:
        return self.__wl

    def set_wl(self, wl: str):
        self.__wl = wl

    def get_kda(self) -> str:
        return self.__kda

    def set_kda(self, kda: str):
        self.__kda = kda

    def get_duracion(self) -> str:
        return self.__duracion

    def set_duracion(self, duracion: str):
        self.__duracion = duracion

    def get_lh(self) -> str:
        return self.__lh

    def set_lh(self, lh: str):
        self.__lh = lh

    def get_opm(self) -> str:
        return self.__opm

    def set_opm(self, opm: str):
        self.__opm = opm

    def get_epm(self) -> str:
        return self.__epm

    def set_epm(self, epm: str):
        self.__epm = epm

    def get_dano(self) -> str:
        return self.__dano

    def set_dano(self, dano: str):
        self.__dano = dano

    def get_dano_t(self) -> str:
        return self.__dano_t

    def set_dano_t(self, dano_t: str):
        self.__dano_t = dano_t

    def get_curacion(self) -> str:
        return self.__curacion

    def set_curacion(self, curacion: str):
        self.__curacion = curacion

    def get_hero_icon(self) -> str:
        return self.__hero_icon

    def set_hero_icon(self, hero_icon: str):
        self.__hero_icon = hero_icon

    def get_hero_img(self) -> str:
        return self.__hero_img

    def set_hero_img(self, hero_img: str):
        self.__hero_img = hero_img

    def get_hero_name(self) -> str:
        return self.__hero__name

    def set_hero_name(self, hero_name: str):
        self.__hero__name = hero_name

    def get_time_ago(self):
        return self.__time_ago

    def set_time_ago(self, time_ago):
        self.__time_ago = time_ago


class Total:
    def __init__(self, titulo, thumbnail, kills, muertes, assists, lh, denegados, dano, total_games=0, winrate=0):
        self.__titulo = titulo
        self.__thumbnail = thumbnail
        self.__kills = kills
        self.__muertes = muertes
        self.__assists = assists
        self.__lh = lh
        self.__denegados = denegados
        self.__dano = dano
        self.__total__games = total_games
        self.__winrate = winrate

    def get_titulo(self):
        return self.__titulo

    def get_thumbnail(self):
        return self.__thumbnail

    def get_kills(self):
        return self.__kills

    def get_muertes(self):
        return self.__muertes

    def get_assists(self):
        return self.__assists

    def get_lh(self):
        return self.__lh

    def get_denegados(self):
        return self.__denegados

    def get_dano(self):
        return self.__dano

    def get_total_games(self):
        return self.__total__games

    def get_winrate(self):
        return self.__winrate


class Avg(Total):
    def __init__(self, titulo, thumbnail, kills, muertes, assists, lh, denegados, dano, nivel, opm, epm):
        super().__init__(titulo, thumbnail, kills, muertes, assists, lh, denegados, dano)
        self.__nivel = nivel
        self.__opm = opm
        self.__epm = epm

    def get_opm(self):
        return self.__opm

    def get_epm(self):
        return self.__epm

    def get_nivel(self):
        return self.__nivel


class Stats:
    def __init__(self, titulo, thumbnail, game0, game1, game2, game3, game4):
        self.__titulo = titulo
        self.__thumbnail = thumbnail
        self.__game0 = game0
        self.__game1 = game1
        self.__game2 = game2
        self.__game3 = game3
        self.__game4 = game4
        self.__delimiter = "-" * 60
        self.__descripcion = "Partidas recientes de este noob"


    def get_titulo(self):
        return self.__titulo

    def get_thumbnail(self):
        return self.__thumbnail

    def get_game(self, n):
        if n == 0:
            return self.__game0
        elif n == 1:
            return self.__game1
        elif n == 2:
            return self.__game2
        elif n == 3:
            return self.__game3
        else:
            return self.__game4

    def get_delimiter(self):
        return self.__delimiter

    def get_descripcion(self):
        return self.__descripcion
