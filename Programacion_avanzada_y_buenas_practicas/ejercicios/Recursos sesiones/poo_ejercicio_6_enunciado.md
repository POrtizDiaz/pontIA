# Ejercicio 6: Una red de seguridad para la plataforma

La plataforma de ajedrez ya tiene bastante lógica: reglas de ELO, validaciones de
partidas, torneos con emparejamientos distintos, lectura de ficheros... Cada vez que
tocamos algo (y en los últimos cuatro ejercicios lo hemos tocado todo) cruzamos los dedos
y ejecutamos `main.py` para ver si "sigue saliendo lo mismo". Eso no escala. En este
ejercicio vamos a escribir **tests unitarios con pytest** que comprueben automáticamente
que cada pieza hace lo que debe, tal y como viste en el vídeo 16.

> **Requisitos previos:** haber terminado el ejercicio 5 (o partir de
> `Clase 2 y 3/soluciones/ejercicio_5/`) y haber visto el vídeo 16 (*Testing con pytest*).
> Instala pytest como dependencia de desarrollo, igual que Ruff:
>
> ```bash
> uv add --dev pytest
> ```
>
> Ruff limpio al acabar (también sobre la carpeta de tests).

---

## ¿Qué se testea y qué no?

Un test unitario comprueba **una pieza pequeña de lógica que hemos escrito nosotros**. No
tiene sentido testear que Python o sus bibliotecas funcionan: eso ya lo garantizan ellos.
Si escribimos `assert [1, 2] + [3] == [1, 2, 3]` no estamos probando nuestro programa,
estamos probando Python.

| Sí se testea (lógica nuestra) | No se testea (lógica de Python o de terceros) |
|---|---|
| Que ganar suma K y perder resta K (`variacion_elo`) | Que `+=` suma |
| Que el ELO no se puede asignar desde fuera (`@property` sin setter) | Que `@property` funciona |
| Que `Partida` rechaza el resultado `"2-0"` y a un jugador contra sí mismo | Que `raise` lanza excepciones |
| Que una liga de 4 genera 6 emparejamientos | Que `itertools.combinations` combina |
| Que `desde_json` convierte el JSON en los jugadores correctos | Que `json.load` parsea JSON o que `open` abre ficheros |
| Que el ranking sale ordenado por ELO descendente | Que `sorted` ordena |

La regla práctica: **si el test fallara, ¿el bug estaría en nuestro código?** Si la
respuesta es no, ese test no aporta nada.

Tampoco vamos a testear en este ejercicio los métodos que solo **imprimen**
(`mostrar_ranking`, `mostrar_historial`, `organizar`): se puede hacer, pero no es tan importante como el resto de funcionalidades.

---

## Parte 1: La estructura de los tests

### Paso 1: la carpeta `tests/` y la configuración

Crea una carpeta `tests/` en la raíz del proyecto (al lado de `ajedrez/` y `main.py`) y
añade al final de `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]   # dónde buscar los tests
pythonpath = ["."]      # para que `from ajedrez... import` funcione desde tests/
```

La segunda línea es importante: los tests van a hacer `from ajedrez.jugador import
Jugador`, igual que `main.py`. `main.py` puede porque se ejecuta desde la raíz del
proyecto; los tests están en otra carpeta, y `pythonpath = ["."]` le dice a pytest que
añada la raíz del proyecto a las rutas donde buscar módulos.

### Paso 2: los tres elementos

En una carpeta de tests hay tres tipos de cosas:

1. **Los tests.** Ficheros `test_*.py` con funciones `test_*`. Cada función es un test:
   prepara un escenario, ejecuta la acción que quiere comprobar y hace uno o varios
   `assert`. pytest los descubre solo por el
   nombre.

2. **Las fixtures.** Casi todos los tests necesitan un escenario de partida: un jugador
   recién creado, una plataforma con cuatro jugadores... En vez de construirlo en cada
   test, se escribe **una vez** como función decorada con `@pytest.fixture`, y cualquier
   test que **ponga su nombre como parámetro** lo recibe ya construido. pytest ejecuta la
   fixture **de nuevo antes de cada test**: aunque un test modifique su plataforma, el
   siguiente recibe una limpia. Eso es lo que hace a los tests independientes.

3. **`conftest.py`.** El fichero donde viven las fixtures compartidas. pytest lo carga
   automáticamente: no hace falta importarlo desde los tests, basta con que esté en la
   carpeta.

### Paso 3: crea `tests/conftest.py` con estas fixtures

Todos los tests del ejercicio van a usar estos cuatro escenarios. Escríbelos en
`tests/conftest.py`:

- `magnus` → `Jugador("Magnus", "NOR")`
- `hikaru` → `Jugador("Hikaru", "USA")`
- `partida` → `Partida(magnus, hikaru, "1-0", BLITZ)`. Fíjate: **una fixture puede pedir
  otras fixtures como parámetros**, y pytest las construye en cadena.
- `plataforma` → una `Plataforma()` con cuatro jugadores registrados: Magnus (NOR),
  Hikaru (USA), Ding (CHN) y Judit (HUN).

