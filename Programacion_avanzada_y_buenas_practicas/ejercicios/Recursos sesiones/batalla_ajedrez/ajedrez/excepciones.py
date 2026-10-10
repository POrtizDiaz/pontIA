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


class PartidaInvalida(ErrorAjedrez):
    """Resultado desconocido o un jugador jugando contra sí mismo."""
    
class TorneoInvalido(ErrorAjedrez):
    """Lanzada cuando la configuración de un torneo es inválida.""" 
