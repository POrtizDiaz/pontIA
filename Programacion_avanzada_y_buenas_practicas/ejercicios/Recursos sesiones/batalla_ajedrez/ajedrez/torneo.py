from abc import ABC, abstractmethod
import itertools
from plataforma import Plataforma
from excepciones import TorneoInvalido

class Torneo (ABC):
    def __init__(self, nombre, plataforma, ritmo, participantes):
        self.nombre = nombre
        self.plataforma = plataforma
        self.ritmo = ritmo
        self.participantes = participantes
        self.partidas = []
        
    @abstractmethod
    def emparejamientos(self):
        pass
    
    def jugar(self, resultados):
        for jugador_b, jugador_n in self.emparejamientos():
            resultado = resultados[(jugador_b, jugador_n)]
            p = self.plataforma.jugar(jugador_b, jugador_n, resultado, self.ritmo)
            self.partidas.append(p)
        
    def jugadores(self):
        lista_jugadores = []
        for nombre_jugadores in self.participantes:
            lista_jugadores.append(self.plataforma[nombre_jugadores])
        return lista_jugadores
    
    def clasificacion(self):
        return sorted(self.jugadores(), reverse = True)
    
    def campeon(self):
        return self.clasificacion()[0]
    
    def __str__(self):
        return f"{self.nombre} ({self.ritmo})"
    
class Liga(Torneo):
    def emparejamientos(self):
        return list(itertools.combinations(self.participantes, 2))
    
class Eliminatoria(Torneo):
    def __init__(self, nombre, plataforma, ritmo, participantes):
        super().__init__(nombre, plataforma, ritmo, participantes)
        if len(self.participantes) % 2 != 0:
            raise TorneoInvalido (f"Una eliminatoria necesita un número par de participantes (hay {len(self.participantes)})")

    def emparejamientos(self):
        return list(zip(self.participantes[::2], self.participantes[1::2]))       
        
    