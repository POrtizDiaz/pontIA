# Ejercicio 1: Anatomía de un conflicto de dependencias

En los vídeos hemos aprendido a instalar Python con `uv` y a crear proyectos con
`pyproject.toml`. En este ejercicio vas a montar un proyecto desde cero y, por el
camino, vamos a provocar un conflicto de dependencias a propósito para aprender a
leer y resolver el error.

> **Requisitos previos:** tener `uv` instalado (`uv --version` debe funcionar).
> Todos los comandos se ejecutan en la terminal, desde la carpeta del proyecto.

---

## Parte 1: Crear el proyecto

Crea un proyecto nuevo llamado `analisis-temperaturas`, pineado a Python 3.12.

Abre la carpeta en VSCode y explora los archivos que se han generado.

**❓ Pregunta 1.**  ¿En cuál de ellos está pineada la versión de Python?

---

## Parte 2: Añadir dependencias

Nuestro proyecto va a analizar datos con **pandas**, y usaremos **pytest** para los
tests. Añade la versión 2.2.2 de pandas y la versión más actual de pytest.

Abre el `pyproject.toml` y observa cómo ha quedado.

**❓ Pregunta 2.** ¿Por qué pandas y pytest han ido a secciones distintas del
`pyproject.toml`?

---

## Parte 3: Escribir el código

Sustituye el contenido de `main.py` por esto:

```python
import pandas as pd

def temperatura_media_por_ciudad(df):
    return df.groupby("ciudad")["temperatura"].mean().round(1)

def main():
    df = pd.DataFrame({
        "ciudad": ["Madrid", "Madrid", "Sevilla", "Sevilla", "Bilbao", "Bilbao"],
        "temperatura": [28.0, 32.0, 36.0, 40.0, 21.0, 24.0],
    })
    print(f"pandas {pd.__version__}")
    print("Temperatura media por ciudad:")
    print(temperatura_media_por_ciudad(df).to_string())

if __name__ == "__main__":
    main()
```

Y crea un archivo `test_main.py` con este contenido:

```python
import pandas as pd
from main import temperatura_media_por_ciudad

def test_temperatura_media():
    df = pd.DataFrame({
        "ciudad": ["Madrid", "Madrid", "Sevilla"],
        "temperatura": [28.0, 32.0, 40.0],
    })
    resultado = temperatura_media_por_ciudad(df)
    assert resultado["Madrid"] == 30.0
    assert resultado["Sevilla"] == 40.0
```

Comprueba que todo funciona:

```bash
uv run main.py
uv run pytest
```

Deberías ver la tabla de temperaturas y 1 test en verde. Si es así, el proyecto
está sano. Ahora vamos a estropearlo.

---

## Parte 4: El conflicto

Por alguna razón, necesitamos instalar numpy ahora en nuestro proyecto. Elegimos una versión en concreto que sabemos que funciona, por ejemplo la 1.21.6. La instalamos:

```bash
uv add "numpy==1.21.6"
```

**No va a funcionar.** Lee el mensaje de error y responde:

**❓ Pregunta 3.** Según el mensaje de error, ¿qué librería exige `numpy>=1.26.0` y
por eso es incompatible con tu petición?

**❓ Pregunta 4.** Después del error, ¿se ha roto algo en tu proyecto? Compruébalo:
mira si el `pyproject.toml` ha cambiado y vuelve a ejecutar `uv run pytest`. ¿Qué
ha pasado y por qué crees que `uv` funciona así?

**❓ Pregunta 5.** Se te ocurren al menos dos formas distintas de salir de este
conflicto? (No hace falta ejecutarlas todavía, solo pensarlas.)

---

## Parte 5: Resolver el conflicto

De las opciones posibles, vamos por la más razonable: no necesitamos exactamente
numpy 1.21.6; nos vale cualquier numpy moderno compatible
con nuestro pandas. Pídelo como rango en lugar de versión exacta:

```bash
uv add "numpy>=1.26"
```

Esta vez sí funciona. Comprueba con `uv tree` que numpy aparece ahora como
dependencia directa del proyecto, y mira cómo ha quedado `dependencies` en el
`pyproject.toml`.

**❓ Pregunta 6.** ¿Qué versión concreta de numpy se ha instalado? ¿Dónde puedes
consultar la versión exacta instalada: en el `pyproject.toml` o en el `uv.lock`?

---

## Parte 6: Asegurando la reproducibilidad

Vamos a simular que se nos ha borrado el entorno. Borra la
carpeta del entorno virtual entera:

```bash
# macOS / Linux
rm -rf .venv

# Windows (PowerShell)
Remove-Item -Recurse -Force .venv
```

Y ahora recupéralo con un solo comando:

```bash
uv sync
uv run pytest
```

Si el test vuelve a estar en verde, acabamos de comprobar que un proyecto con `uv.lock` es 100% reproducible.

**❓ Pregunta 7.** De todos los archivos y carpetas del proyecto
(`pyproject.toml`, `uv.lock`, `.venv/`, `.python-version`, código), ¿cuáles
subirías a Git y cuáles no?
