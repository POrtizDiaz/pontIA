#!/usr/bin/env bash

# ============================================================================
# SCRIPT DE COMPROBACIÓN DEL ENTORNO
# ============================================================================
# Verifica que el sistema cumple los requisitos necesarios para ejecutar
# los ejercicios de terminal de Linux.
# 
# Uso: bash check_environment.sh
# ============================================================================

# Modo estricto: falla si se usa una variable no definida
set -u

# Contador para registrar la cantidad de errores encontrados
errors=0

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

# Imprime un mensaje de éxito en color/formato
# Parámetro: $1 = mensaje a mostrar
ok() {
    printf '[OK] %s\n' "$1"
}

# Imprime un mensaje de advertencia (no bloquea la ejecución)
# Parámetro: $1 = mensaje a mostrar
warn() {
    printf '[AVISO] %s\n' "$1"
}

# Imprime un mensaje de error y incrementa el contador
# Parámetro: $1 = mensaje a mostrar
fail() {
    printf '[ERROR] %s\n' "$1" >&2
    errors=$((errors + 1))
}

# ============================================================================
# COMPROBACIÓN 1: SHELL BASH
# ============================================================================
# Verifica que Bash esté disponible en el sistema
if command -v bash >/dev/null 2>&1; then
    ok "Shell disponible: $(bash --version | head -n 1)"
else
    fail "Bash no está disponible"
fi

# ============================================================================
# COMPROBACIÓN 2: SISTEMA OPERATIVO
# ============================================================================
# Identifica el SO (Linux, macOS, etc.) y verifica compatibilidad
case "$(uname -s 2>/dev/null || true)" in
    Linux)
        # Verifica si es Linux en WSL (Windows Subsystem for Linux)
        if grep -qi microsoft /proc/version 2>/dev/null; then
            ok "Sistema compatible: Linux sobre WSL"
        else
            ok "Sistema compatible: Linux"
        fi
        ;;
    Darwin)
        # macOS es totalmente compatible
        ok "Sistema compatible: macOS"
        ;;
    *)
        # SO no reconocido, se recomienda usar WSL 2 o macOS
        warn "Sistema no reconocido; se recomienda WSL 2 o macOS"
        ;;
esac

# ============================================================================
# COMPROBACIÓN 3: PYTHON 3
# ============================================================================
# Verifica que Python 3 esté instalado (necesario para algunos scripts)
if command -v python3 >/dev/null 2>&1; then
    ok "Python 3 disponible: $(python3 --version 2>&1)"
else
    fail "Python 3 no está disponible"
fi

# ============================================================================
# COMPROBACIÓN 4: GIT
# ============================================================================
# Comprueba Git (opcional pero recomendado para futuras sesiones)
if command -v git >/dev/null 2>&1; then
    ok "Git disponible: $(git --version)"
else
    warn "Git no está disponible; no bloquea esta sesión, pero se usará más adelante"
fi

# ============================================================================
# COMPROBACIÓN 5: ESTRUCTURA DE DIRECTORIOS
# ============================================================================
# Verifica que el script se ejecuta desde la raíz del proyecto
# y que existen los archivos/directorios necesarios
missing_paths=""
for path in data/orders.csv logs/pipeline.log scripts/process.py config/pipeline.env; do
    if [ ! -e "$path" ]; then
        missing_paths="$missing_paths $path"
    fi
done

if [ -z "$missing_paths" ]; then
    ok "Directorio de trabajo válido"
else
    fail "Ejecuta el script desde la raíz del material. Faltan:$missing_paths"
fi

# ============================================================================
# RESULTADO FINAL
# ============================================================================
# Si no hay errores, el entorno está listo; si hay errores, lista cuántos
if [ "$errors" -eq 0 ]; then
    printf '\nEntorno preparado para la sesión.\n'
    exit 0
fi

printf '\nHay %s error(es) que debes corregir antes de la sesión.\n' "$errors" >&2
exit 1

