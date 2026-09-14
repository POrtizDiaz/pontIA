# Instalar Python desde cero

En el vídeo anterior dejamos preparado el editor (VSCode). Ahora toca lo más
importante: **instalar Python** en nuestro equipo. Veremos primero la forma
"clásica" (descargándolo de la página oficial) y por qué resulta incómoda, y
después introduciremos una herramienta moderna, **`uv`**, que nos hará la vida mucho
más fácil. A partir de ahí, instalaremos Python a través de `uv`.

> 📌 En este vídeo **solo** instalamos Python. Todo lo relativo a dependencias y
> entornos virtuales con `uv` lo veremos en los próximos vídeos.

---

## 1. La forma clásica: la página oficial de Python

La web oficial de Python es **[python.org](https://www.python.org)**. Es el lugar
donde se publica el lenguaje y donde tradicionalmente se descarga el instalador.

Merece la pena conocerla:

- En el menú **`Downloads`** la web detecta tu sistema operativo y te ofrece el
  instalador recomendado.
- En **`Downloads > All releases`** puedes ver **todas las versiones** publicadas y
  descargar una concreta.
- Encontrarás también la **documentación oficial**, que es una referencia excelente.

La idea, a grandes rasgos, es sencilla: descargas el instalador correspondiente a tu
sistema operativo, lo ejecutas y ya tienes Python en el equipo.

### ¿Por qué esta forma resulta incómoda?

Aunque funciona, instalar Python "a mano" desde la web tiene varios inconvenientes,
sobre todo en cuanto empiezas a usar Python en serio:

- **Configurar el `PATH`.** Para poder llamar a Python desde la terminal, el
  instalador tiene que dejarlo bien registrado en el sistema. Es un paso fácil de
  olvidar (en Windows es la típica casilla que hay que marcar) y, cuando sale mal, el
  ordenador "no encuentra" Python y empiezan los problemas.
- **No romper el Python del sistema.** En macOS y Linux ya viene un Python
  preinstalado del que depende el propio sistema operativo. Si lo tocas o lo
  confundes con el tuyo, puedes provocar fallos difíciles de diagnosticar.
- **El lío de `python` vs `python3`.** Según el sistema y cómo se instalara, el
  comando a veces es uno y a veces otro, lo que genera bastante confusión.

### El verdadero problema: mantener varias versiones

El mayor dolor de cabeza llega cuando necesitas **varias versiones de Python a la
vez**, algo muy habitual: un proyecto antiguo pide la 3.10, otro más nuevo la 3.12,
etc.

Con la forma clásica, esto significa **instalar cada versión por separado** y luego
**pelearte para decir cuál usar en cada momento**: ajustar el `PATH` a mano,
acordarte de qué instalador puso qué, instaladores que se pisan entre sí... Es un
proceso manual, frágil y propenso a errores.

> ⚠️ En resumen: la forma clásica vale para instalar **una** versión y poco más. En
> cuanto quieres gestionar **varias versiones** de forma cómoda y sin romper nada,
> se queda muy corta. Justo aquí es donde entra **`uv`**.

---

## 2. Una forma moderna: `uv`

**`uv`** es una herramienta moderna y muy rápida (escrita en Rust) creada por
*Astral*. Sirve como gestor "todo en uno" para Python: puede **instalar versiones de
Python**, crear entornos virtuales y gestionar dependencias.

> 📚 Toda su documentación oficial está en
> **[docs.astral.sh/uv](https://docs.astral.sh/uv/)**.

> En esta clase usaremos `uv` **solo para instalar Python**. Sus otras capacidades
> (entornos y dependencias) las veremos más adelante.

### ¿Qué ventajas tiene `uv`?

- **Instala y gestiona varias versiones de Python por ti**, sin pelearte con el
  `PATH` ni con instaladores. Cambiar de versión es un solo comando.
- **Es muy rápido**: notablemente más veloz que las herramientas tradicionales.
- **Es multiplataforma y consistente**: los mismos comandos funcionan igual en
  Windows, macOS y Linux.
- **No interfiere con otros Python ya instalados**: el propio `uv` gestiona sus descargas de Python sin interferir con versiones existentes.
- **Unifica herramientas**: reemplaza a varias utilidades clásicas (como `pyenv`,
  `virtualenv`, `pip`...) en una sola.

---

## 3. Instalar `uv`

Los comandos oficiales y actualizados están siempre en la
[guía de instalación de `uv`](https://docs.astral.sh/uv/getting-started/installation/).

### En Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

> 💡 Alternativa con **winget**: `winget install --id=astral-sh.uv -e`

### En macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

> 💡 Alternativa con **Homebrew** (macOS): `brew install uv`

### Comprobar que `uv` se ha instalado

Cierra y vuelve a abrir la terminal (para que se actualice el `PATH`) y ejecuta:

```bash
uv --version
```

Deberías ver el número de versión de `uv`. Si es así, ya está listo.

---

## 4. Instalar Python con `uv`

Ahora viene lo interesante. Con `uv` instalado, conseguir Python es un único
comando (igual en todos los sistemas operativos):

```bash
uv python install 3.12.3
```

Con esto, `uv` descarga e instala la versión **3.12.3** por nosotros.

### Comandos útiles de Python con `uv`

**Ver las versiones de Python que tienes instaladas y disponibles:**

```bash
uv python list
```

**Saber dónde está el Python que se usará:**

```bash
uv python find
```

**Instalar otra versión** (puedes tener varias a la vez sin conflictos):

```bash
uv python install 3.11
```

**Fijar la versión de Python para el proyecto actual** (crea un archivo
`.python-version` en la carpeta):

```bash
uv python pin 3.12.3
```

> 💡 Fíjate en lo cómodo que resulta: tener varias versiones conviviendo y elegir
> cuál usar en cada proyecto, sin tocar el `PATH` ni romper nada del sistema. Esto,
> a mano, era justamente lo complicado de la forma clásica.

> 📚 Puedes ver todas las opciones para gestionar versiones de Python en la
> [documentación de `uv` sobre versiones de Python](https://docs.astral.sh/uv/concepts/python-versions/).

---

## Resumen

En esta sesión hemos aprendido a instalar Python:

1. **La forma clásica:** descargar el instalador desde
   **[python.org](https://www.python.org)**. Funciona para una versión, pero es
   incómoda (configurar el `PATH`, no romper el Python del sistema) y, sobre todo,
   **mantener varias versiones a la vez se vuelve un quebradero de cabeza**.
2. **`uv`:** una herramienta moderna y rápida que **instala y gestiona las versiones
   de Python por nosotros** con un solo comando, igual en cualquier sistema
   operativo.
3. A partir de ahora usaremos **`uv`** para gestionar nuestras versiones de Python,
   empezando por la **3.12.3**.

En las próximas clases daremos el siguiente paso: usar `uv` para crear **entornos
virtuales** y **gestionar las dependencias** de nuestros proyectos.
