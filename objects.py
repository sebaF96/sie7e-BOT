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

