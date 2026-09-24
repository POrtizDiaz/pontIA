# Ejercicio 2: Migrar un proyecto a una versión nueva de Python

## La situación

Es tu primer día en la empresa. Tu responsable te da la bienvenida y te suelta esto:

> "Mira, el análisis de ventas lo hizo un compañero que ya no está. Funciona, pero
> lo montó hace años con **Python 3.9** y librerías antiguas, y nadie se ha atrevido
> a tocarlo. Necesito dos cosas: **primero ponlo en marcha tal cual está** (que no
> se rompa nada), y después **modernízalo**: quiero que corra con **Python 3.12**,
> **pandas moderno (>=2.2)** y **numpy moderno (>=2.1)**, con los tests en verde."

El proyecto es la carpeta que te han entregado (este mismo directorio). Fíjate en
que no incluye la carpeta `.venv`: como buen proyecto, viaja solo con su
`pyproject.toml` y su `uv.lock`.

> **Requisitos:** `uv` instalado. No hace falta que tengas
> instalado ni Python 3.9 ni 3.12: de eso se encarga `uv` solito.

---

## Parte 1: Ponerlo en marcha (sin tocar nada)

Desde la carpeta del proyecto, reconstruye el entorno y comprueba que todo funciona
como le funcionaba al antiguo compañero.

**❓ Pregunta 1.** ¿Con qué versión de Python se ha ejecutado `main.py`? (El propio
programa la imprime.) Tú no has instalado esa versión a mano: ¿de dónde ha salido y
qué archivo del proyecto le ha dicho a `uv` cuál usar?

**❓ Pregunta 2.** ¿De dónde ha sacado `uv sync` las **versiones exactas** de cada
librería que ha instalado? ¿Qué habría pasado si el proyecto no incluyera ese
archivo?

---

## Parte 2: Actualizar las versiones

Toca actualizar pandas>=2.2 y numpy>=2.1. Empieza pidiéndoselo a `uv`:

```bash
uv add "pandas>=2.2" "numpy>=2.1"
```

No funciona.

**❓ Pregunta 3.** El error no habla de un conflicto entre dos librerías, sino entre
una librería y otra cosa. ¿Entre qué y qué exactamente es la incompatibilidad?

Con lo aprendido en los vídeos, seguramente pienses: "¡claro, hay que cambiar la
versión de Python del proyecto!". Adelante: **pinea Python 3.12** con el comando que
ya conoces y vuelve a lanzar el `uv add`.

Sigue fallando con el mismo error.

**❓ Pregunta 4.** Has cambiado la versión de Python del proyecto y `uv` sigue
diciendo que "the requested Python version (>=3.9)" no vale. **Hay dos sitios donde
un proyecto habla de su versión de Python** y solo has cambiado uno. ¿Cuál te
falta, en qué archivo está, y qué diferencia hay entre los dos? Corrígelo (este se
edita a mano) y vuelve a intentar el `uv add`. Esta vez sí.

**❓ Pregunta 5.** Abre el `pyproject.toml` y mira la lista `dependencies`. El
antiguo compañero tenía pineado `numpy>=1.21,<2`. ¿Qué ha pasado con ese pin al
hacer el `uv add`?

---

## Parte 3: Verificación final

Comprueba que hemos cumplido todos los pasos:

```bash
uv run pytest   # los tests siguen en verde
uv run main.py  # debe decir Python 3.12.x y un pandas moderno
```

Fíjate en la primera línea que imprime `main.py`: mismo código, pero ahora corre
con otro Python y otro pandas.

---