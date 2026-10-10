# Puntos (blancas, negras) para cada resultado posible
from ajedrez.excepciones import PartidaInvalida

RESULTADOS = {"1-0": (1, 0), "0-1": (0, 1), "1/2-1/2": (0.5, 0.5)}


class Partida:
    def __init__(self, blancas, negras, resultado, ritmo):
        if resultado not in RESULTADOS:
            raise ValueError(f"Resultado inválido: {resultado}")
        if blancas is negras:
            raise PartidaInvalida(blancas, negras)
        self.blancas = blancas
        self.negras = negras
        self.resultado = resultado
        self.ritmo = ritmo

    def puntos(self):
        return RESULTADOS[self.resultado]

    def rival_de(self, jugador):
        return self.negras if jugador is self.blancas else self.blancas

    def color_de(self, jugador):
        return "blancas" if jugador is self.blancas else "negras"

    def describir_para(self, jugador):
        rival = self.rival_de(jugador)
        return (
            f"vs {rival.nombre:<8} con {self.color_de(jugador):<8} "
            f"{self.resultado:<8} [{self.ritmo.describir()}]"
        )