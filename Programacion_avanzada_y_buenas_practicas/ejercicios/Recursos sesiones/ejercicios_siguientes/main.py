from ajedrez.plataforma import Plataforma
from ajedrez.ritmo import BLITZ, BULLET, CLASICA


def main():
    plataforma = Plataforma()
    plataforma.registrar("Magnus", "NOR")
    plataforma.registrar("Hikaru", "USA")
    plataforma.registrar("Ding", "CHN")
    plataforma.registrar("Judit", "HUN")
    plataforma.registrar("Magnus", "NOR")  # duplicado

    plataforma.jugar("Magnus", "Hikaru", "1-0", BLITZ)
    plataforma.jugar("Ding", "Judit", "1/2-1/2", CLASICA)
    plataforma.jugar("Hikaru", "Ding", "1-0", BULLET)
    plataforma.jugar("Judit", "Magnus", "0-1", CLASICA)
    plataforma.jugar("Hikaru", "Judit", "0-1", BLITZ)
    plataforma.jugar("Magnus", "Ding", "1/2-1/2", BULLET)

    plataforma.mostrar_ranking()
    plataforma.mostrar_historial("Magnus")
    plataforma.mostrar_historial("Judit")

    print(f"\nTotal de partidas en la plataforma: {len(plataforma.partidas)}")

    # Lo nuevo del data model, en acciÃ³n
    print(f"Jugadores registrados: {len(plataforma)}")
    print(f"Mejor jugador: {max(plataforma).nombre}")
    print(f"repr: {plataforma['Magnus']!r}")


if __name__ == "__main__":
    main()