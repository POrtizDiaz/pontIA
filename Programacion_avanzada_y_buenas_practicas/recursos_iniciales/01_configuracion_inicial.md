# Configuración inicial: entorno de trabajo en Python

En esta primera sesión vamos a dejar listo nuestro entorno de trabajo. Antes de
escribir una sola línea de código, conviene tener un buen editor configurado y la
versión correcta de Python instalada. Una configuración cuidada al principio nos
ahorra muchísimos problemas más adelante.

---

## 1. El editor de código: VSCode

Vamos a usar **Visual Studio Code (VSCode)** como editor principal a lo largo del
curso. Es un editor gratuito, ligero y mantenido por Microsoft, y se ha convertido
en uno de los más utilizados del mundo, tanto por principiantes como por equipos
profesionales.

### ¿Por qué VSCode?

- **Es gratuito y multiplataforma.** Funciona igual en Windows, macOS y Linux, así
  que todos trabajaremos con la misma herramienta independientemente del sistema
  operativo.
- **Es ligero pero potente.** Arranca rápido y consume pocos recursos, pero gracias
  a su sistema de extensiones puede crecer hasta convertirse en un entorno de
  desarrollo muy completo.
- **Tiene un ecosistema de extensiones enorme.** Hay extensiones para casi
  cualquier lenguaje, framework o herramienta. Instalamos solo lo que necesitamos.
- **Integra terminal, control de versiones (Git) y depurador (debugger)** dentro de la misma
  ventana, sin tener que saltar entre programas.
- **Está muy bien documentado** y tiene una comunidad enorme, por lo que cualquier
  duda suele estar resuelta a un par de búsquedas de distancia.

### ¿Hay alternativas?

Sí, y es importante saberlo: **VSCode no es la única opción**. Si en algún momento
prefieres otro editor, puedes usarlo siendo consciente de que no será el que usemos en clase.

- La alternativa habitual es **PyCharm** (de JetBrains): un IDE específico para Python, muy potente y con
  muchas funcionalidades integradas "de fábrica". Tiene una versión *Community*
  gratuita y una *Professional* de pago.

> 💡 **En este curso usaremos VSCode** para que todos partamos de la misma base,
> pero lo que aprendamos sobre entornos, Python y buenas prácticas es válido sea
> cual sea el editor que elijas.

---

## 2. Configuración básica de VSCode

Una vez instalado VSCode desde su página oficial
([code.visualstudio.com](https://code.visualstudio.com)), conviene dejar listos
unos ajustes básicos:

1. **Instalar el intérprete de Python** (lo veremos en el siguiente vídeo) y asegurarnos de
   que VSCode lo detecta.
2. **Seleccionar el intérprete de Python** con el que vamos a trabajar:
   - Abre la *Command Palette* con `Ctrl + Shift + P` (en macOS, `Cmd + Shift + P`).
   - Escribe `Python: Select Interpreter` y elige la versión correcta.
3. **Activar el guardado automático** (opcional pero cómodo):
   - Menú `File > Auto Save`.
4. **Ajustes recomendados** (`Ctrl ,` para abrir la configuración):
   - Mostrar los números de línea.
   - Activar el formateo al guardar (*Format On Save*).
   - Definir la tabulación a **4 espacios**, que es la convención en Python.
5. **Conocer la terminal integrada**: ábrela desde el menú
   `Terminal > New Terminal`. La usaremos constantemente para ejecutar scripts,
   instalar paquetes y gestionar entornos.

> 💡 Muchos de estos ajustes se guardan en un archivo `settings.json`. No es
> necesario tocarlo a mano al principio: la interfaz gráfica de configuración es
> más que suficiente.

---

## 3. Extensiones imprescindibles

Las extensiones son lo que convierte a VSCode en un entorno de desarrollo a medida.
Estas son las más importantes para trabajar con Python:

| Extensión | Para qué sirve |
|-----------|----------------|
| **Python** (Microsoft) | La extensión fundamental. Añade soporte de Python: ejecución, depuración, selección de intérprete, etc. |
| **Pylance** | Motor de análisis de código: comprobación de tipos y navegación por el código. Se instala junto con la anterior. |
| **Jupyter** | Permite ejecutar *notebooks* (`.ipynb`) directamente dentro de VSCode. |
| **Ruff** o **Black Formatter** | Formateo y *linting* del código para mantenerlo limpio y consistente. |
| **Python Debugger** (Microsoft) | Añade el depurador de Python (basado en `debugpy`). Permite poner *breakpoints*, ejecutar paso a paso e inspeccionar variables desde la GUI. Se instala junto con la extensión Python. |
| **Python Test Explorer** | Integra la ejecución de tests (`unittest` y `pytest`) en VSCode: ejecuta y depura tests con un clic desde el panel lateral, sin tocar la terminal. |

> 💡 Para instalar una extensión: abre el panel de extensiones con
> `Ctrl + Shift + X`, busca el nombre y pulsa *Install*.

Empezaremos solo con la extensión **Python** (que arrastra a Pylance) y a partir de
ahí iremos añadiendo el resto según las vayamos necesitando.

---

## 4. La versión de Python

En este curso vamos a trabajar con **Python 3.12.3**.

### ¿Por qué esta versión?

- Es una versión **moderna, estable y ampliamente soportada**. Aunque existen
  versiones más recientes, **3.12.3 está perfectamente bien** para todo lo que
  vamos a hacer.
- Entre versiones cercanas de Python (por ejemplo, de la 3.11 a la 3.12, o de la
  3.12 a la 3.13) **los cambios no afectan a lo que aprenderemos**: la sintaxis y el
  comportamiento del lenguaje son prácticamente idénticos para nuestro uso.
- Lo importante es **fijar una versión común** para que todos tengamos exactamente el
  mismo comportamiento y evitemos el clásico "en mi máquina funciona".

### Lo que sí debemos evitar

Lo que **no** podemos hacer es usar una versión **antigua** del tipo **Python 2.x**
(o incluso versiones muy tempranas de la rama 3). Python 2 tiene un comportamiento
**muy diferente** en cosas tan básicas como:

- La función `print`, que en Python 2 era una sentencia (`print "hola"`) y en
  Python 3 es una función (`print("hola")`).
- El manejo de cadenas de texto y la codificación (Unicode).
- La división de enteros, que se comporta de forma distinta.

Además, **Python 2 está oficialmente descontinuado** desde 2020: ya no recibe
actualizaciones ni parches de seguridad. Por eso, partir de Python 3.12.3 es la
opción correcta.
