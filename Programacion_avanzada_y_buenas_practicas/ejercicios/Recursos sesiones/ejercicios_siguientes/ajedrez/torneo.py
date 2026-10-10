from abc import ABC, abstractmethod


class Torneo(ABC):
    def __init__(self, nombre, plataforma, ritmo, participantes):
        ...  # nombre, plataforma, ritmo, participantes (lista de nombres), partidas = []

    @abstractmethod
    def emparejamientos(self):
        """Devuelve la lista de parejas (nombre_blancas, nombre_negras)."""

    def jugar(self, resultados):
        """resultados es un dict {(blancas, negras): "1-0", ...}.
        Juega cada emparejamiento A TRAVÉS de la plataforma y guarda las partidas."""

    def jugadores(self):
        """Los objetos Jugador de los participantes (pídeselos a la plataforma)."""

    def clasificacion(self):
        """Participantes ordenados de mayor a menor ELO."""

    def campeon(self):
        """El participante con más ELO."""

    def __str__(self):
        """'Liga Rapid (rapid, 15 min)'"""