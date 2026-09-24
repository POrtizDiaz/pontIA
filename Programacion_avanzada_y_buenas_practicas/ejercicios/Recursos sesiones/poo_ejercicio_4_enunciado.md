# Ejercicio 4: Torneos para todos los gustos

La plataforma quiere organizar **torneos**. Hay de varios tipos: una **liga** (todos
contra todos) y una **eliminatoria** (parejas a partidas únicas). Y seguro que mañana
aparece otro (suizo, por equipos...). En este bloque vas a aplicar lo visto en los vídeos
de herencia, clases abstractas y polimorfismo para que añadir un tipo de torneo nuevo
sea escribir **una clase pequeña** y nada más: sin tocar `Plataforma`, sin `if/elif`.

> **Requisitos previos:** haber terminado el ejercicio 3 (o partir de
> `soluciones/ejercicio_3/`). Ruff limpio al acabar.

---

## Parte 1: La clase abstracta `Torneo`

Todos los torneos comparten casi todo: tienen un nombre, se juegan en una plataforma con
un ritmo, tienen participantes, se juegan y tienen un campeón. **Lo único que cambia es
cómo se emparejan los participantes.** Eso es exactamente lo que modela una clase
abstracta: el esqueleto común se escribe una vez, y el hueco variable se deja como
`@abstractmethod` para que lo rellene cada subclase.

Crea `ajedrez/torneo.py` con:

```python
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
```

Fíjate en que un torneo **tiene** una plataforma (composición): las partidas se juegan
con `self.plataforma.jugar(...)`, que ya valida, actualiza ELO e historiales. `Torneo` no
repite nada de eso.

Comprueba que **no** se puede instanciar:

```python
>>> Torneo("Imposible", plataforma, RAPID, ["Magnus", "Hikaru"])
TypeError: Can't instantiate abstract class Torneo without an implementation for abstract method 'emparejamientos'
```

**❓ Pregunta 1.** Alguien propone `class Torneo(Plataforma)` "para que el torneo tenga
acceso directo a los jugadores y a `jugar()`". ¿Por qué es mala idea? Piensa en la
pregunta del vídeo 12: ¿un torneo **es** una plataforma o **tiene** una plataforma?
¿Qué pasaría con `len(torneo)` o con `torneo.registrar(...)`?

---

## Parte 2: Las subclases

Ahora toca rellenar el hueco que dejó la clase abstracta. En esta parte tienes que
crear dos clases nuevas, `Liga` y `Eliminatoria`, las dos heredando de `Torneo`. Cada una solo tiene que implementar el método `emparejamientos()` que `Torneo` dejó abstracto.

Recuerda el contrato: `emparejamientos()` devuelve una lista de tuplas de nombres
`(nombre_blancas, nombre_negras)`, y `Torneo.jugar` la recorre buscando cada pareja como
clave en el diccionario `resultados`.

### Clase 1: `Liga(Torneo)`, todos contra todos

Crea la clase `Liga`, que hereda de `Torneo`. En una liga, cada pareja de
participantes juega una vez. Con `["Magnus", "Hikaru", "Ding", "Judit"]`
salen seis partidas:

```python
[("Magnus", "Hikaru"), ("Magnus", "Ding"), ("Magnus", "Judit"),
 ("Hikaru", "Ding"), ("Hikaru", "Judit"), ("Ding", "Judit")]
```

Eso es exactamente lo que devuelve `itertools.combinations(self.participantes, 2)` (todas
las combinaciones de dos elementos, sin repetir y sin importar el orden).


### Clase 2: `Eliminatoria(Torneo)`, una ronda a partido único

Crea la clase `Eliminatoria`, que también hereda de `Torneo`. Los participantes se
emparejan en el orden en que vienen en la lista: el 1º contra el
2º, el 3º contra el 4º, y así sucesivamente. Con `["Alireza", "Anish", "Hikaru", "Judit"]`
solo hay dos partidas: `[("Alireza", "Anish"), ("Hikaru", "Judit")]`.

Esta clase tiene dos partes:

1. El método `emparejamientos()`. `self.participantes[::2]` son los elementos en posiciones
   pares (1º, 3º, ...) y `self.participantes[1::2]` los de posiciones impares (2º, 4º, ...).

2. Un `__init__` propio con una validación. Con un número impar de participantes alguien se
   quedaría sin rival, así que una eliminatoria con 3 jugadores no debe poder crearse.
   Para eso `Eliminatoria` sobreescribe `__init__`

   - La primera línea debe ser `super().__init__(...)` con los mismos cuatro
     argumentos. Es lo que ejecuta el `__init__` de `Torneo` y crea `self.nombre`,
     `self.plataforma`, `self.ritmo`, `self.participantes` y `self.partidas`. Si te la
     saltas, la línea siguiente falla con `AttributeError: 'Eliminatoria' object has no
     attribute 'participantes'`: sobreescribir `__init__` no ejecuta el del padre
     automáticamente, hay que pedirlo.
   - Después, la comprobación. El mensaje de la excepción debe ser
     `"Una eliminatoria necesita un número par de participantes (hay 3)"`.

   `TorneoInvalido` no existe todavía: crea también esa clase en
   `ajedrez/excepciones.py`, heredando de `ErrorAjedrez`, igual que `PartidaInvalida`
   (basta la clase con su docstring; recibe el mensaje ya hecho). Impórtala en `torneo.py`.

Comprueba:

