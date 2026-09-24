from ajedrez.jugador import Jugador
from ajedrez.partida import Partida


class Plataforma:

    def __init__(self):
        self.jugadores = {}  # nombre -> Jugador
        self.partidas = []  # lista de Partida

    def registrar(self, nombre, pais):
        if nombre in self.jugadores:
            print(f"El jugador {nombre} ya existe")
            return
        self.jugadores[nombre] = Jugador(nombre, pais)

    def buscar(self, nombre):
        if nombre not in self.jugadores:
            raise ValueError(f"El jugador {nombre} no está registrado")
        return self.jugadores[nombre]

    def jugar(self, nombre_blancas, nombre_negras, resultado, ritmo):
        blancas = self.buscar(nombre_blancas)
        negras = self.buscar(nombre_negras)
        if blancas is negras:
            raise ValueError("Un jugador no puede jugar contra sí mismo")

        partida = Partida(blancas, negras, resultado, ritmo)
        puntos_b, puntos_n = partida.puntos()

        blancas.registrar_resultado(puntos_b)
        negras.registrar_resultado(puntos_n)
        blancas.actualizar_elo(puntos_b, ritmo.k)
        negras.actualizar_elo(puntos_n, ritmo.k)

        self.partidas.append(partida)
        blancas.historial.append(partida)
        negras.historial.append(partida)

    def ranking(self):
        return sorted(self.jugadores.values(), key=lambda j: j.elo, reverse=True)

    def mostrar_ranking(self):
        print("\nRANKING")
        for pos, jugador in enumerate(self.ranking(), start=1):
            print(f"{pos}. {jugador.resumen()}")

    def mostrar_historial(self, nombre):
        jugador = self.buscar(nombre)
        print(f"\nHistorial de {nombre}")
        for partida in jugador.historial:
            print(f"  {partida.describir_para(jugador)}")