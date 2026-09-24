# Ejercicio 3: Proteger el estado y hablar con el exterior

En la reflexión final del ejercicio 1 vimos que nada impedía hacer
`plataforma.jugadores["Magnus"].elo = 9999`, y dijimos que "lo veríamos más adelante".
Ha llegado el momento. En este bloque vas a:

- proteger el ELO con **`@property`** (un concepto nuevo, no está en los vídeos);
- sustituir los `print` y los `ValueError` genéricos por **excepciones propias**;
- añadir **constructores alternativos** con `@classmethod` para cargar y guardar la
  plataforma en JSON.

> **Requisitos previos:** haber terminado el ejercicio 2. Sigue trabajando en el mismo
> proyecto (si no lo terminaste, copia `soluciones/ejercicio_2/` y continúa desde ahí).
> Al acabar, `uv run ruff check .` y `uv run ruff format --check .` deben seguir limpios.

---

## Parte 1: `@property`, el ELO es de solo lectura

Un decorador `@property` convierte un método en un **atributo calculado**: se lee como
atributo (`jugador.elo`, sin paréntesis) pero por dentro ejecuta código. Si no defines un
*setter*, el atributo es de **solo lectura**.

```python
class Termometro:
    def __init__(self, celsius):
        self._celsius = celsius        # el dato real, con guion bajo

    @property
    def celsius(self):                 # se lee como t.celsius
        return self._celsius

    @property
    def fahrenheit(self):              # calculado al vuelo, no se almacena
        return self._celsius * 9 / 5 + 32


t = Termometro(20)
print(t.celsius, t.fahrenheit)         # 20 68.0
t.celsius = 30                         # AttributeError: property 'celsius' ... has no setter
```

Aplícalo a `Jugador`:

1. Renombra el atributo `elo` a `_elo` (el guion bajo es la convención de Python para
   "esto es interno, no lo toques desde fuera") y expón una propiedad `elo` de **solo
   lectura**. El único sitio donde `_elo` cambia es `actualizar_elo`.
2. Convierte `partidas_jugadas()` y `porcentaje_victorias()` en propiedades: son datos
   derivados, no acciones. Actualiza `__str__`, que los usaba con paréntesis.

Comprueba:

```python
>>> from ajedrez.jugador import Jugador
>>> j = Jugador("Magnus", "NOR")
>>> j.elo
1200
>>> j.elo = 9999
Traceback (most recent call last):
  ...
AttributeError: property 'elo' of 'Jugador' object has no setter
>>> j.actualizar_elo(1, 20); j.elo
1220
```

---

## Parte 2: Excepciones propias

Ahora mismo la plataforma mezcla dos maneras de avisar de un error: `registrar` hace un
`print` y sigue, y el resto lanza `ValueError` (¡igual que lanzaría `int("hola")`!). Quien
usa la plataforma no puede distinguir *nuestros* errores de los demás.

La solución tiene tres pasos: **definir** nuestras propias excepciones, **lanzarlas**
(`raise`) en los sitios donde hoy hay un `print` o un `ValueError`, y **capturarlas**
(`try/except`) en `main.py`.

### Paso 1: definir las excepciones

Una excepción propia no es más que una clase que hereda de `Exception` (o de otra
excepción). Crea el fichero `ajedrez/excepciones.py` con una **clase base** y tres
**clases hijas**:

```python
class ErrorAjedrez(Exception):
    """Base de todas las excepciones de la plataforma."""


class JugadorNoRegistrado(ErrorAjedrez):
    def __init__(self, nombre):
        super().__init__(f"El jugador {nombre} no está registrado")
        self.nombre = nombre


class JugadorDuplicado(ErrorAjedrez):
    # TODO: igual que JugadorNoRegistrado, con el mensaje "El jugador X ya existe"
    ...


class PartidaInvalida(ErrorAjedrez):
    """Resultado desconocido o un jugador jugando contra sí mismo."""
```

`PartidaInvalida` no necesita `__init__` propio: recibe el mensaje ya hecho, como
cualquier excepción normal (`raise PartidaInvalida("Resultado inválido: 2-0")`).

Si quieres pruébalas antes de seguir, en `uv run python`:

```python
>>> from ajedrez.excepciones import ErrorAjedrez, JugadorNoRegistrado
>>> e = JugadorNoRegistrado("Bobby")
>>> print(e)
El jugador Bobby no está registrado
>>> e.nombre
'Bobby'
>>> isinstance(e, ErrorAjedrez)
True
```

### Paso 2: lanzarlas donde hoy hay un `print` o un `ValueError`