La primera queda así; las otras tres siguen el mismo patrón:

```python
import pytest

from ajedrez.jugador import Jugador


@pytest.fixture
def magnus():
    return Jugador("Magnus", "NOR")
```

### Paso 4: el primer test

Crea `tests/test_jugador.py` con un único test que pida la fixture `magnus` y compruebe
que un jugador nuevo empieza con el ELO inicial:

```python
def test_jugador_nuevo_empieza_con_elo_inicial(magnus):
    assert magnus.elo == 1200
```

Ejecútalo:

```bash
uv run pytest -v
```

```
collected 1 item

tests/test_jugador.py::test_jugador_nuevo_empieza_con_elo_inicial PASSED [100%]

============================== 1 passed in 0.01s ===============================
```

Si ves eso, la estructura funciona. Todo lo que viene ahora es añadir tests.

---

## Parte 2: Un fichero de tests por componente

Vamos a crear un fichero de tests por cada módulo del paquete. Para cada uno te damos
**un test concreto** que debes escribir (con la herramienta de pytest que toca) y al final
tienes que **añadir al menos un test propio**: piensa qué lógica de ese componente
escribiste tú y qué debería cumplirse siempre.

### `tests/test_jugador.py`

**Test dado: la regla del ELO con `parametrize`.** `variacion_elo(puntos, k)` tiene tres
casos (victoria, derrota, tablas), y escribir tres tests casi iguales es un desperdicio.
Usa `@pytest.mark.parametrize` para que **un solo test** los recorra:

```python
@pytest.mark.parametrize(
    "puntos, k, esperado",
    [
        (1, 20, 20),    # victoria: suma K
        (0, 20, -20),   # derrota: resta K
        (0.5, 20, 0),   # tablas: no cambia
    ],
)
def test_variacion_elo(puntos, k, esperado):
    assert Jugador.variacion_elo(puntos, k) == esperado
```

En `pytest -v` verás tres líneas, una por caso: `test_variacion_elo[1-20-20]`,
`test_variacion_elo[0-20--20]`... Si una falla, sabes exactamente qué combinación.

**Ideas para tus tests propios:** que `magnus.elo = 9999` lanza `AttributeError` (la
propiedad de solo lectura del ejercicio 3); que `porcentaje_victorias` es `0.0` cuando no
hay partidas (¡el caso límite de la división por cero!); que `desde_dict` y `a_dict` son
inversos.

### `tests/test_partida.py`

**Test dado: una validación con `pytest.raises`.** Comprobar que el código **falla cuando
debe** es tan importante como que funcione. `Partida` debe rechazar un resultado que no
existe:

```python
def test_resultado_invalido_lanza_error(magnus, hikaru):
    with pytest.raises(PartidaInvalida):
        Partida(magnus, hikaru, "2-0", BLITZ)
```

La llamada que debe fallar va **dentro** del `with`. Si no lanza `PartidaInvalida`, el
test falla.

**Ideas para tus tests propios:** que un jugador no puede jugar contra sí mismo; que
`puntos()` devuelve `(1, 0)`, `(0, 1)` y `(0.5, 0.5)` según el resultado (¿parametrize?);
que `rival_de` y `color_de` devuelven lo correcto para los dos jugadores (usa la fixture
`partida`).

### `tests/test_plataforma.py`

**Test dado: jugar una partida cambia el estado de los dos jugadores.** Es el método más
importante de la plataforma, y hace varias cosas a la vez; comprueba las que más importan:

```python
def test_jugar_actualiza_el_elo_de_ambos(plataforma):
    plataforma.jugar("Magnus", "Hikaru", "1-0", BLITZ)

    assert plataforma["Magnus"].elo == 1220
    assert plataforma["Hikaru"].elo == 1180
    assert len(plataforma.partidas) == 1
```

Observa el patrón *Arrange – Act – Assert*: la fixture prepara, la primera línea actúa, el
resto comprueba.

**Ideas para tus tests propios:** que registrar un nombre repetido lanza
`JugadorDuplicado`; que `plataforma["Bobby"]` lanza `JugadorNoRegistrado`; que recorrer
la plataforma con `for` devuelve los jugadores de mayor a menor ELO (juega un par de
partidas primero para que los ELO sean distintos).

### `tests/test_torneo.py`

**Test dado: los emparejamientos de una liga.** Es lógica 100 % nuestra: con cuatro
participantes tiene que haber seis parejas, y cada pareja una sola vez:

```python
def test_liga_de_cuatro_tiene_seis_emparejamientos(plataforma):
    liga = Liga("Liga", plataforma, RAPID, ["Magnus", "Hikaru", "Ding", "Judit"])

    emparejamientos = liga.emparejamientos()

    assert len(emparejamientos) == 6
    assert ("Magnus", "Hikaru") in emparejamientos
    assert ("Hikaru", "Magnus") not in emparejamientos
```

