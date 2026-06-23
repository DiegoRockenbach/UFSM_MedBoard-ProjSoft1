"""
app/database.py
Camada de acesso a dados: Supabase como fonte principal, com fallback CSV opcional.
"""

from __future__ import annotations

import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

try:
    from .nhanes_mapping import CSV_TO_DB, CVD_COLUMNS
except ImportError:
    from nhanes_mapping import CSV_TO_DB, CVD_COLUMNS

load_dotenv()

TABLE_NAME = "nhanes_cvd"
PAGE_SIZE = 1000
DATA_SOURCE_KEY = "medboard_data_source"


def _allow_csv_fallback() -> bool:
    return os.environ.get("ALLOW_CSV_FALLBACK", "").strip().lower() == "true"


def get_data_source(df: pd.DataFrame | None = None) -> str:
    if df is not None:
        source = df.attrs.get("data_source")
        if source:
            return source
    return st.session_state.get(DATA_SOURCE_KEY, "Fonte nao carregada")


def _convert_cvd(value) -> bool | None:
    """Normaliza flags cardiovasculares vindas do Supabase ou do CSV fallback."""
    if pd.isna(value):
        return None

    if value is True or str(value).lower() == "true":
        return True
    if value is False or str(value).lower() == "false":
        return False

    # Mantem compatibilidade apenas com o CSV de fallback: 1 = sim, 2 = nao.
    if value == 1 or value == 1.0 or str(value) in {"1", "1.0"}:
        return True
    if value == 2 or value == 2.0 or str(value) in {"2", "2.0"}:
        return False
    if value == 9 or value == 9.0 or str(value) in {"9", "9.0"}:
        return None

    return None


def _prepare(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza o DataFrame para o formato esperado por app/main.py."""
    if "created_at" in df.columns:
        df = df.drop(columns=["created_at"])

    if df.empty:
        return df

    for col in CVD_COLUMNS:
        if col in df.columns:
            df[col] = df[col].apply(_convert_cvd)

    skip = set(CVD_COLUMNS) | {"seqn"}
    for col in df.columns:
        if col not in skip:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "seqn" in df.columns:
        df["seqn"] = pd.to_numeric(df["seqn"], errors="coerce").astype("Int64")

    return df


def _load_csv() -> pd.DataFrame:
    """Carrega o CSV local apenas quando ALLOW_CSV_FALLBACK=true."""
    csv_path = os.path.join(
        os.path.dirname(__file__), "..", "Dataset", "Nhanes_cvd_raw.csv"
    )
    df = pd.read_csv(csv_path, na_values=["NA", "N/A", ""])
    df = df.rename(columns=CSV_TO_DB)
    return _prepare(df)


def _load_supabase() -> pd.DataFrame:
    """Carrega todos os registros do Supabase com paginacao por seqn."""
    from supabase import create_client

    url = os.environ.get("SUPABASE_URL", "").strip()
    anon_key = os.environ.get("SUPABASE_ANON_KEY", "").strip()

    if not url or url.startswith("https://seu-projeto") or not anon_key:
        raise ValueError(
            "SUPABASE_URL e SUPABASE_ANON_KEY nao configurados no arquivo .env."
        )

    client = create_client(url, anon_key)
    all_rows: list[dict] = []
    offset = 0

    while True:
        response = (
            client.table(TABLE_NAME)
            .select("*")
            .order("seqn")
            .range(offset, offset + PAGE_SIZE - 1)
            .execute()
        )

        rows = response.data or []
        if not rows:
            break

        all_rows.extend(rows)
        if len(rows) < PAGE_SIZE:
            break

        offset += PAGE_SIZE

    return _prepare(pd.DataFrame(all_rows))


@st.cache_data(ttl=3600, show_spinner=False)
def load_data() -> pd.DataFrame:
    """Carrega dados do Supabase; CSV somente com ALLOW_CSV_FALLBACK=true."""
    try:
        df = _load_supabase()
        df.attrs["data_source"] = "Supabase"
        st.session_state[DATA_SOURCE_KEY] = "Supabase"
        return df
    except Exception as exc:
        if _allow_csv_fallback():
            st.warning(
                f"Supabase indisponivel ({exc}). "
                "Carregando CSV local porque ALLOW_CSV_FALLBACK=true."
            )
            df = _load_csv()
            df.attrs["data_source"] = "CSV local (fallback)"
            st.session_state[DATA_SOURCE_KEY] = "CSV local (fallback)"
            return df

        st.session_state[DATA_SOURCE_KEY] = "Erro ao carregar Supabase"
        st.error(
            "Nao foi possivel carregar os dados do Supabase. "
            f"Detalhes: {exc} "
            "Configure SUPABASE_URL e SUPABASE_ANON_KEY no .env, "
            "ou use ALLOW_CSV_FALLBACK=true apenas em desenvolvimento."
        )
        st.stop()
