class ErrorAjedrez(Exception):
    """Base de todas las excepciones de la plataforma."""


class JugadorNoRegistrado(ErrorAjedrez):
    def __init__(self, nombre):
        super().__init__(f"El jugador {nombre} no está registrado")
        self.nombre = nombre


class JugadorDuplicado(ErrorAjedrez):
    def __init__(self, nombre):
            super().__init__(f"El jugador {nombre} ya existe")
            self.nombre = nombre
    ...


class PartidaInvalida(ErrorAjedrez):
    def __init__(self, blancas, negras):
                super().__init__(f"Un jugador no puede jugar contra sí mismo")
                self.blancas = blancas
                self.negras = negras
    
