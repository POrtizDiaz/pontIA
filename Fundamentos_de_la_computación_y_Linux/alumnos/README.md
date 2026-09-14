# Linux y terminal — materiales de demostración

<img src="./img/sergio_portrait_square.png" alt="Sergio Benito" align="right" width="100">

- **Autor:** Sergio Benito Martín
- **Contacto:** pontia@sergiobenito.com
- **Última actualización:** 24/08/2026

Este paquete acompaña a la presentación `Linux_y_terminal_PontIA_2026.pptx`.
Los ejemplos están preparados para ejecutarse desde la raíz de esta carpeta.

## Estructura

```text
linux-terminal/
├── check_environment.sh
├── config/
│   └── pipeline.env
├── data/
│   └── orders.csv
├── logs/
│   └── pipeline.log
├── output/
├── scripts/
│   ├── generate_report.sh
│   ├── process.py
│   └── wait_demo.sh
└── .env.example
```

## 1. Comprobar el entorno

```bash
bash check_environment.sh
```

El script comprueba Bash, Python 3, Git y la estructura del material. Git no se
utiliza en esta asignatura, pero se comprueba porque será necesario más adelante
en el máster.

## 2. Provocar y observar un error

`process.py` necesita la variable de entorno `DATA_PATH`. Si no existe, escribe
el error en `stderr` y termina con código 1:

```bash
mkdir -p output
python3 scripts/process.py > output/run.txt 2> output/errors.txt
echo $?
cat output/errors.txt
```

## 3. Ejecutar correctamente el procesamiento

```bash
export DATA_PATH="data/orders.csv"
python3 scripts/process.py
```

Resultado esperado:

```text
Procesados: 842 registros
Salida: output/summary.csv
```

## 4. Ejecutar el informe Bash

Invocando Bash directamente:

```bash
bash scripts/generate_report.sh
```

O dando permiso de ejecución al archivo:

```bash
chmod +x scripts/generate_report.sh
./scripts/generate_report.sh
```

El script crea `output/report.txt`, ejecuta el procesamiento Python y conserva
la salida normal y los errores en archivos separados.

## 5. Demostrar Ctrl+C y procesos

```bash
bash scripts/wait_demo.sh
```

Detén el proceso con `Ctrl+C`. El script captura la interrupción y termina de
forma limpia con código 130.

## Reiniciar la demostración

Los archivos originales de `data/`, `logs/` y `config/` no se modifican. Para
vaciar únicamente los resultados generados:

```bash
rm -f output/*.txt output/*.csv
```

