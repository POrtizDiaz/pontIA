#!/usr/bin/env python3
"""Procesa pedidos y genera un resumen por estado usando solo la librería estándar."""

from __future__ import annotations

import csv
import os
import sys
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path


REQUIRED_COLUMNS = {"order_id", "date", "status", "amount"}


def fail(message: str, exit_code: int = 1) -> "NoReturn":
    """Muestra un error por stderr y termina con un código distinto de cero."""
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(exit_code)


def main() -> int:
    data_path_value = os.environ.get("DATA_PATH")
    if not data_path_value:
        fail("falta la variable de entorno DATA_PATH")

    data_path = Path(data_path_value)
    output_dir = Path(os.environ.get("OUTPUT_DIR", "output"))
    output_path = output_dir / "summary.csv"

    if not data_path.is_file():
        fail(f"no existe el archivo: {data_path}")

    counts: Counter[str] = Counter()
    amounts: dict[str, Decimal] = {}
    processed = 0

    try:
        with data_path.open(newline="", encoding="utf-8") as source:
            reader = csv.DictReader(source)
            columns = set(reader.fieldnames or [])
            missing = REQUIRED_COLUMNS - columns
            if missing:
                fail(f"faltan columnas obligatorias: {', '.join(sorted(missing))}")

            for line_number, row in enumerate(reader, start=2):
                status = (row["status"] or "").strip().lower()
                if not status:
                    fail(f"estado vacío en la línea {line_number}")
                try:
                    amount = Decimal(row["amount"])
                except (InvalidOperation, TypeError):
                    fail(f"importe no válido en la línea {line_number}")

                counts[status] += 1
                amounts[status] = amounts.get(status, Decimal("0")) + amount
                processed += 1
    except OSError as exc:
        fail(f"no se pudo leer {data_path}: {exc}")

    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        with output_path.open("w", newline="", encoding="utf-8") as target:
            writer = csv.writer(target)
            writer.writerow(["status", "orders", "total_amount"])
            for status in sorted(counts):
                writer.writerow([status, counts[status], f"{amounts[status]:.2f}"])
    except OSError as exc:
        fail(f"no se pudo escribir {output_path}: {exc}")

    print(f"Procesados: {processed} registros")
    print(f"Salida: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

