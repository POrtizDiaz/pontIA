class Jugador:
    ELO_INICIAL = 1200
    total_registrados = 0

    def __init__(self, nombre, pais):
        self.nombre = nombre
        self.pais = pais
        self._elo = Jugador.ELO_INICIAL
        self.victorias = 0
        self.derrotas = 0
        self.tablas = 0
        self.historial = []
        Jugador.total_registrados += 1

    @classmethod
    def desde_dict(cls, datos: dict):
        jugador = cls(datos["nombre"], datos["pais"])
        jugador._elo = datos["elo"]
        jugador.victorias = datos["victorias"]
        jugador.derrotas = datos["derrotas"]
        jugador.tablas = datos["tablas"]
        return jugador

    def a_dict(self) -> dict:
        return {
            "nombre": self.nombre,
            "pais": self.pais,
            "elo": self.elo,
            "victorias": self.victorias,
            "derrotas": self.derrotas,
            "tablas": self.tablas,
        }

    def __repr__(self):
        return f"Jugador({self.nombre!r}, {self.pais!r}, elo={self.elo})"

    def __str__(self):
        return (
            f"{self.nombre:<8} ({self.pais})  ELO {self.elo}  "
            f"| {self.victorias}V {self.derrotas}D {self.tablas}T "
            f"| {self.porcentaje_victorias:.0f}% victorias"
        )

    def __lt__(self, otro):
        return self.elo < otro.elo

    @staticmethod
    def variacion_elo(puntos, k):
        if puntos == 1:
            return k
        elif puntos == 0:
            return -k
        else:
            return 0

    def actualizar_elo(self, puntos, k):
        self._elo += self.variacion_elo(puntos, k)

    @property
    def partidas_jugadas(self):
        return self.victorias + self.derrotas + self.tablas

    @property
    def porcentaje_victorias(self):
        total = self.partidas_jugadas
        return 100 * self.victorias / total if total else 0.0

    def registrar_resultado(self, puntos):
        if puntos == 1:
            self.victorias += 1
        elif puntos == 0:
            self.derrotas += 1
        else:
            self.tablas += 1

    @property
    def elo(self):
        return self._elo