Hay exactamente tres sitios que cambiar. En cada uno, importa la excepción que toque
(`from ajedrez.excepciones import ...`) al principio del fichero.

**a) `Plataforma.__getitem__`** (fichero `plataforma.py`): sustituye el `KeyError` por
`JugadorNoRegistrado`.

**b) `Plataforma.registrar`** (fichero `plataforma.py`): sustituye el `print` + `return`
por `raise`. A partir de ahora registrar un duplicado no es un aviso, es un error.

**c) `Partida.__init__`** (fichero `partida.py`): sustituye el `ValueError` del resultado
por `PartidaInvalida` y añade ahí la comprobación de que blancas y negras no sean el
mismo jugador. Esa comprobación está hoy en `Plataforma.jugar`: bórrala de allí. La
idea es que una partida inválida no pueda ni siquiera construirse.

### Paso 3: capturarlas en `main.py`

Hasta ahora, un error paraba el programa entero. Ahora `main.py` va a intentar cada
operación y, si falla por un motivo nuestro, avisar y seguir con la siguiente:


- `except ErrorAjedrez` captura cualquiera de las tres hijas, porque todas heredan de
  ella. No hace falta un `except` por cada tipo.
- `type(e).__name__` es el nombre de la clase concreta (`JugadorDuplicado`), y `{e}` el
  mensaje que construimos en el Paso 1.

Escribe en `main.py` una secuencia de operaciones que incluya, a propósito: un registro
duplicado, una partida contra un jugador inexistente (`"Bobby"`), una de un jugador contra
sí mismo y un resultado `"2-0"`. Cada una debe imprimir su línea de "Operación rechazada"
y el programa debe llegar al final y mostrar el ranking. Si repetir el `try/except` cuatro
veces te parece pesado, mete las operaciones en una lista y recórrela con un solo bucle.

---

## Parte 3: Constructores alternativos y JSON

La plataforma necesita **persistir**: guardar los jugadores al cerrar y cargarlos al
arrancar. El formato será JSON:

Crea la carpeta `datos/` dentro del proyecto y, en ella, el fichero `jugadores.json` con
este contenido exacto (seis jugadores: los cuatro de siempre más Alireza y Anish):

```json
{
  "jugadores": [
    {"nombre": "Magnus", "pais": "NOR", "elo": 2830, "victorias": 40, "derrotas": 5, "tablas": 25},
    {"nombre": "Hikaru", "pais": "USA", "elo": 2790, "victorias": 35, "derrotas": 10, "tablas": 20},
    {"nombre": "Ding", "pais": "CHN", "elo": 2760, "victorias": 28, "derrotas": 12, "tablas": 30},
    {"nombre": "Judit", "pais": "HUN", "elo": 2735, "victorias": 30, "derrotas": 15, "tablas": 15},
    {"nombre": "Alireza", "pais": "FRA", "elo": 2750, "victorias": 33, "derrotas": 14, "tablas": 18},
    {"nombre": "Anish", "pais": "NED", "elo": 2745, "victorias": 20, "derrotas": 8, "tablas": 42}
  ]
}
```

Cada entrada tiene las mismas claves que los atributos de `Jugador`, y el ELO ya no es el
inicial: son jugadores con historia.

1. En `Jugador`, añade el constructor alternativo **`desde_dict(cls, datos)`** con
   `@classmethod`, y su inverso `a_dict()`. El `__init__` sigue recibiendo solo
   `nombre` y `pais`; es `desde_dict` quien rellena el resto (incluido `_elo`).

2. En `Plataforma` añade dos métodos (necesitarás `import json` al principio de
   `plataforma.py`):

   - **`desde_json(cls, ruta)`**, un `@classmethod`, igual que `desde_dict`. Pasos:
     1. Abre el fichero con `with open(ruta, encoding="utf-8") as f:` y léelo con
        `datos = json.load(f)`. `datos` es un diccionario con una única clave,
        `"jugadores"`, cuyo valor es la lista de diccionarios del fichero.
     2. Crea una plataforma vacía: `plataforma = cls()`.
     3. Recorre `datos["jugadores"]`; por cada diccionario crea el jugador con
        `Jugador.desde_dict(...)` y guárdalo en `plataforma.jugadores[jugador.nombre]`.
        (No uses `registrar`: ese método crea jugadores nuevos con ELO 1200.)
     4. Devuelve la plataforma.
   - **`guardar_json(self, ruta)`**, un método normal. Construye un diccionario con la
     misma forma que el fichero de entrada,
     `{"jugadores": [jugador.a_dict() for jugador in self]}` (recuerda que iterar la
     plataforma recorre sus jugadores), y escríbelo con
     `json.dump(datos, f, indent=2, ensure_ascii=False)` dentro de un
     `with open(ruta, "w", encoding="utf-8") as f:`.

