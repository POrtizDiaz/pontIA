import json

from ajedrez.excepciones import JugadorDuplicado, JugadorNoRegistrado
from ajedrez.jugador import Jugador
from ajedrez.partida import Partida
from ajedrez.ritmo import Ritmo


class Plataforma:
    def __init__(self):
        self.jugadores = {}  # nombre -> Jugador
        self.partidas = []  # lista de Partida

    @classmethod
    def desde_json(cls, ruta: str):
        with open(ruta, encoding="utf-8") as f:
            datos = json.load(f)

        plataforma = cls()
        for d in datos["jugadores"]:
            jugador = Jugador.desde_dict(d)
            plataforma.jugadores[jugador.nombre] = jugador
        return plataforma

    def guardar_json(self, ruta: str):
        datos = {"jugadores": [jugador.a_dict() for jugador in self]}
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

    def __len__(self):
        return len(self.jugadores)

    def __iter__(self):
        return iter(sorted(self.jugadores.values(), reverse=True))

    def __getitem__(self, nombre):
        if nombre not in self.jugadores:
            raise JugadorNoRegistrado(nombre)
        jugador = self.jugadores[nombre]
        return jugador

    def registrar(self, nombre, pais):
        if nombre in self.jugadores:
            raise JugadorDuplicado(nombre)
        self.jugadores[nombre] = Jugador(nombre, pais)

    def jugar(self, nombre_blancas, nombre_negras, resultado, ritmo: Ritmo):
        blancas = self[nombre_blancas]
        negras = self[nombre_negras]

        partida = Partida(blancas, negras, resultado, ritmo)
        puntos_b, puntos_n = partida.puntos()

        blancas.registrar_resultado(puntos_b)
        negras.registrar_resultado(puntos_n)
        blancas.actualizar_elo(puntos_b, ritmo.k)
        negras.actualizar_elo(puntos_n, ritmo.k)

        self.partidas.append(partida)
        blancas.historial.append(partida)
        negras.historial.append(partida)

    def mostrar_ranking(self):
        print("\nRANKING")
        for pos, jugador in enumerate(self, start=1):
            print(f"{pos}. {jugador}")

    def mostrar_historial(self, nombre):
        jugador = self[nombre]
        print(f"\nHistorial de {nombre}")
        for partida in jugador.historial:
            print(f"  {partida.describir_para(jugador)}")
