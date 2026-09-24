# Ejercicio 5: Cargar jugadores sin cargarlos todos

Último bloque del proyecto, y el más corto. Vamos a aplicar lo que has visto en el
notebook `generadores.ipynb`: escribir un generador con `yield` y usarlo
desde `main.py`.

La situación es esta. La plataforma organiza un gran evento y recibe un fichero con
todas las inscripciones: cientos, miles o millones de jugadores. Cargar el fichero
entero en memoria para crear todos los objetos `Jugador` de golpe puede ser lento o
directamente imposible. Pero un torneo no necesita a todos: una eliminatoria a partido
único necesita dos jugadores, y una liga pequeña, cuatro. La idea es leer el
fichero **a medida que cada torneo pide jugadores**, y no más.

> **Requisitos previos:** haber terminado el ejercicio 4 (o partir de
> `soluciones/ejercicio_4/`) y haber leído el notebook `generadores.ipynb`,
> sobre todo las secciones 2 (cómo funciona `yield`), 4 (`islice`) y 6 (generadores dentro
> de una clase). Copia `datos/inscripciones.csv` desde `soluciones/ejercicio_5/datos/` a tu
> carpeta `datos/`: son 40 jugadores, uno por fila, con las mismas columnas que el JSON
> del ejercicio 3. Ruff limpio al acabar.

---

## Parte 1: El generador `leer_jugadores`

Crea el fichero `ajedrez/lectura.py` con **una función generadora `leer_jugadores(ruta)`**
que recorra el CSV y entregue **un `Jugador` cada vez que se lo pidan**, sin construir
nunca una lista con todos. Pasos:

1. Abre el fichero con `with open(ruta, encoding="utf-8", newline="") as f:` y recórrelo
   con `csv.DictReader(f)`: cada vuelta del `for` es un diccionario con las columnas de
   esa fila, por ejemplo `{"nombre": "Fabiano", "pais": "GER", "elo": "2474", ...}`.
2. Ojo: el CSV es texto, así que `elo`, `victorias`, `derrotas` y `tablas` llegan como
   **cadenas**. Conviértelos a su tipo de dato correcto.
3. Construye el jugador con el constructor alternativo `Jugador.desde_dict(...)`

Comprueba en `uv run python` que funciona y que es perezoso:

```python
>>> from itertools import islice
>>> from ajedrez.lectura import leer_jugadores
>>> jugadores = leer_jugadores("datos/inscripciones.csv")
>>> jugadores                      # todavía no se ha leído ninguna fila
<generator object leer_jugadores at 0x...>
>>> next(jugadores)                # ahora se lee la primera
Jugador('Fabiano', 'GER', elo=2474)
>>> [j.nombre for j in islice(jugadores, 2)]   # las dos siguientes
['Ian', 'Wesley']
```

---

## Parte 2: Torneos que piden jugadores de dos en dos

Hay un pequeño obstáculo: `Plataforma.registrar(nombre, pais)` crea un jugador nuevo con
ELO 1200, pero los que salen del generador **ya vienen construidos** con su ELO. Añade a
`Plataforma` un método `anadir(self, jugador)` que reciba un `Jugador` ya hecho y lo
guarde en `self.jugadores` (lanzando `JugadorDuplicado` si ya existe, igual que
`registrar`).

Ahora reescribe `main()` en `main.py`. Empieza con una plataforma **vacía** (ya no cargamos
el JSON) y el generador:

```python
plataforma = Plataforma()
jugadores = leer_jugadores("datos/inscripciones.csv")
```

Y celebra los torneos pidiendo al generador **solo los jugadores que hacen falta**:

1. Escribe una función auxiliar `siguiente_grupo(jugadores, plataforma, cuantos)` que pida
   al generador los siguientes `cuantos` jugadores con `list(islice(jugadores, cuantos))`,
   los añada a la plataforma con `anadir` y devuelva la lista de sus **nombres** (que es lo
   que espera `Torneo`).

2. Celebra **tres eliminatorias** seguidas, en un bucle. Cada una pide un grupo de **2**
   jugadores y se organiza con `plataforma.organizar(...)`.

3. Celebra **una liga** con un grupo de **4** jugadores.

4. Para no escribir los resultados a mano, usa esta función (necesita `import random` y
   `random.seed(42)` al principio de `main()` para que la salida sea siempre la misma):

   ```python
   def resultados_al_azar(torneo):
       return {
           pareja: random.choice(["1-0", "0-1", "1/2-1/2"])
           for pareja in torneo.emparejamientos()
       }
   ```

5. Termina imprimiendo cuántos jugadores hay en la plataforma (`len(plataforma)`) y el
   nombre del **siguiente** jugador del generador (`next(jugadores).nombre`).

Salida esperada:

```
Generador creado: <generator object leer_jugadores at 0x7f721b7c9ea0>
Jugadores en la plataforma: 0

TORNEO: KO 1 (blitz, 5 min)
1. Ian      (UZB)  ELO 2748  | 9V 22D 9T | 22% victorias
2. Fabiano  (GER)  ELO 2474  | 25V 9D 18T | 48% victorias
Campeón: Ian

TORNEO: KO 2 (blitz, 5 min)
1. Wesley   (USA)  ELO 2514  | 9V 21D 11T | 22% victorias
2. Levon    (NED)  ELO 2476  | 32V 19D 7T | 55% victorias
Campeón: Wesley

TORNEO: KO 3 (blitz, 5 min)
1. Anish    (ESP)  ELO 2759  | 41V 18D 6T | 63% victorias
2. Alireza  (GER)  ELO 2728  | 12V 13D 25T | 24% victorias
Campeón: Anish

TORNEO: Liga Rapid (rapid, 15 min)
1. Gukesh   (ESP)  ELO 2578  | 21V 6D 23T | 42% victorias
2. Pragg    (CUB)  ELO 2510  | 24V 19D 10T | 45% victorias
3. Nodirbek (IND)  ELO 2475  | 9V 24D 24T | 16% victorias
4. Arjun    (ARM)  ELO 2442  | 24V 24D 27T | 32% victorias
Campeón: Gukesh

Jugadores en la plataforma: 10
El generador se quedó esperando en la fila 11: Vidit
```