3. Reescribe `main()` en `main.py` con este flujo. Ya no se registra a nadie a mano: los
   jugadores vienen del fichero.

   1. Carga la plataforma con `Plataforma.desde_json("datos/jugadores.json")` e imprime
      `Cargados 6 jugadores desde datos/jugadores.json` (usa `len(plataforma)`).
   2. Demuestra la Parte 1: obtén a Magnus con `plataforma["Magnus"]`, intenta
      `magnus.elo = 9999` dentro de un `try/except AttributeError` e imprime
      `No se puede asignar el ELO: <mensaje>`.
   3. Ejecuta estas ocho operaciones, en este orden, cada una protegida con el
      `try/except ErrorAjedrez` de la Parte 2. Cuatro son válidas y cambian el ELO; las
      otras cuatro deben ser rechazadas:

      | # | Operación | ¿Qué pasa? |
      |---|---|---|
      | 1 | `registrar("Magnus", "NOR")` | rechazada: `JugadorDuplicado` |
      | 2 | `jugar("Magnus", "Hikaru", "1-0", BLITZ)` | válida: Magnus +20, Hikaru −20 |
      | 3 | `jugar("Ding", "Judit", "1/2-1/2", CLASICA)` | válida: tablas, el ELO no cambia |
      | 4 | `jugar("Alireza", "Bobby", "1-0", BULLET)` | rechazada: `JugadorNoRegistrado` |
      | 5 | `jugar("Anish", "Anish", "1-0", BLITZ)` | rechazada: `PartidaInvalida` |
      | 6 | `jugar("Hikaru", "Ding", "2-0", BULLET)` | rechazada: `PartidaInvalida` |
      | 7 | `jugar("Judit", "Alireza", "0-1", CLASICA)` | válida: Alireza +40, Judit −40 |
      | 8 | `jugar("Anish", "Magnus", "1/2-1/2", BULLET)` | válida: tablas |

      La forma más limpia es una lista de tuplas y un único bucle:

      ```python
      operaciones = [
          ("registrar", "Magnus", "NOR"),
          ("jugar", "Magnus", "Hikaru", "1-0", BLITZ),
          ...
      ]
      for operacion, *argumentos in operaciones:
          try:
              if operacion == "registrar":
                  plataforma.registrar(*argumentos)
              else:
                  plataforma.jugar(*argumentos)
          except ErrorAjedrez as e:
              print(f"Operación rechazada ({type(e).__name__}): {e}")
      ```

      (`*argumentos` en el `for` recoge el resto de la tupla en una lista; `*argumentos`
      en la llamada la vuelve a desempaquetar como parámetros.)

   4. Muestra el ranking (`mostrar_ranking`) y el historial de Magnus (`mostrar_historial`).
   5. Guarda el estado con `plataforma.guardar_json("datos/jugadores_actualizado.json")` e
      imprime `Guardado en datos/jugadores_actualizado.json`.

Salida esperada:

```
Cargados 6 jugadores desde datos/jugadores.json
No se puede asignar el ELO: property 'elo' of 'Jugador' object has no setter
Operación rechazada (JugadorDuplicado): El jugador Magnus ya existe
Operación rechazada (JugadorNoRegistrado): El jugador Bobby no está registrado
Operación rechazada (PartidaInvalida): Anish no puede jugar contra sí mismo
Operación rechazada (PartidaInvalida): Resultado inválido: 2-0

RANKING
1. Magnus   (NOR)  ELO 2850  | 41V 5D 26T | 57% victorias
2. Alireza  (FRA)  ELO 2790  | 34V 14D 18T | 52% victorias
3. Hikaru   (USA)  ELO 2770  | 35V 11D 20T | 53% victorias
4. Ding     (CHN)  ELO 2760  | 28V 12D 31T | 39% victorias
5. Anish    (NED)  ELO 2745  | 20V 8D 43T | 28% victorias
6. Judit    (HUN)  ELO 2695  | 30V 16D 16T | 48% victorias

Historial de Magnus
  vs Hikaru   con blancas  1-0      [blitz, 5 min]
  vs Anish    con negras   1/2-1/2  [bullet, 1 min]

Guardado en datos/jugadores_actualizado.json
```

Para terminar, abre `datos/jugadores_actualizado.json` y compáralo con `jugadores.json`:
Magnus, Hikaru, Alireza y Judit han cambiado de ELO y de estadísticas; Ding y Anish solo
han sumado unas tablas. Ese fichero es el que cargaríamos la próxima vez que arranque la
plataforma.
