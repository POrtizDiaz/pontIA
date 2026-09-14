# Calidad del código con Ruff

En los vídeos anteriores aprendimos a montar un proyecto de Python con `uv` y a
gestionar sus dependencias. Ya podemos escribir código... pero escribir código que
**funcione** no es lo mismo que escribir código **de calidad**. En este vídeo veremos
**Ruff**, una herramienta que nos ayuda a mantener nuestro código limpio, consistente
y libre de errores tontos.

> 📚 Documentación oficial de referencia:
> **[docs.astral.sh/ruff](https://docs.astral.sh/ruff/)**.

---

## 1. ¿Qué es Ruff?

**Ruff** es una herramienta moderna y extremadamente rápida (escrita en Rust, igual
que `uv`, y también de *Astral*) que cumple dos funciones principales:

- **Linter**: analiza tu código en busca de **problemas** sin llegar a ejecutarlo:
  imports que no usas, variables declaradas y nunca utilizadas, errores potenciales,
  malas prácticas, etc.
- **Formateador (*formatter*)**: **reordena y da formato** a tu código de manera
  automática para que siga siempre el mismo estilo (espaciado, comillas, longitud de
  línea...), parecido a lo que hace *Black*.

### ¿Por qué nos importa la calidad del código?

- **Legibilidad**: un código con un estilo consistente es mucho más fácil de leer,
  tanto para ti dentro de unos meses como para tus compañeros.
- **Menos errores**: muchos fallos (un import que falta, una variable mal escrita)
  se detectan **antes** de ejecutar el programa.
- **Trabajo en equipo**: si todos seguimos el mismo estilo, dejamos de discutir sobre
  comas y espacios y nos centramos en lo importante.

### ¿Qué es un *linter* y qué es un *formatter*?

Conviene distinguirlos bien, porque Ruff hace las dos cosas:

| Herramienta | Qué hace | Ejemplo |
|-------------|----------|---------|
| **Linter** | **Detecta** problemas y te avisa (y algunos los puede arreglar). | "Has importado `os` pero no lo usas." |
| **Formatter** | **Reescribe** el código para que tenga un formato uniforme. | Convierte `x=1` en `x = 1`. |

> 💡 Antes se usaban varias herramientas distintas (Flake8, isort, Black,
> pylint...). Ruff las **reemplaza a casi todas** en una sola, y es muchísimo más
> rápido.

---

## 2. Instalar Ruff con `uv`

Como Ruff es una herramienta que solo usamos **mientras desarrollamos** (no es
necesaria para que el programa funcione en producción), la añadimos como
**dependencia de desarrollo**, tal y como vimos en el vídeo anterior:

```bash
uv add --dev ruff
```

Esto añade Ruff a la sección de dependencias de desarrollo del `pyproject.toml`:

```toml
[dependency-groups]
dev = [
    "ruff>=0.6.0",
]
```

Para comprobar que se ha instalado correctamente:

```bash
uv run ruff --version
```

> 💡 Recuerda ejecutarlo desde la **carpeta del proyecto** (la que tiene el
> `pyproject.toml`). Usamos `uv run` para que Ruff se ejecute dentro del entorno
> virtual del proyecto.

---

## 3. Los dos comandos principales

Ruff se usa, básicamente, con dos comandos:

### Revisar el código (linter)

```bash
uv run ruff check
```

Analiza todos los archivos del proyecto y te muestra los problemas que encuentra (sin
modificar nada).

### Formatear el código (formatter)

```bash
uv run ruff format
```

Reescribe los archivos para dejarlos con un formato uniforme.

> 💡 Puedes indicar un archivo o carpeta concretos: `uv run ruff check main.py`.

---

## 4. Ejemplo práctico: rompamos `main.py` a propósito

La mejor forma de entender Ruff es verlo en acción. Vamos a coger el archivo
`main.py` que creó `uv init` y a **introducir varios fallos** típicos para que Ruff
los detecte.

### Paso 1: escribir un `main.py` con problemas

Abre `main.py` en VSCode y déjalo así:

```python
import os
import math


def saludar(nombre):
    mensaje = "Hola, " + nombre
    numero_no_usado = 42
    print(mensaje)


saludar("Mundo")
```

¿Qué problemas hemos metido aquí? A simple vista parece correcto, pero hay tres:

1. **`import os`** — importamos `os` pero **no lo usamos** en ningún sitio.
2. **`import math`** — lo mismo: importado y nunca utilizado.
3. **`numero_no_usado = 42`** — una variable que creamos pero **nunca usamos**.

Son errores muy comunes en el día a día y, aunque el programa *funciona*, "ensucian"
el código.

### Paso 2: pasar el linter

Ahora ejecutamos Ruff sobre el proyecto:

```bash
uv run ruff check
```

La salida será parecida a esta:

```
main.py:1:8: F401 [*] `os` imported but unused
main.py:2:8: F401 [*] `math` imported but unused
main.py:7:5: F841 [*] Local variable `numero_no_usado` is assigned to but never used
Found 3 errors.
[*] 3 fixable with the `--fix` option.
```

Vamos a leer una de esas líneas, porque es importante entender el formato:

```
main.py:1:8: F401 [*] `os` imported but unused
   │     │ │   │   │     └── descripción del problema
   │     │ │   │   └──────── [*] significa que Ruff puede arreglarlo automáticamente
   │     │ │   └──────────── código de la regla (F401)
   │     │ └──────────────── columna
   │     └────────────────── número de línea
   └──────────────────────── archivo
```

> 💡 Cada problema tiene un **código de regla** (como `F401` o `F841`). Puedes buscar
> qué significa cualquiera de ellos en la
> [lista de reglas de Ruff](https://docs.astral.sh/ruff/rules/).

### Paso 3: arreglarlo automáticamente

Fíjate en que Ruff nos dice que los 3 errores son **arreglables automáticamente**
(`[*] 3 fixable`). Podemos pedirle que los corrija él mismo:

```bash
uv run ruff check --fix
```

Ruff eliminará los imports y la variable que no se usan. Si vuelves a abrir `main.py`,
quedará limpio:

```python
def saludar(nombre):
    mensaje = "Hola, " + nombre
    print(mensaje)


saludar("Mundo")
```

Y si ahora ejecutas de nuevo `uv run ruff check`, deberías ver:

```
All checks passed!
```

### Paso 4: probar el formateador

Vamos ahora a "afear" el formato (sin meter errores de lógica). Cambia el cuerpo de la
función para que quede mal espaciado:

```python
def saludar(nombre):
    mensaje="Hola, "+nombre
    print( mensaje )


saludar("Mundo")
```

Pasamos el formateador:

```bash
uv run ruff format
```

Ruff reescribe el archivo con un estilo correcto y uniforme:

```python
def saludar(nombre):
    mensaje = "Hola, " + nombre
    print(mensaje)


saludar("Mundo")
```

> 💡 El **linter** (`ruff check`) se fija en *problemas*; el **formatter**
> (`ruff format`) se fija en el *aspecto*. Lo normal es usar los dos.

---

## 5. Resumen y chuleta de comandos

En este vídeo hemos aprendido a cuidar la calidad de nuestro código:

1. **Ruff** es un **linter** (detecta problemas) y **formatter** (uniforma el
   estilo), todo en una sola herramienta muy rápida.
2. Se instala como **dependencia de desarrollo** con `uv add --dev ruff`.
3. Con `ruff check` revisamos el código y con `ruff format` lo formateamos.
4. Muchos problemas se pueden **arreglar automáticamente** con `--fix`.
5. Todo se configura en el `pyproject.toml`, y la extensión de VSCode lo integra en
   el editor.

### Chuleta de comandos

| Comando | Para qué sirve |
|---------|----------------|
| `uv add --dev ruff` | Instalar Ruff como dependencia de desarrollo. |
| `uv run ruff check` | Revisar el código en busca de problemas. |
| `uv run ruff check --fix` | Revisar **y** arreglar automáticamente lo que pueda. |
| `uv run ruff format` | Formatear el código con un estilo uniforme. |
| `uv run ruff check --watch` | Revisar en continuo, reaccionando a cada cambio. |
| `uv run ruff --version` | Comprobar la versión de Ruff instalada. |

> 📚 Para profundizar: la [documentación de Ruff](https://docs.astral.sh/ruff/) y su
> [lista completa de reglas](https://docs.astral.sh/ruff/rules/).

Con Ruff en nuestro flujo de trabajo, escribiremos código más limpio y profesional
desde el primer día.
