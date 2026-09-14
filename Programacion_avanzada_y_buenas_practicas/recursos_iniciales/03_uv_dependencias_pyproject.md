# Crear un proyecto de Python desde cero con `uv`

En los vídeos anteriores preparamos el editor (VSCode) e instalamos Python usando
`uv`. Ahora vamos a dar el salto a lo que de verdad hacemos en el día a día:
**arrancar un proyecto de Python desde cero**, entender qué archivos lo componen y,
sobre todo, **gestionar sus dependencias** de forma ordenada con `uv` y el archivo
**`pyproject.toml`**.

> 📚 Documentación oficial de referencia:
> **[docs.astral.sh/uv](https://docs.astral.sh/uv/)**.

---

## 1. ¿Qué es un "proyecto" de Python?

Hasta ahora, ejecutar Python podía ser tan simple como tener un archivo `.py` suelto.
Pero un proyecto real es algo más: es una **carpeta organizada** que contiene nuestro
código, la **lista de librerías que necesita** (sus *dependencias*) y la
**información que lo describe** (nombre, versión, versión de Python requerida...).

El objetivo de organizarlo bien es conseguir que el proyecto sea:

- **Reproducible**: que cualquier persona (o tú mismo en otro ordenador) pueda
  instalar exactamente lo mismo y que funcione igual.
- **Aislado**: que las librerías de este proyecto no se mezclen con las de otros.
- **Compartible**: que se pueda subir a Git y que otra persona lo ponga en marcha en
  segundos.

### ¿Qué son las dependencias?

Casi ningún proyecto se escribe partiendo de cero absoluto. Usamos **librerías** que
otras personas han escrito: para hacer peticiones web (`requests`), para manejar
datos (`pandas`), para crear APIs (`fastapi`), etc. Esas librerías son las
**dependencias** de nuestro proyecto: código externo del que dependemos para
funcionar.

El reto es **llevar la cuenta** de qué dependencias usamos y de **qué versión** de
cada una, para que el proyecto sea reproducible. De eso se encargan `uv` y
`pyproject.toml`.

---

## 2. El corazón del proyecto: `pyproject.toml`

El archivo **`pyproject.toml`** es el **archivo de configuración estándar** de un
proyecto Python moderno. Está definido por la propia comunidad de Python (no es algo
exclusivo de `uv`) y es donde se declara toda la información del proyecto.

> El formato **TOML** (*Tom's Obvious Minimal Language*) es un formato de
> configuración pensado para ser fácil de leer y escribir por humanos. Se organiza en
> **secciones** (entre corchetes, `[seccion]`) y **pares clave = valor**.
> Puedes consultar su especificación en **[toml.io](https://toml.io/en/)**.

Un `pyproject.toml` sencillo tiene este aspecto:

```toml
[project]
name = "mi-proyecto"
version = "0.1.0"
description = "Un proyecto de ejemplo"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []
```

Veamos qué significa cada campo de la sección `[project]`:

| Campo | Qué indica |
|-------|------------|
| `name` | El nombre del proyecto. |
| `version` | Su versión actual (empezamos por la `0.1.0`). |
| `description` | Una descripción breve de qué hace. |
| `readme` | El archivo con la documentación principal (normalmente `README.md`). |
| `requires-python` | La versión/versiones de Python que necesita el proyecto. |
| `dependencies` | **La lista de librerías que el proyecto necesita.** Empieza vacía. |

> 💡 La gran ventaja: en lugar de tener las dependencias "sueltas" instaladas en
> nuestro ordenador, quedan **declaradas en un archivo** que viaja junto al código.
> Quien reciba el proyecto sabe exactamente qué necesita.

> 📚 **Documentación oficial sobre `pyproject.toml`:**
> - [Guía para escribir un `pyproject.toml`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) (Python Packaging).
> - [Especificación completa del `pyproject.toml`](https://packaging.python.org/en/latest/specifications/pyproject-toml/) y de la sección `[project]`.
> - [Estructura de un proyecto en `uv`](https://docs.astral.sh/uv/concepts/projects/layout/) y [configuración del proyecto](https://docs.astral.sh/uv/concepts/projects/config/).

---

## 3. Crear el proyecto con `uv init`

No hace falta escribir el `pyproject.toml` a mano. `uv` puede generar la estructura
inicial de un proyecto por nosotros con un solo comando.

Para crear un proyecto nuevo en una carpeta:

```bash
uv init mi-proyecto
```

Esto crea una carpeta `mi-proyecto/` con la estructura básica. Si ya estás **dentro**
de la carpeta donde quieres el proyecto, puedes ejecutar simplemente:

```bash
uv init
```

### ¿Qué genera `uv init`?

Tras ejecutarlo, encontrarás algo así:

```
mi-proyecto/
├── .git/                # repositorio de Git (control de versiones)
├── .gitignore           # archivos que Git debe ignorar
├── .python-version      # versión de Python fijada para el proyecto
├── README.md            # documentación inicial
├── main.py              # un archivo de ejemplo para empezar
└── pyproject.toml       # ⭐ la configuración del proyecto
```

Fíjate en que `uv` ya nos prepara prácticamente todo: el `pyproject.toml`, la versión
de Python del proyecto e incluso inicializa Git.

> 💡 Abre el `pyproject.toml` recién creado en VSCode y verás la sección `[project]`
> que comentábamos en el punto anterior, lista para empezar a trabajar.

---

## 4. Fijar (pinear) la versión de Python del proyecto

Una de las grandes ventajas de `uv` es que cada proyecto puede usar **su propia
versión de Python**, independientemente de las demás que tengas instaladas. A
"amarrar" una versión concreta a un proyecto se le llama **pinear** la versión.

### Dos conceptos que conviene no confundir

Hay **dos sitios** donde aparece la versión de Python, y significan cosas distintas:

| Dónde | Qué representa |
|-------|----------------|
| `.python-version` (archivo en la raíz del proyecto) | La versión **exacta** que `uv` usará para *este* proyecto. Es lo que se "pinea". |
| `requires-python` (en el `pyproject.toml`) | El **rango** de versiones con las que el proyecto declara ser compatible (p. ej. `>=3.12`). |

Dicho de forma sencilla: `requires-python` dice "funciono con la 3.12 o superior", y
`.python-version` dice "para trabajar, usa **exactamente** la 3.12.3". La versión
pineada siempre debe estar dentro del rango declarado en `requires-python`.

### ¿Se hace al empezar el proyecto con `uv init`?

Sí. De hecho, cuando ejecutas `uv init`, `uv` **ya crea un `.python-version`** con la
versión por defecto. Pero puedes elegir tú la versión desde el principio con la
opción `--python`:

```bash
uv init mi-proyecto --python 3.12.3
```

Esto crea el proyecto y deja pineada la **3.12.3** en el `.python-version`.

> 💡 Si la versión que pides no la tienes instalada, `uv` se encarga de descargarla
> automáticamente (como vimos en el vídeo anterior).

---

## 5. Añadir dependencias con `uv add`

Aquí está el núcleo del vídeo. Para añadir una librería al proyecto, usamos
**`uv add`**:

```bash
uv add requests
```

> 📂 **¿Desde qué directorio lo ejecuto?** Desde la **carpeta del proyecto**, es
> decir, la que contiene el `pyproject.toml` (en nuestro ejemplo, `mi-proyecto/`).
> `uv` busca el `pyproject.toml` en la carpeta actual y, si no lo encuentra, va
> subiendo por las carpetas superiores; por eso también funciona desde una subcarpeta
> del proyecto. Lo más sencillo y recomendable es situarte en la raíz del proyecto
> antes de ejecutarlo:
>
> ```bash
> cd mi-proyecto
> uv add requests
> ```
>

Con ese único comando, `uv` hace **varias cosas a la vez**:

1. **Añade la librería al `pyproject.toml`**, dentro de `dependencies`.
2. **La instala** en el entorno virtual `.venv` (creándolo si no existía).
3. **Actualiza el archivo `uv.lock`** (lo vemos en el punto 8) con la versión exacta.

Si ahora abres el `pyproject.toml`, la sección de dependencias habrá cambiado:

```toml
dependencies = [
    "requests>=2.32.0",
]
```

### Especificar versiones

Podemos pedir una versión concreta o un rango:

```bash
uv add "requests==2.32.0"     # exactamente esa versión
uv add "requests>=2.30"       # esa versión o superior
```

### Añadir varias a la vez

```bash
uv add pandas numpy
```

---

## 6. Dependencias de desarrollo

No todas las dependencias son iguales. Algunas las necesita el proyecto **para
funcionar** (por ejemplo, `requests`). Otras solo las usamos **mientras
desarrollamos**: herramientas de testing, de formateo, de linting... pero no hacen
falta para que el programa funcione una vez desplegado.

A estas últimas las llamamos **dependencias de desarrollo** y se añaden con la opción
`--dev`:

```bash
uv add --dev pytest
```

Esto las guarda en una sección aparte del `pyproject.toml`, para distinguirlas
claramente de las dependencias "de verdad":

```toml
[dependency-groups]
dev = [
    "pytest>=8.0",
]
```

> 💡 Separar las dependencias de desarrollo es una buena práctica: mantiene el
> proyecto ligero en producción y deja claro qué es imprescindible y qué es solo
> herramienta de trabajo.

---

## 7. `uv.lock`: el archivo que garantiza la reproducibilidad

Cuando añadimos dependencias, `uv` crea (y mantiene) un archivo llamado
**`uv.lock`**. Es uno de los conceptos más importantes de este vídeo.

- El `pyproject.toml` dice **qué** queremos, a veces de forma flexible
  (`requests>=2.30`).
- El `uv.lock` registra **exactamente qué versiones** se instalaron de **cada
  librería**, incluidas las dependencias de nuestras dependencias.

¿Por qué importa tanto? Porque garantiza que el proyecto sea **100% reproducible**:
cualquiera que use el `uv.lock` instalará **exactamente las mismas versiones** que tú,
evitando el clásico "en mi máquina funciona".

> ✅ **Regla práctica:** el `pyproject.toml` **y** el `uv.lock` **sí se suben a Git**.
> La carpeta `.venv/` **no**.

---

## 8. Quitar dependencias y sincronizar el entorno

### Eliminar una dependencia

Para quitar una librería que ya no usamos:

```bash
uv remove requests
```

`uv` la elimina del `pyproject.toml`, del `uv.lock` y del entorno virtual.

### Recrear el entorno con `uv sync`

Imagina que te descargas un proyecto de un compañero (o lo clonas de Git). Tendrás el
`pyproject.toml` y el `uv.lock`, pero **no** la carpeta `.venv`. Para reconstruir el
entorno con exactamente las dependencias correctas, basta con:

```bash
uv sync
```

`uv sync` lee el `uv.lock` y deja el entorno virtual con **justo** las versiones
indicadas. Esto es precisamente lo que hace que compartir proyectos sea tan cómodo:
clonar, `uv sync` y a trabajar.

---

## 9. Ejecutar el código con `uv run`

Una vez tenemos dependencias instaladas, queremos ejecutar nuestro programa **usando
el entorno del proyecto**. La forma recomendada con `uv` es **`uv run`**:

```bash
uv run main.py
```

O para abrir la consola interactiva de Python del proyecto:

```bash
uv run python
```

La ventaja de `uv run` es que **se asegura de usar el entorno virtual correcto** (y de
que esté sincronizado) sin que tengamos que activarlo manualmente. Por ejemplo, para
lanzar los tests con pytest:

```bash
uv run pytest
```

---

## 10. Resumen y chuleta de comandos

En este vídeo hemos aprendido a montar un proyecto de Python desde cero:

1. Un **proyecto** es una carpeta organizada con código, dependencias e información,
   pensada para ser **reproducible, aislada y compartible**.
2. El **`pyproject.toml`** es el archivo estándar que **describe el proyecto** y
   **declara sus dependencias**.
3. Con **`uv init`** generamos la estructura inicial automáticamente.
4. Cada proyecto puede **pinear su versión de Python** en el `.python-version`, ya sea
   al crearlo (`uv init --python`) o cambiándola después (`uv python pin`).
5. `uv` gestiona por nosotros el **entorno virtual** (`.venv`), sin tener que crearlo
   ni activarlo a mano.
6. Con **`uv add`** / **`uv remove`** gestionamos las dependencias, que quedan
   declaradas en el `pyproject.toml`.
7. El **`uv.lock`** fija las versiones exactas y garantiza la **reproducibilidad**.
8. Con **`uv sync`** recreamos el entorno en cualquier máquina, y con **`uv run`**
   ejecutamos el código en el entorno correcto.

### Chuleta de comandos

| Comando | Para qué sirve |
|---------|----------------|
| `uv init mi-proyecto` | Crear un proyecto nuevo. |
| `uv init mi-proyecto --python 3.12.3` | Crear un proyecto pineando la versión de Python. |
| `uv python pin <versión>` | Cambiar la versión de Python del proyecto. |
| `uv add <librería>` | Añadir una dependencia. |
| `uv add --dev <librería>` | Añadir una dependencia de desarrollo. |
| `uv remove <librería>` | Quitar una dependencia. |
| `uv sync` | Reconstruir el entorno a partir del `uv.lock`. |
| `uv run <archivo/comando>` | Ejecutar código en el entorno del proyecto. |
| `uv lock` | Regenerar el archivo de bloqueo. |
| `uv tree` | Ver el árbol de dependencias del proyecto. |

> 📚 Para profundizar, consulta la
> [guía de proyectos de `uv`](https://docs.astral.sh/uv/guides/projects/) y la
> [gestión de dependencias](https://docs.astral.sh/uv/concepts/projects/dependencies/)
> en su documentación oficial.

Con esto, ya sabemos crear proyectos limpios y reproducibles. En los próximos vídeos
empezaremos a **escribir código** dentro de esta estructura.
