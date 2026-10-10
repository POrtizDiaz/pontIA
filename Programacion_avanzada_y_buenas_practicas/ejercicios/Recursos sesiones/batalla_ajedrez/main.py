from ajedrez.excepciones import ErrorAjedrez
from ajedrez.plataforma import Plataforma
from ajedrez.ritmo import BLITZ, BULLET, CLASICA


def main():
    # 1. Cargar desde JSON
    plataforma = Plataforma.desde_json("datos/jugadores.json")
    print(f"Cargados {len(plataforma)} jugadores desde datos/jugadores.json")

    # 2. Probar propiedad de solo lectura
    magnus = plataforma["Magnus"]
    try:
        magnus.elo = 9999
    except AttributeError as e:
        print(f"No se puede asignar el ELO: {e}")

    # 3. Lista de operaciones (4 válidas y 4 que deben ser rechazadas)
    operaciones = [
        ("registrar", "Magnus", "NOR"),
        ("jugar", "Magnus", "Hikaru", "1-0", BLITZ),
        ("jugar", "Ding", "Judit", "1/2-1/2", CLASICA),
        ("jugar", "Alireza", "Bobby", "1-0", BULLET),
        ("jugar", "Anish", "Anish", "1-0", BLITZ),
        ("jugar", "Hikaru", "Ding", "2-0", BULLET),
        ("jugar", "Judit", "Alireza", "0-1", CLASICA),
        ("jugar", "Anish", "Magnus", "1/2-1/2", BULLET),
    ]

    for operacion, *argumentos in operaciones:
        try:
            if operacion == "registrar":
                plataforma.registrar(*argumentos)
            else:
                plataforma.jugar(*argumentos)
        except ErrorAjedrez as e:
            print(f"Operación rechazada ({type(e).__name__}): {e}")

    # 4. Mostrar resultados
    plataforma.mostrar_ranking()
    plataforma.mostrar_historial("Magnus")

    # 5. Guardar estado actualizado
    plataforma.guardar_json("datos/jugadores_actualizado.json")
    print("\nGuardado en datos/jugadores_actualizado.json")


if __name__ == "__main__":
    main()
