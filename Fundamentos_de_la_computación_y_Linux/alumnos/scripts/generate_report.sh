#!/usr/bin/env bash

# Orquesta la inspección del log y el procesamiento Python.

set -eu

log_path="${LOG_PATH:-logs/pipeline.log}"
output_dir="${OUTPUT_DIR:-output}"

if [ -z "${DATA_PATH:-}" ]; then
    printf 'ERROR: falta la variable de entorno DATA_PATH\n' >&2
    printf 'Ejemplo: export DATA_PATH="data/orders.csv"\n' >&2
    exit 1
fi

if [ ! -f "$log_path" ]; then
    printf 'ERROR: no existe el log: %s\n' "$log_path" >&2
    exit 1
fi

mkdir -p "$output_dir"

report_path="$output_dir/report.txt"
run_path="$output_dir/run.txt"
errors_path="$output_dir/errors.txt"

printf 'RESUMEN DE ERRORES\n' > "$report_path"
grep 'ERROR' "$log_path" | sort | uniq -c >> "$report_path" || true
printf '\nTOTAL\n' >> "$report_path"
grep -c 'ERROR' "$log_path" >> "$report_path" || true

if python3 scripts/process.py > "$run_path" 2> "$errors_path"; then
    printf '\nPROCESAMIENTO\n' >> "$report_path"
    cat "$run_path" >> "$report_path"
    printf 'Informe generado: %s\n' "$report_path"
else
    status=$?
    printf 'ERROR: el procesamiento Python ha fallado. Revisa %s\n' "$errors_path" >&2
    exit "$status"
fi