**Ideas para tus tests propios:** que una `Eliminatoria` con tres participantes lanza
`TorneoInvalido`; que `Torneo(...)` no se puede instanciar (`TypeError`); que después de
`jugar(...)` una eliminatoria de cuatro, `campeon()` es quien esperas.

Cuando termines, `uv run pytest` debería ejecutar unos 20 tests en verde.

---

## Parte 3: Testear la lectura del JSON sin leer ningún fichero (mocking)

Queda `Plataforma.desde_json(ruta)`. Mira lo que hace:

```python
    @classmethod
    def desde_json(cls, ruta):
        with open(ruta, encoding="utf-8") as f:
            datos = json.load(f)
        plataforma = cls()
        for datos_jugador in datos["jugadores"]:
            jugador = Jugador.desde_dict(datos_jugador)
            plataforma.jugadores[jugador.nombre] = jugador
        return plataforma
```

Mezcla dos cosas: **abrir y parsear un fichero** (`open` + `json.load`, que no es código
nuestro) y **construir la plataforma a partir del diccionario**. Lo que
queremos testear es lo segundo. Podríamos hacer un test que lea `datos/jugadores.json`,
pero sería un mal test:

- Depende de un fichero externo: si alguien cambia el ELO de Magnus en el JSON, el test
  falla sin que el código esté mal. Si el fichero no está (otra máquina, otra carpeta),
  falla también.
- Toca el disco: es lento y no está aislado. Los tests deben ser rápidos, independientes
  y repetibles.

### La idea del mocking

Un **mock** es un objeto falso que sustituye temporalmente a una pieza real durante un
test y se comporta como nosotros digamos. Aquí la pieza que queremos sustituir es
`open`: en lugar de abrir un fichero, queremos que "devuelva" un JSON que escribimos en
el propio test. Así el test controla al 100 % los datos de entrada y solo comprueba
nuestra lógica.

Para hacerlo cómodo desde pytest usaremos el plugin **pytest-mock**. Instálalo como
dependencia de desarrollo:

```bash
uv add --dev pytest-mock
```

El plugin añade una fixture llamada **`mocker`**: la pides como parámetro del test, igual
que `magnus` o `plataforma`, y te da dos herramientas:

- **`mocker.mock_open(read_data=texto)`** crea un doble de `open` que, al leerlo, devuelve
  `texto`.
- **`mocker.patch("builtins.open", doble)`** sustituye `open` por ese doble **durante el
  resto del test** y devuelve el mock para que puedas interrogarlo. Al terminar el test,
  pytest-mock deshace el cambio solo: `open` vuelve a ser el de verdad. El objetivo es
  `"builtins.open"` porque `plataforma.py` usa el `open` incorporado de Python.

### El test

Añade a `tests/test_plataforma.py` (no hace falta importar nada nuevo: `mocker` es una
fixture):

```python
def test_desde_json_construye_los_jugadores_del_fichero(mocker):
    contenido = """
    {
      "jugadores": [
        {"nombre": "Ana", "pais": "ESP", "elo": 2000, "victorias": 3, "derrotas": 1, "tablas": 0},
        {"nombre": "Luis", "pais": "ARG", "elo": 1800, "victorias": 1, "derrotas": 3, "tablas": 2}
      ]
    }
    """
    # Durante este test, `open` es un doble que devuelve `contenido` al leer
    abrir_falso = mocker.patch("builtins.open", mocker.mock_open(read_data=contenido))

    plataforma = Plataforma.desde_json("cualquier/ruta.json")

    abrir_falso.assert_called_once_with("cualquier/ruta.json", encoding="utf-8")
    assert len(plataforma) == 2
    assert plataforma["Ana"].elo == 2000
    assert plataforma["Luis"].victorias == 1
```

Fíjate en tres cosas:

- La ruta `"cualquier/ruta.json"` **no existe**, y da igual: `open` es falso. El test
  pasa igual aunque borres la carpeta `datos/`.
- `abrir_falso` es el mock. Además de sustituir a `open`, **recuerda cómo se le llamó**, y
  `assert_called_once_with(...)` comprueba que `desde_json` abrió exactamente la ruta que
  le pasamos, con `encoding="utf-8"`. Es la parte de "nuestro código" en esa línea.
- Los `assert` finales comprueban lo que de verdad nos importa: que el JSON se ha
  convertido en los jugadores correctos.

**Test propio:** un JSON con la lista `"jugadores"` vacía debe producir una plataforma con
`len(plataforma) == 0`. (Pide también `mocker`, aunque no necesites guardar el mock.)

---

## Para terminar

Pasa toda la batería:

```bash
uv run pytest -v
```

Y ahora prueba la red de seguridad: abre `ajedrez/jugador.py`, cambia en `variacion_elo`
el `return -k` de la derrota por `return k`, y vuelve a ejecutar los tests. Verás fallar
varios a la vez (el parametrizado de `variacion_elo`, el de `jugar`, el del ranking...):
pytest te dice **qué** ha fallado, **dónde** y **qué valor esperaba frente a cuál ha
recibido**. Deshaz el cambio y comprueba que todo vuelve a verde. Eso es exactamente para
lo que sirven los tests.