```python
>>> ko = Eliminatoria("KO Blitz", plataforma, BLITZ, ["Alireza", "Anish", "Hikaru", "Judit"])
>>> ko.emparejamientos()
[('Alireza', 'Anish'), ('Hikaru', 'Judit')]
>>> Eliminatoria("Impar", plataforma, BLITZ, ["Magnus", "Hikaru", "Ding"])
Traceback (most recent call last):
  ...
ajedrez.excepciones.TorneoInvalido: Una eliminatoria necesita un número par de participantes (hay 3)
```

En resumen, al acabar esta parte habrás creado **tres clases nuevas**: `Liga` y
`Eliminatoria` en `torneo.py` (ambas hijas de `Torneo`) y `TorneoInvalido` en
`excepciones.py` (hija de `ErrorAjedrez`). Fíjate en lo poco que has escrito: dos
subclases de menos de diez líneas y ya tienes dos tipos de torneo completos, con
clasificación y campeón incluidos.

**❓ Pregunta 2.** Escribe una subclase `Suizo(Torneo)` **sin** `emparejamientos()` e intenta
instanciarla. ¿Qué ocurre?

---

## Parte 3: Polimorfismo

Ya tienes dos tipos de torneo. Ahora la plataforma tiene que poder **celebrar cualquiera
de ellos con el mismo código**, sin preguntar de qué tipo es. Eso es el polimorfismo del
vídeo 13, y en esta parte vas a hacer dos cosas: **añadir un método a `Plataforma`** y
**reescribir `main.py`** para usarlo.

### Paso 1: añade el método `organizar` a la clase `Plataforma`

Abre `ajedrez/plataforma.py` y **añade a la clase `Plataforma` un método nuevo,
`organizar(self, torneo, resultados)`**. Recibe un objeto torneo (una `Liga`, una
`Eliminatoria`... cualquier hijo de `Torneo`) y el diccionario de resultados, y hace
cuatro cosas en orden:

1. Imprime la cabecera `TORNEO: <torneo>` (con `print(f"\nTORNEO: {torneo}")`; el
   `{torneo}` usa el `__str__` de la Parte 1).
2. Juega el torneo: `torneo.jugar(resultados)`.
3. Imprime la clasificación numerada, igual que hace `mostrar_ranking` pero recorriendo
   `torneo.clasificacion()`.
4. Imprime `Campeón: <nombre>` usando `torneo.campeon().nombre`.

### Paso 2: reescribe `main.py`

Sustituye el contenido de `main()` por este flujo:

1. Carga la plataforma con `Plataforma.desde_json("datos/jugadores.json")` e imprime
   `Cargados 6 jugadores`.

2. Crea los dos torneos y sus resultados. Las claves del diccionario son las parejas
   exactamente como las devuelve `emparejamientos()` (blancas primero):

   ```python
   liga = Liga("Liga Rapid", plataforma, RAPID, ["Magnus", "Hikaru", "Ding", "Judit"])
   resultados_liga = {
       ("Magnus", "Hikaru"): "1/2-1/2",
       ("Magnus", "Ding"): "1-0",
       ("Magnus", "Judit"): "1-0",
       ("Hikaru", "Ding"): "1-0",
       ("Hikaru", "Judit"): "1/2-1/2",
       ("Ding", "Judit"): "0-1",
   }

   eliminatoria = Eliminatoria("KO Blitz", plataforma, BLITZ, ["Alireza", "Anish", "Hikaru", "Judit"])
   resultados_eliminatoria = {
       ("Alireza", "Anish"): "0-1",
       ("Hikaru", "Judit"): "1-0",
   }
   ```

3. Celebra los dos torneos con un único bucle. Aquí está el polimorfismo en acción:
   la lista mezcla una `Liga` y una `Eliminatoria`, y el cuerpo del bucle es el mismo para
   ambas.

4. Termina con `plataforma.mostrar_ranking()` y el total de partidas,
   `len(plataforma.partidas)` (deben ser 8: 6 de la liga + 2 de la eliminatoria).

Salida esperada:

```
Cargados 6 jugadores

TORNEO: Liga Rapid (rapid, 15 min)
1. Magnus   (NOR)  ELO 2890  | 42V 5D 26T | 58% victorias
2. Hikaru   (USA)  ELO 2820  | 36V 10D 22T | 53% victorias
3. Judit    (HUN)  ELO 2735  | 31V 16D 16T | 49% victorias
4. Ding     (CHN)  ELO 2670  | 28V 15D 30T | 38% victorias
Campeón: Magnus

TORNEO: KO Blitz (blitz, 5 min)
1. Hikaru   (USA)  ELO 2840  | 37V 10D 22T | 54% victorias
2. Anish    (NED)  ELO 2765  | 21V 8D 42T | 30% victorias
3. Alireza  (FRA)  ELO 2730  | 33V 15D 18T | 50% victorias
4. Judit    (HUN)  ELO 2715  | 31V 17D 16T | 48% victorias
Campeón: Hikaru

RANKING
1. Magnus   (NOR)  ELO 2890  | 42V 5D 26T | 58% victorias
2. Hikaru   (USA)  ELO 2840  | 37V 10D 22T | 54% victorias
3. Anish    (NED)  ELO 2765  | 21V 8D 42T | 30% victorias
4. Alireza  (FRA)  ELO 2730  | 33V 15D 18T | 50% victorias
5. Judit    (HUN)  ELO 2715  | 31V 17D 16T | 48% victorias
6. Ding     (CHN)  ELO 2670  | 28V 15D 30T | 38% victorias

Total de partidas en la plataforma: 8
```