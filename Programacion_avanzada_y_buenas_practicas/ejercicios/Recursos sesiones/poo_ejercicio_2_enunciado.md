# Ejercicio 2: Del notebook al proyecto

En la Clase 1 convertimos la plataforma de ajedrez en cuatro clases (`Jugador`, `Ritmo`,
`Partida` y `Plataforma`) dentro de un notebook. A partir de ahora vamos a trabajar como
se trabaja en un proyecto real: **un proyecto `uv` con un paquete de Python**, varios
módulos, un `main.py` y Ruff vigilando el estilo.

En este primer bloque montarás el proyecto y, ya con el código en ficheros, aplicarás dos
cosas que has visto en los vídeos: **dataclasses** y el **data model** de Python (los
métodos `__dunder__`) para que tus objetos se comporten como objetos nativos de Python.

> **Requisitos previos:** tener `uv` instalado (`uv --version` debe funcionar) y haber
> terminado el ejercicio 1. El código de partida es la solución del ejercicio 1 en un
> único fichero, y lo tienes justo debajo: **al final de este ejercicio tu programa debe
> imprimir exactamente la misma salida** (más unas líneas nuevas al final).

---

## Código de partida

Este es el programa completo tal y como quedó al terminar el ejercicio 1. Si quieres ver
la salida de referencia por ti mismo, pégalo en un fichero `ajedrez.py` y ejecútalo con
`python ajedrez.py`.

```python
class Jugador:
    ELO_INICIAL = 1200
    total_registrados = 0

    def __init__(self, nombre, pais):
        self.nombre = nombre
        self.pais = pais
        self.elo = Jugador.ELO_INICIAL
        self.victorias = 0
        self.derrotas = 0
        self.tablas = 0
        self.historial = []
        Jugador.total_registrados += 1

    @staticmethod
    def variacion_elo(puntos, k):
        if puntos == 1:
            return k
        elif puntos == 0:
            return -k
        else:
            return 0

    def actualizar_elo(self, puntos, k):
        self.elo += self.variacion_elo(puntos, k)

    def partidas_jugadas(self):
        return self.victorias + self.derrotas + self.tablas

    def porcentaje_victorias(self):
        total = self.partidas_jugadas()
        return 100 * self.victorias / total if total else 0.0

    def registrar_resultado(self, puntos):
        if puntos == 1:
            self.victorias += 1
        elif puntos == 0:
            self.derrotas += 1
        else:
            self.tablas += 1

    def resumen(self):
        return (
            f"{self.nombre:<8} ({self.pais})  ELO {self.elo}  "
            f"| {self.victorias}V {self.derrotas}D {self.tablas}T "
            f"| {self.porcentaje_victorias():.0f}% victorias"
        )


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


class Partida:
    RESULTADOS = {"1-0": (1, 0), "0-1": (0, 1), "1/2-1/2": (0.5, 0.5)}

    def __init__(self, blancas, negras, resultado, ritmo):
        if resultado not in Partida.RESULTADOS:
            raise ValueError(f"Resultado inválido: {resultado}")
        self.blancas = blancas
        self.negras = negras
        self.resultado = resultado
        self.ritmo = ritmo

    def puntos(self):
        return Partida.RESULTADOS[self.resultado]

    def rival_de(self, jugador):
        return self.negras if jugador is self.blancas else self.blancas

    def color_de(self, jugador):
        return "blancas" if jugador is self.blancas else "negras"

    def describir_para(self, jugador):
        rival = self.rival_de(jugador)
        return (
            f"vs {rival.nombre:<8} con {self.color_de(jugador):<8} "
            f"{self.resultado:<8} [{self.ritmo.describir()}]"
        )


class Plataforma:
    def __init__(self):
        self.jugadores = {}  # nombre -> Jugador
        self.partidas = []  # lista de Partida

    def registrar(self, nombre, pais):
        if nombre in self.jugadores:
            print(f"El jugador {nombre} ya existe")
            return
        self.jugadores[nombre] = Jugador(nombre, pais)

    def buscar(self, nombre):
        if nombre not in self.jugadores:
            raise ValueError(f"El jugador {nombre} no está registrado")
        return self.jugadores[nombre]

    def jugar(self, nombre_blancas, nombre_negras, resultado, ritmo):
        blancas = self.buscar(nombre_blancas)
        negras = self.buscar(nombre_negras)
        if blancas is negras:
            raise ValueError("Un jugador no puede jugar contra sí mismo")

        partida = Partida(blancas, negras, resultado, ritmo)
        puntos_b, puntos_n = partida.puntos()

        blancas.registrar_resultado(puntos_b)
        negras.registrar_resultado(puntos_n)
        blancas.actualizar_elo(puntos_b, ritmo.k)
        negras.actualizar_elo(puntos_n, ritmo.k)

        self.partidas.append(partida)
        blancas.historial.append(partida)
        negras.historial.append(partida)

    def ranking(self):
        return sorted(self.jugadores.values(), key=lambda j: j.elo, reverse=True)

    def mostrar_ranking(self):
        print("\nRANKING")
        for pos, jugador in enumerate(self.ranking(), start=1):
            print(f"{pos}. {jugador.resumen()}")

    def mostrar_historial(self, nombre):
        jugador = self.buscar(nombre)
        print(f"\nHistorial de {nombre}")
        for partida in jugador.historial:
            print(f"  {partida.describir_para(jugador)}")


# --- Programa principal ---
if __name__ == "__main__":
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
```

