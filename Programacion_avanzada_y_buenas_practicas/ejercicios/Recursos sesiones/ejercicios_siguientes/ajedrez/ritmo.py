from dataclasses import dataclass


@dataclass(frozen=True)
class Ritmo:
    """Ritmo de juego: cuánto tiempo hay por jugador y cuánto ELO está en juego."""

    nombre: str
    k: int
    tiempo: str

    def describir(self):
        return f"{self.nombre}, {self.tiempo}"


BULLET = Ritmo("bullet", 10, "1 min")
BLITZ = Ritmo("blitz", 20, "5 min")
CLASICA = Ritmo("clasica", 40, "90 min")
RAPID = Ritmo("rapid", 30, "15 min")