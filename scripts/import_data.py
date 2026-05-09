"""
scripts/import_data.py
Importa o CSV Nhanes_cvd_raw.csv para a tabela nhanes_cvd no Supabase.

Pré-requisitos:
  1. Criar a tabela no Supabase usando schema.sql
  2. Configurar as variáveis de ambiente em .env

Uso:
  python scripts/import_data.py
"""

import os
import sys
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "Dataset", "Nhanes_cvd_raw.csv")

COLUMN_RENAME: dict[str, str] = {
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
    "Total_Colesterol": "total_cholesterol",
    "C_Reactive": "c_reactive",
}

CVD_COLS = ["congestive", "coronary", "heart_attack", "stroke", "angina"]


def load_and_clean() -> pd.DataFrame:
    """Lê e prepara o CSV para inserção no Supabase."""
    print(f"Lendo: {os.path.abspath(CSV_PATH)}")
    df = pd.read_csv(CSV_PATH, na_values=["NA", "N/A", ""])
    df = df.rename(columns=COLUMN_RENAME)
    print(f"  → {len(df):,} linhas · {len(df.columns)} colunas")

    # Converte flags CVD: 2 → True, NaN → False
    for col in CVD_COLS:
        if col in df.columns:
            df[col] = (df[col] == 2).astype(bool)

    # Substitui NaN por None (serialização JSON → NULL no Postgres)
    df = df.where(pd.notna(df), other=None)

    return df


def insert_batches(client, records: list[dict], batch_size: int = 500) -> int:
    """Insere registros em lotes; retorna total inserido."""
    total = len(records)
    inserted = 0
    for i in range(0, total, batch_size):
        batch = records[i : i + batch_size]
        client.table("nhanes_cvd").insert(batch).execute()
        inserted += len(batch)
        pct = inserted / total * 100
        print(f"  ✓ {inserted:>6,}/{total:,}  ({pct:.1f}%)…", end="\r")
    print()
    return inserted


def main() -> None:
    from supabase import create_client

    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_KEY", "").strip()

    if not url or key == "" or url.startswith("https://seu-projeto"):
        print(
            "\nERRO: Configure as variáveis SUPABASE_URL e SUPABASE_KEY no arquivo .env\n"
            "      Copie .env.example para .env e preencha com suas credenciais do Supabase."
        )
        sys.exit(1)

    print(f"\nConectando ao Supabase: {url}")
    client = create_client(url, key)

    df = load_and_clean()
    records = df.to_dict(orient="records")

    print(f"\nInserindo {len(records):,} registros na tabela 'nhanes_cvd'…")
    n = insert_batches(client, records)

    print(f"\n✅ Importação concluída: {n:,} registros inseridos com sucesso.")


if __name__ == "__main__":
    main()
