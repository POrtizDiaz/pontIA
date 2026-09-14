#!/usr/bin/env bash

# Proceso deliberadamente largo para practicar Ctrl+C, ps y kill.

set -u

on_interrupt() {
    printf '\nInterrupción recibida. Proceso detenido de forma segura.\n'
    exit 130
}

trap on_interrupt INT TERM

printf 'Proceso iniciado con PID %s. Pulsa Ctrl+C para detenerlo.\n' "$$"

counter=1
while true; do
    printf 'Esperando... iteración %s\n' "$counter"
    counter=$((counter + 1))
    sleep 2
done

