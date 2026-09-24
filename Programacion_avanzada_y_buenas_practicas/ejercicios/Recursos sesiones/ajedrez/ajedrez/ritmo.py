class Ritmo:
    def __init__(self, nombre, k, tiempo):
        self.nombre = nombre
        self.k = k
        self.tiempo = tiempo

    def describir(self):
        return f"{self.nombre}, {self.tiempo}"


BULLET = Ritmo("bullet", 10, "1 min")
BLITZ = Ritmo("blitz", 20, "5 min")
CLASICA = Ritmo("clasica", 40, "90 min")
RAPID = Ritmo("rapid", 30, "15 min")