Salida de referencia:

```
El jugador Magnus ya existe

RANKING
1. Magnus   (NOR)  ELO 1260  | 2V 0D 1T | 67% victorias
2. Ding     (CHN)  ELO 1190  | 0V 1D 2T | 0% victorias
3. Judit    (HUN)  ELO 1180  | 1V 1D 1T | 33% victorias
4. Hikaru   (USA)  ELO 1170  | 1V 2D 0T | 33% victorias

Historial de Magnus
  vs Hikaru   con blancas  1-0      [blitz, 5 min]
  vs Judit    con negras   0-1      [clasica, 90 min]
  vs Ding     con blancas  1/2-1/2  [bullet, 1 min]

Historial de Judit
  vs Ding     con negras   1/2-1/2  [clasica, 90 min]
  vs Magnus   con blancas  0-1      [clasica, 90 min]
  vs Hikaru   con negras   0-1      [blitz, 5 min]

Total de partidas en la plataforma: 6
```

---

## Parte 1: Crear el proyecto y trocear el código

1. Crea un proyecto `uv` llamado `ajedrez`, pineado a Python 3.12, y añade **Ruff** como
   dependencia de desarrollo.

2. Dentro del proyecto crea el paquete `ajedrez/` con un módulo por clase y reparte el
   código de partida de arriba:

   ```
   ajedrez/
   ├── pyproject.toml
   ├── main.py                 # solo el programa principal, dentro de una función main()
   └── ajedrez/
       ├── jugador.py
       ├── ritmo.py            # la clase Ritmo y las constantes BULLET, BLITZ, CLASICA, RAPID
       ├── partida.py
       └── plataforma.py
   ```

   Cada módulo importa **solo lo que necesita** (`partida.py` necesita `Jugador` y
   `Ritmo`; `plataforma.py` necesita `Jugador` y `Partida`...). Usa siempre importaciones
   absolutas desde el paquete, también en `main.py`:

   ```python
   from ajedrez.plataforma import Plataforma
   from ajedrez.ritmo import BLITZ, BULLET, CLASICA
   ```

