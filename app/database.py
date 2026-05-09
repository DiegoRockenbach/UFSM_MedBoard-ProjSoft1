"""
app/database.py
Camada de acesso a dados: Supabase (primário) com fallback para CSV local.
"""

import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Mapeamento de colunas CSV → banco de dados ────────────────────────────────
CSV_TO_DB: dict[str, str] = {
    "SEQN": "seqn",
    "Protein": "protein",
    "Carbohydrates": "carbohydrates",
    "Sugars": "sugars",
    "Fiber": "fiber",
    "Saturated_Fat": "saturated_fat",
    "Monounsaturated_Fat": "monounsaturated_fat",
    "Polyunsaturated_Fat": "polyunsaturated_fat",
    "Cholesterol": "cholesterol",
    "Beta_Carotene": "beta_carotene",
    "Cryptoxanthin": "cryptoxanthin",
    "Lutein_Zeaxanthin": "lutein_zeaxanthin",
    "Thiamin": "thiamin",
    "Riboflavin": "riboflavin",
    "Niacin": "niacin",
    "Vitamin_B6": "vitamin_b6",
    "Folic_Acid": "folic_acid",
    "Food_Folate": "food_folate",
    "Vitamin_B12": "vitamin_b12",
    "Vitamin_C": "vitamin_c",
    "Vitamin_D": "vitamin_d",
    "Vitamin_E": "vitamin_e",
    "Vitamin_K": "vitamin_k",
    "Iron": "iron",
    "Choline": "choline",
    "Calcium": "calcium",
    "Phosphorus": "phosphorus",
    "Magnesium": "magnesium",
    "Zinc": "zinc",
    "Copper": "copper",
    "Sodium": "sodium",
    "Potassium": "potassium",
    "Selenium": "selenium",
    "Theobromine": "theobromine",
    "Moisture": "moisture",
    "Congestive": "congestive",
    "Coronary": "coronary",
    "Heart_attack": "heart_attack",
    "Stroke": "stroke",
    "Angina": "angina",
    "Age": "age",
    "BMI": "bmi",
    "Waist_circ": "waist_circ",
    "Systolic_BP": "systolic_bp",
    "Diastolic_BP": "diastolic_bp",
    "Total_Colesterol": "total_cholesterol",  # corrige o typo do CSV original
    "C_Reactive": "c_reactive",
}

CVD_COLUMNS = ["congestive", "coronary", "heart_attack", "stroke", "angina"]


# ── Preparação dos dados ──────────────────────────────────────────────────────

def _convert_cvd(val) -> bool:
    """Converte flags CVD: 2/True/'2' → True, qualquer outro → False."""
    return val is True or val == 2 or val == 2.0 or str(val) == "2"


def _prepare(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza tipos e valores ausentes após qualquer fonte de carga."""
    # Flags cardiovasculares → bool
    for col in CVD_COLUMNS:
        if col in df.columns:
            df[col] = df[col].apply(_convert_cvd)

    # Colunas numéricas → float/int
    skip = set(CVD_COLUMNS) | {"seqn"}
    for col in df.columns:
        if col not in skip:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


# ── Fontes de dados ───────────────────────────────────────────────────────────

def _load_csv() -> pd.DataFrame:
    """Carrega diretamente do arquivo CSV (fallback sem Supabase)."""
    csv_path = os.path.join(
        os.path.dirname(__file__), "..", "Dataset", "Nhanes_cvd_raw.csv"
    )
    df = pd.read_csv(csv_path, na_values=["NA", "N/A", ""])
    df = df.rename(columns=CSV_TO_DB)
    return _prepare(df)


def _load_supabase() -> pd.DataFrame:
    """Carrega todos os registros do Supabase usando paginação."""
    from supabase import create_client  # import tardio

    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_KEY", "").strip()

    if not url or not key:
        raise ValueError(
            "SUPABASE_URL e SUPABASE_KEY não configurados. "
            "Copie .env.example para .env e preencha as credenciais."
        )

    client = create_client(url, key)
    all_rows: list[dict] = []
    page_size = 1000
    offset = 0

    while True:
        resp = (
            client.table("nhanes_cvd")
            .select("*")
            .range(offset, offset + page_size - 1)
            .execute()
        )
        if not resp.data:
            break
        all_rows.extend(resp.data)
        if len(resp.data) < page_size:
            break
        offset += page_size

    return _prepare(pd.DataFrame(all_rows))


# ── Ponto de entrada principal (com cache) ────────────────────────────────────

@st.cache_data(ttl=3600, show_spinner=False)
def load_data() -> pd.DataFrame:
    """
    Carrega os dados de saúde NHANES.
    Usa Supabase quando as variáveis de ambiente estão configuradas;
    caso contrário, carrega do CSV local automaticamente.
    """
    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_KEY", "").strip()

    if url and key and not url.startswith("https://seu-projeto"):
        try:
            return _load_supabase()
        except Exception as exc:
            st.warning(
                f"⚠️ Supabase indisponível ({exc}). "
                "Carregando dados do arquivo CSV local..."
            )

    return _load_csv()
