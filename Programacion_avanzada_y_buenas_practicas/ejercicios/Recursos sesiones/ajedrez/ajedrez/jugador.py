class Jugador:
    ELO_INICIAL = 1200
    total_registrados = 0

    def __init__(self, nombre, pais):
        self.nombre = nombre
        self.pais = pais
        self.elo = Jugador.ELO_INICIAL
        self.victorias = 0
        self.derrotas = 0
        self.tablas = 0
        self.historial = []
        Jugador.total_registrados += 1

    @staticmethod
    def variacion_elo(puntos, k):
        if puntos == 1:
            return k
        elif puntos == 0:
            return -k
        else:
            return 0

    def actualizar_elo(self, puntos, k):
        self.elo += self.variacion_elo(puntos, k)

    def partidas_jugadas(self):
        return self.victorias + self.derrotas + self.tablas

    def porcentaje_victorias(self):
        total = self.partidas_jugadas()
        return 100 * self.victorias / total if total else 0.0

    def registrar_resultado(self, puntos):
        if puntos == 1:
            self.victorias += 1
        elif puntos == 0:
            self.derrotas += 1
        else:
            self.tablas += 1

    def resumen(self):
        return (
            f"{self.nombre:<8} ({self.pais})  ELO {self.elo}  "
            f"| {self.victorias}V {self.derrotas}D {self.tablas}T "
            f"| {self.porcentaje_victorias():.0f}% victorias"
        )