3. Ejecuta y limpia:

   ```bash
   uv run main.py
   uv run ruff check .
   uv run ruff format .
   ```

   La salida debe ser **idéntica** a la de referencia, y Ruff no debe quejarse de nada.
   Te avisará de una cosa: el diccionario `RESULTADOS` de `Partida` es un **atributo de
   clase mutable** (regla `RUF012`, el mismo peligro del vídeo 06). Sácalo fuera de la
   clase como constante del módulo `partida.py` y usa `RESULTADOS[...]` en vez de
   `Partida.RESULTADOS[...]`.

---

## Parte 2: Dataclasses

`Ritmo` es, sobre todo, un contenedor de datos: todo su `__init__` se limita a copiar
parámetros a atributos. Es el caso perfecto para una dataclass.

Reescribe `Ritmo` como una **`@dataclass(frozen=True)`** con los campos `nombre`, `k` y
`tiempo`. Mantén el método `describir()` y las cuatro constantes. `Partida` se queda como
está: su `__init__` valida el resultado, y eso ya no es "solo copiar datos".

Comprueba en una sesión interactiva (`uv run python`) que:

```python
>>> from ajedrez.ritmo import BLITZ, Ritmo
>>> BLITZ
Ritmo(nombre='blitz', k=20, tiempo='5 min')
>>> BLITZ == Ritmo("blitz", 20, "5 min")
True
>>> BLITZ.k = 99
Traceback (most recent call last):
  ...
dataclasses.FrozenInstanceError: cannot assign to field 'k'
```

**❓ Pregunta 1.** El `repr` y la comparación con `==` de arriba funcionan sin que hayas
escrito ni una línea para ello. ¿Qué métodos ha generado `@dataclass` por ti? ¿Por qué
tiene sentido que `Ritmo` sea `frozen`? Piensa en qué representa un ritmo y qué pasaría
si alguien pudiera cambiar `BLITZ.k` a mitad de programa.

---

## Parte 3: El data model

Ahora que las clases están en su sitio, vamos a hacer que se comporten como objetos
nativos de Python.

1. En `Jugador`:
   - `__repr__` → `Jugador('Magnus', 'NOR', elo=1260)` (para depurar).
   - `__str__` → la línea del ranking que hasta ahora devolvía `resumen()`. Elimina
     `resumen()`: a partir de ahora basta con `print(jugador)` o `f"{jugador}"`.
   - `__lt__` → compara por ELO. Con esto `sorted(lista_de_jugadores)` y
     `max(lista_de_jugadores)` funcionan **sin `key=`**.

2. En `Plataforma`:
   - `__len__` → número de jugadores registrados.
   - `__iter__` → recorre los jugadores **de mayor a menor ELO** (usa `sorted` con
     `reverse=True`; ya no necesitas `key=`). Elimina el método `ranking()`.
   - `__getitem__(nombre)` → devuelve el `Jugador` con ese nombre; si no existe lanza
     `KeyError`. Sustituye al método `buscar()`: donde antes ponías `self.buscar(nombre)`
     ahora pones `self[nombre]`.

3. Reescribe `mostrar_ranking` aprovechando lo anterior:

   ```python
   for pos, jugador in enumerate(self, start=1):
       print(f"{pos}. {jugador}")
   ```

4. Añade al final de `main.py` estas líneas y comprueba la salida:

   ```python
   print(f"Jugadores registrados: {len(plataforma)}")
   print(f"Mejor jugador: {max(plataforma).nombre}")
   print(f"repr: {plataforma['Magnus']!r}")
   ```

   ```
   Jugadores registrados: 4
   Mejor jugador: Magnus
   repr: Jugador('Magnus', 'NOR', elo=1260)
   ```

Vuelve a pasar `ruff check` y `ruff format` antes de dar el ejercicio por terminado.

**❓ Pregunta 2.** Has eliminado tres métodos "de la casa" (`resumen`, `ranking`, `buscar`)
y los has sustituido por métodos `__dunder__`. ¿Qué gana alguien que usa tu clase por
primera vez? ¿Y qué pierde? ¿Se te ocurre alguna operación de `Plataforma` que **no**
deberías convertir en un dunder?
