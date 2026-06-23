"""
scripts/import_data.py
Importa o CSV Dataset/Nhanes_cvd_raw.csv para a tabela nhanes_cvd no Supabase.

Pre-requisitos:
  1. Criar a tabela no Supabase usando schema.sql
  2. Configurar SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY no arquivo .env

Uso:
  python scripts/import_data.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

import pandas as pd
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "Dataset" / "Nhanes_cvd_raw.csv"
BATCH_SIZE = 500
TABLE_NAME = "nhanes_cvd"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.nhanes_mapping import CSV_TO_DB, CVD_COLUMNS  # noqa: E402

load_dotenv(PROJECT_ROOT / ".env")


def _convert_cvd(value: Any) -> bool | None:
    """Converte codigos NHANES CVD para booleano nullable."""
    if pd.isna(value):
        return None

    code = float(value)
    if code == 1.0:
        return True
    if code == 2.0:
        return False
    if code == 9.0:
        return None

    raise ValueError(f"Valor cardiovascular inesperado: {value!r}")


def _to_json_value(value: Any) -> Any:
    """Normaliza escalares do Pandas/NumPy e ausentes para JSON/PostgREST."""
    if value is None or pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def load_and_clean() -> pd.DataFrame:
    """Le e prepara o CSV para upsert no Supabase."""
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV nao encontrado: {CSV_PATH}")

    print(f"Lendo CSV: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH, na_values=["NA", "N/A", ""])
    total_rows = len(df)

    missing_columns = sorted(set(CSV_TO_DB) - set(df.columns))
    if missing_columns:
        raise ValueError(
            "O CSV nao contem as colunas esperadas: "
            + ", ".join(missing_columns)
        )

    df = df.rename(columns=CSV_TO_DB)
    df = df[list(CSV_TO_DB.values())]

    for col in CVD_COLUMNS:
        if col in df.columns:
            df[col] = df[col].apply(_convert_cvd)

    df = df.astype(object).where(pd.notna(df), None)

    print(f"Total de linhas lidas do CSV: {total_rows:,}")
    return df


def dataframe_to_records(df: pd.DataFrame) -> list[dict[str, Any]]:
    """Converte DataFrame para registros JSON-safe."""
    records = df.to_dict(orient="records")
    return [
        {column: _to_json_value(value) for column, value in record.items()}
        for record in records
    ]


def upsert_batches(client: Any, records: list[dict[str, Any]], batch_size: int) -> int:
    """Envia registros em lotes usando seqn como chave de conflito."""
    total = len(records)
    sent = 0

    for start in range(0, total, batch_size):
        batch = records[start : start + batch_size]
        (
            client.table(TABLE_NAME)
            .upsert(batch, on_conflict="seqn")
            .execute()
        )
        sent += len(batch)
        pct = sent / total * 100 if total else 100
        print(f"Enviados {sent:>6,}/{total:,} registros ({pct:.1f}%)", end="\r")

    print()
    return sent


def get_supabase_credentials() -> tuple[str, str]:
    """Le credenciais de importacao do .env."""
    url = os.environ.get("SUPABASE_URL", "").strip()
    service_role_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()

    if not url or url.startswith("https://seu-projeto"):
        raise ValueError("Configure SUPABASE_URL no arquivo .env.")

    if not service_role_key or service_role_key == "sua-service-role-key-aqui":
        raise ValueError("Configure SUPABASE_SERVICE_ROLE_KEY no arquivo .env.")

    return url, service_role_key


def main() -> None:
    from supabase import create_client

    try:
        url, service_role_key = get_supabase_credentials()
        print(f"Conectando ao Supabase: {url}")
        client = create_client(url, service_role_key)

        df = load_and_clean()
        records = dataframe_to_records(df)

        print(f"Enviando lotes de ate {BATCH_SIZE} registros para '{TABLE_NAME}'...")
        sent = upsert_batches(client, records, BATCH_SIZE)

        print(f"Total de linhas enviadas ao Supabase: {sent:,}")
        print("Importacao concluida com sucesso.")
        print("Valide no Supabase com: SELECT COUNT(*) FROM nhanes_cvd;")
    except Exception as exc:
        print(f"ERRO na importacao: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
