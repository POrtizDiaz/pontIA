from ajedrez.jugador import Jugador
from ajedrez.partida import Partida
from ajedrez.excepciones import JugadorNoRegistrado, JugadorDuplicado


class Plataforma:
    def __init__(self):
        self.jugadores = {}  # nombre -> Jugador
        self.partidas = []  # lista de Partida

    # --- Data model: la plataforma se comporta como una colección ----
    def __len__(self):
        return len(self.jugadores)

    def __iter__(self):
        # Recorrer la plataforma = recorrer sus jugadores de mayor a menor ELO
        return iter(sorted(self.jugadores.values(), reverse=True))

    def __getitem__(self, nombre):
        if nombre not in self.jugadores:
            raise JugadorNoRegistrado(nombre)
        return self.jugadores[nombre]

    # --- Operaciones -------------------------------------------------
    def registrar(self, nombre, pais):
        if nombre in self.jugadores:
            raise JugadorDuplicado(nombre)
            return
        self.jugadores[nombre] = Jugador(nombre, pais)

    def jugar(self, nombre_blancas, nombre_negras, resultado, ritmo):
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