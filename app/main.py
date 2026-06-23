"""
app/main.py
MedBoard – Dashboard de Saúde NHANES
Projeto de Software 1 · UFSM

Execução:
    streamlit run app/main.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from database import get_data_source, load_data

# ── Configuração da página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="MedBoard – Dashboard de Saúde",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "MedBoard · Projeto de Software 1 · UFSM"},
)

# ── CSS personalizado ─────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Fundo principal */
    .main { background-color: #F8FAFC; }

    /* Cards de métricas */
    [data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }

    /* Barra de abas */
    [data-testid="stTabs"] {
        margin-top: -3rem !important;
        margin-bottom: 0.5rem !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: linear-gradient(90deg, rgba(199, 135, 255, 0.1) 0%, rgba(247, 54, 112, 0.1) 100%);
        padding: 10px 8px;
        border-radius: 12px;
        margin-bottom: 1.5rem !important;
        border-bottom: 1px solid #D1D5DB;
        padding-bottom: 1rem !important;
        display: flex !important;
        width: 100% !important;
    }
    .stTabs [data-baseweb="tab"],
    .stTabs [data-baseweb="tab"] [data-testid="stBaseButton-primary"],
    .stTabs [data-baseweb="tab"] button {
        transition: none !important;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 12px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.9rem;
        background-color: white !important;
        border: 1px solid rgba(219, 221, 225, 0.5) !important;
        color: #000000 !important;
        transition: transform 0.2s ease !important;
        flex: 1 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        transform: scale(1.04) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
    }
    .stTabs [aria-selected="true"] [data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, #FA3939 0%, #F73670 100%) !important;
        border-color: #FA3939 !important;
        color: white !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(250, 57, 57, 0.3) !important;
        border-bottom: 4px solid #FA3939 !important;
    }

    /* Indicador deslizante da aba ativa */
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #FA3939 !important;
        height: 3px !important;
        border-radius: 2px !important;
    }

    /* Título principal */
    h1 { color: #1E3A5F !important; font-size: 1.9rem !important; }
    h2 { color: #1E40AF !important; }
    h3 { color: #374151 !important; }

    /* Rodapé Streamlit oculto */
    footer { visibility: hidden; }

    /* Reduz espaço em branco no topo */
    .main .block-container { padding-top: 1rem !important; }

    /* Só afeta blocos com 6+ colunas = rows de badges (7 colunas) */
    [data-testid="stHorizontalBlock"]:has([data-testid="stColumn"]:nth-child(6)) {
        gap: 6px !important;
        margin-bottom: -10px !important;
    }

    [data-testid="stHorizontalBlock"]:has([data-testid="stColumn"]:nth-child(6))
    [data-testid="stButton"] button {
        border-radius: 3px !important;
        height: auto !important;
        min-height: 34px !important;
        padding: 4px 10px !important;
        font-size: 0.78rem !important;
        line-height: 1.3 !important;
        white-space: normal !important;
        overflow: hidden;
        text-overflow: unset;
        word-break: break-word;
    }

    /* Badge ativa */
    [data-testid="stHorizontalBlock"]:has([data-testid="stColumn"]:nth-child(6))
    [data-testid="stBaseButton-primary"] {
        background-color: #FA3939 !important;
        border-color: #FA3939 !important;
        color: white !important;
    }
    [data-testid="stHorizontalBlock"]:has([data-testid="stColumn"]:nth-child(6))
    [data-testid="stBaseButton-primary"]:hover {
        background-color: #fb5c5c !important;
        border-color: #fb5c5c !important;
    }

    /* Badge pinada (disabled) — mesmo visual da ativa, sem efeito de desabilitado */
    [data-testid="stHorizontalBlock"]:has([data-testid="stColumn"]:nth-child(6))
    [data-testid="stBaseButton-primary"]:disabled {
        background-color: #FA3939 !important;
        border-color: #FA3939 !important;
        color: white !important;
        opacity: 1 !important;
        cursor: not-allowed !important;
    }

    /* Sliders — trilha e thumb */
    [data-testid="stSidebar"] [data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stSliderThumb"] {
        background-color: #FA3939 !important;
    }
    [data-testid="stSidebar"] [data-testid="stSlider"] [data-baseweb="slider"] div[role="progressbar"] {
        background-color: #FA3939 !important;
    }

    /* Badge inativa — cinza claro */
    [data-testid="stHorizontalBlock"]:has([data-testid="stColumn"]:nth-child(6))
    [data-testid="baseButton-secondary"] {
        background-color: #EDF2F7 !important;
        border-color: #CBD5E1 !important;
        color: #4A5568 !important;
    }
    [data-testid="stHorizontalBlock"]:has([data-testid="stColumn"]:nth-child(6))
    [data-testid="baseButton-secondary"]:hover {
        background-color: #E2E8F0 !important;
    }


    /* Botões de navegação de página */
    [data-testid="stHorizontalBlock"]:has([data-testid="stColumn"]:nth-child(5)):not(:has([data-testid="stColumn"]:nth-child(6)))
    [data-testid="stBaseButton-secondary"] {
        height: 48px !important;
        min-height: 48px !important;
        font-size: 1.25rem !important;
        padding: 1.2rem !important;
    }

    /* Botão Exportar CSV */
    [data-testid="stDownloadButton"] [data-testid="stBaseButton-primary"] {
        background-color: #FA3939 !important;
        border-color: #FA3939 !important;
    }
    [data-testid="stDownloadButton"] [data-testid="stBaseButton-primary"]:hover {
        background-color: #fb5c5c !important;
        border-color: #fb5c5c !important;
    }

    /* Links dos autores na sidebar */
    [data-testid="stSidebar"] small a {
        color: #6B7280 !important;
        text-decoration: none !important;
        transition: color 0.15s;
    }
    [data-testid="stSidebar"] small a:hover {
        color: #9CA3AF !important;
    }

    /* Links dos autores no rodapé */
    .main small a,
    [data-testid="stMarkdownContainer"] small a {
        color: #6B7280 !important;
        text-decoration: none !important;
        transition: color 0.15s;
    }
    .main small a:hover,
    [data-testid="stMarkdownContainer"] small a:hover {
        color: #9CA3AF !important;
    }

    /* Caixa de informação customizada */
    .medboard-info {
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        font-size: 0.88rem;
        color: #1E3A5F;
        margin: 6px 0 14px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Constantes ────────────────────────────────────────────────────────────────
CVD_CONDITIONS: dict[str, str] = {
    "congestive":   "Insuficiência Cardíaca",
    "coronary":     "Doença Arterial Coronariana",
    "heart_attack": "Infarto do Miocárdio",
    "stroke":       "AVC",
    "angina":       "Angina",
}

NUTRIENTS_MACRO    = ["protein", "carbohydrates", "sugars", "fiber",
                      "saturated_fat", "monounsaturated_fat", "polyunsaturated_fat", "cholesterol"]
NUTRIENTS_VITAMINS = ["vitamin_c", "vitamin_d", "vitamin_e", "vitamin_k",
                      "vitamin_b6", "vitamin_b12", "thiamin", "riboflavin",
                      "niacin", "folic_acid", "food_folate", "beta_carotene",
                      "cryptoxanthin", "lutein_zeaxanthin"]
NUTRIENTS_MINERALS = ["calcium", "iron", "magnesium", "zinc", "sodium",
                      "potassium", "phosphorus", "copper", "selenium", "choline"]

LABELS: dict[str, str] = {
    "protein":             "Proteína (g)",
    "carbohydrates":       "Carboidratos (g)",
    "sugars":              "Açúcares (g)",
    "fiber":               "Fibra (g)",
    "saturated_fat":       "Gordura Saturada (g)",
    "monounsaturated_fat": "Gordura Monoinsaturada (g)",
    "polyunsaturated_fat": "Gordura Poliinsaturada (g)",
    "cholesterol":         "Colesterol Dietético (mg)",
    "vitamin_c":           "Vitamina C (mg)",
    "vitamin_d":           "Vitamina D (mcg)",
    "vitamin_e":           "Vitamina E (mg)",
    "vitamin_k":           "Vitamina K (mcg)",
    "vitamin_b6":          "Vitamina B6 (mg)",
    "vitamin_b12":         "Vitamina B12 (mcg)",
    "thiamin":             "Tiamina (mg)",
    "riboflavin":          "Riboflavina (mg)",
    "niacin":              "Niacina (mg)",
    "folic_acid":          "Ácido Fólico (mcg)",
    "food_folate":         "Folato Alimentar (mcg)",
    "beta_carotene":       "Beta-Caroteno (mcg)",
    "cryptoxanthin":       "Criptoxantina (mcg)",
    "lutein_zeaxanthin":   "Luteína + Zeaxantina (mcg)",
    "calcium":             "Cálcio (mg)",
    "iron":                "Ferro (mg)",
    "magnesium":           "Magnésio (mg)",
    "zinc":                "Zinco (mg)",
    "sodium":              "Sódio (mg)",
    "potassium":           "Potássio (mg)",
    "phosphorus":          "Fósforo (mg)",
    "copper":              "Cobre (mg)",
    "selenium":            "Selênio (mcg)",
    "choline":             "Colina (mg)",
    "age":                 "Idade (anos)",
    "bmi":                 "IMC (kg/m²)",
    "waist_circ":          "Circ. Abdominal (cm)",
    "systolic_bp":         "PA Sistólica (mmHg)",
    "diastolic_bp":        "PA Diastólica (mmHg)",
    "total_cholesterol":   "Colesterol Total (mg/dL)",
    "c_reactive":          "Proteína C-Reativa (mg/L)",
}

TPLT   = "plotly_white"
C_BLUE = "#1E40AF"
C_GRN  = "#10B981"
C_RED  = "#DC2626"
C_AMB  = "#F59E0B"
C_SEQ  = [C_BLUE, C_GRN, C_AMB, C_RED, "#8B5CF6", "#EC4899", "#14B8A6"]

# ── Valores de referência clínicos / IDR ─────────────────────────────────────
# ref_min: abaixo disto é deficiente (None = sem limite inferior preocupante)
# ref_max: acima disto é elevado    (None = sem limite superior preocupante)
REFERENCE_VALUES: dict[str, dict] = {
    # ── Marcadores Clínicos ───────────────────────────────────────────────────
    "total_cholesterol": {
        "ref_min": None, "ref_max": 200.0,
        "tipo": "Clínico", "fonte": "AHA/ACC 2019",
        "msg_baixo": None,
        "msg_alto": (
            "Colesterol total elevado é o principal fator de risco para doença arterial coronariana "
            "e AVC. Valores entre 200–239 mg/dL são considerados limítrofes; acima de 240 mg/dL "
            "indicam hipercolesterolemia. O excesso de LDL deposita-se nas paredes das artérias "
            "(aterosclerose), reduzindo o fluxo sanguíneo e aumentando o risco de infarto."
        ),
    },
    "systolic_bp": {
        "ref_min": None, "ref_max": 120.0,
        "tipo": "Clínico", "fonte": "AHA/ACC 2017",
        "msg_baixo": (
            "Pressão sistólica abaixo de 90 mmHg caracteriza hipotensão, podendo causar tontura, "
            "desmaio e insuficiência de perfusão em órgãos vitais. Pode indicar desidratação, "
            "insuficiência cardíaca ou reação anafilática."
        ),
        "msg_alto": (
            "Hipertensão sistólica (≥130 mmHg) é o principal fator de risco modificável para "
            "doenças cardiovasculares. A pressão cronicamente elevada danifica as paredes "
            "das artérias, sobrecarrega o coração e aumenta o risco de infarto, AVC e "
            "insuficiência renal. Valores ≥180 mmHg configuram crise hipertensiva."
        ),
    },
    "diastolic_bp": {
        "ref_min": None, "ref_max": 80.0,
        "tipo": "Clínico", "fonte": "AHA/ACC 2017",
        "msg_baixo": (
            "Pressão diastólica muito baixa (< 60 mmHg) pode indicar desidratação grave, "
            "choque séptico ou doença cardíaca avançada. Em idosos, a hipertensão sistólica "
            "isolada (sistólica alta + diastólica baixa) também é preocupante."
        ),
        "msg_alto": (
            "Pressão diastólica elevada (≥80 mmHg) contribui para hipertrofia ventricular "
            "esquerda e aumenta o risco de doença arterial coronariana. Em pacientes mais "
            "jovens, frequentemente causada por aterosclerose precoce ou doença renal crônica."
        ),
    },
    "c_reactive": {
        "ref_min": None, "ref_max": 1.0,
        "tipo": "Clínico", "fonte": "AHA/CDC 2003",
        "msg_baixo": None,
        "msg_alto": (
            "A Proteína C-Reativa (PCR) é marcador de inflamação sistêmica. Valores entre "
            "1–3 mg/L indicam risco cardiovascular moderado; acima de 3 mg/L representam alto risco. "
            "PCR elevada está associada a aterosclerose, síndrome metabólica, diabetes tipo 2 "
            "e maior mortalidade cardiovascular. Inflamação crônica de baixo grau acelera "
            "a progressão de placas arteriais."
        ),
    },
    "bmi": {
        "ref_min": 18.5, "ref_max": 24.9,
        "tipo": "Clínico", "fonte": "WHO 2000",
        "msg_baixo": (
            "IMC abaixo de 18,5 kg/m² caracteriza baixo peso, associado a desnutrição, "
            "deficiências vitamínicas e minerais, osteoporose, anemia e imunossupressão. "
            "Pode indicar transtorno alimentar, câncer ou doença crônica grave."
        ),
        "msg_alto": (
            "IMC acima de 24,9 indica sobrepeso; acima de 30, obesidade. O excesso de peso "
            "está associado a hipertensão, diabetes tipo 2, apneia do sono, doença cardiovascular "
            "e determinados cânceres. Obesidade mórbida (IMC ≥40) reduz significativamente "
            "a expectativa de vida."
        ),
    },
    "waist_circ": {
        "ref_min": None, "ref_max": 94.0,
        "tipo": "Clínico", "fonte": "IDF 2006",
        "msg_baixo": None,
        "msg_alto": (
            "Circunferência abdominal elevada indica obesidade central (gordura visceral), "
            "independentemente do IMC. A gordura visceral libera adipocitocinas inflamatórias, "
            "aumentando o risco de síndrome metabólica, diabetes tipo 2, doença cardiovascular "
            "e hipertensão. Limites de risco: >94 cm em homens, >80 cm em mulheres (IDF)."
        ),
    },
    # ── Macronutrientes ───────────────────────────────────────────────────────
    "protein": {
        "ref_min": 50.0, "ref_max": 175.0,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 2005",
        "msg_baixo": (
            "Ingestão insuficiente de proteínas leva à sarcopenia (perda de massa muscular), "
            "comprometimento imunológico, cicatrização lenta e edema (kwashiorkor). Em idosos, "
            "a deficiência proteica acelera a perda óssea e muscular, aumentando o risco "
            "de quedas e fraturas."
        ),
        "msg_alto": (
            "Ingestão muito elevada (>2,5 g/kg/dia por período prolongado) pode sobrecarregar "
            "os rins em pessoas com doença renal preexistente. Dietas hiperproteicas ricas "
            "em carne vermelha e gordura saturada também aumentam o risco cardiovascular."
        ),
    },
    "carbohydrates": {
        "ref_min": 130.0, "ref_max": 325.0,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 2005",
        "msg_baixo": (
            "Ingestão abaixo de 130 g/dia pode causar hipoglicemia, fadiga, dificuldade de "
            "concentração e cetose. O cérebro depende quase exclusivamente de glicose "
            "como combustível em condições normais."
        ),
        "msg_alto": (
            "Excesso de carboidratos, especialmente refinados, está associado a obesidade, "
            "resistência à insulina, diabetes tipo 2 e dislipidemia (triglicerídeos elevados). "
            "O excesso é convertido em gordura hepática pelo fígado (lipogênese de novo)."
        ),
    },
    "sugars": {
        "ref_min": None, "ref_max": 50.0,
        "tipo": "Ingestão Diária Recomendada", "fonte": "OMS 2015",
        "msg_baixo": None,
        "msg_alto": (
            "Consumo excessivo de açúcares livres (>10% das calorias diárias) aumenta o risco "
            "de obesidade, cárie dentária, diabetes tipo 2 e doença cardiovascular. A frutose "
            "em excesso promove esteatose hepática mesmo em pessoas com peso normal. "
            "A OMS recomenda reduzir a <5% das calorias para benefícios adicionais (<25 g/dia)."
        ),
    },
    "fiber": {
        "ref_min": 25.0, "ref_max": None,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 2005",
        "msg_baixo": (
            "Baixo consumo de fibras está associado a constipação intestinal, disbiose da "
            "microbiota, maior risco de câncer colorretal, doença cardiovascular e diabetes "
            "tipo 2. Fibras solúveis reduzem o colesterol LDL; fibras insolúveis regulam o "
            "trânsito intestinal. A maioria da população consome menos da metade do recomendado."
        ),
        "msg_alto": None,
    },
    "saturated_fat": {
        "ref_min": None, "ref_max": 22.0,
        "tipo": "Ingestão Diária Recomendada", "fonte": "AHA 2021",
        "msg_baixo": None,
        "msg_alto": (
            "Consumo elevado de gordura saturada aumenta o LDL, favorecendo aterosclerose "
            "e doença arterial coronariana. Fontes principais: carnes gordurosas, laticínios "
            "integrais, manteiga e óleo de coco. A substituição por gorduras insaturadas "
            "(azeite, abacate, oleaginosas) reduz significativamente o risco cardiovascular."
        ),
    },
    "cholesterol": {
        "ref_min": None, "ref_max": 300.0,
        "tipo": "Ingestão Diária Recomendada", "fonte": "AHA/ACC 2019",
        "msg_baixo": None,
        "msg_alto": (
            "O impacto do colesterol dietético no colesterol sanguíneo varia conforme a genética. "
            "Consumo >300 mg/dia pode aumentar o LDL em pessoas sensíveis. Alimentos ricos "
            "em colesterol dietético geralmente também contêm gordura saturada, o que amplifica "
            "o risco cardiovascular."
        ),
    },
    "sodium": {
        "ref_min": 500.0, "ref_max": 2300.0,
        "tipo": "Ingestão Diária Recomendada", "fonte": "OMS 2012 / AHA",
        "msg_baixo": (
            "Sódio é essencial para equilíbrio eletrolítico, transmissão nervosa e contração "
            "muscular. Deficiência grave (hiponatremia) causa confusão mental, convulsões e "
            "pode ser fatal. Em condições normais, a deficiência alimentar de sódio é rara."
        ),
        "msg_alto": (
            "Consumo excessivo de sódio é a principal causa dietética de hipertensão arterial. "
            "O sódio em excesso retém água, aumentando o volume sanguíneo e a pressão. "
            "Está associado a maior risco de AVC, doença cardíaca, insuficiência renal e "
            "osteoporose. A maioria da população consome 3–4× mais que o ideal (OMS: <2000 mg/dia)."
        ),
    },
    # ── Vitaminas ─────────────────────────────────────────────────────────────
    "vitamin_c": {
        "ref_min": 65.0, "ref_max": 2000.0,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 2000",
        "msg_baixo": (
            "Deficiência de vitamina C causa escorbuto (sangramento nas gengivas, cicatrização "
            "prejudicada, fadiga extrema). Valores moderadamente baixos comprometem a imunidade, "
            "a síntese de colágeno e a absorção de ferro não-heme. Fumantes necessitam de "
            "35 mg/dia a mais devido ao estresse oxidativo aumentado."
        ),
        "msg_alto": (
            "Em doses muito altas (>2000 mg/dia de suplemento), pode causar diarreia osmótica "
            "e cálculos renais de oxalato. A toxicidade por fontes alimentares é extremamente "
            "rara — o risco vem principalmente de suplementação excessiva."
        ),
    },
    "vitamin_d": {
        "ref_min": 15.0, "ref_max": 100.0,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 2011",
        "msg_baixo": (
            "Deficiência de vitamina D é pandêmica globalmente. Causa raquitismo em crianças e "
            "osteomalácia em adultos. Está associada a osteoporose, fraqueza muscular, depressão, "
            "doenças autoimunes e infecções respiratórias. A principal fonte é a síntese "
            "cutânea pela exposição solar."
        ),
        "msg_alto": (
            "Toxicidade (hipervitaminose D) ocorre com ingestão >100 mcg/dia por período prolongado, "
            "causando hipercalcemia: náusea, vômitos, fraqueza, cálculos renais e calcificação "
            "de tecidos moles. Impossível atingir por exposição solar — o risco vem exclusivamente "
            "de suplementação excessiva."
        ),
    },
    "vitamin_e": {
        "ref_min": 15.0, "ref_max": 1000.0,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 2000",
        "msg_baixo": (
            "Deficiência de vitamina E (antioxidante lipossolúvel) causa neuropatia periférica, "
            "fraqueza muscular e ataxia. A deficiência alimentar isolada é rara, mas comum em "
            "síndromes de má absorção de gordura (doença de Crohn, fibrose cística)."
        ),
        "msg_alto": (
            "Em doses muito altas (>1000 mg/dia de suplemento), pode interferir na coagulação, "
            "aumentando o risco de hemorragia — especialmente com anticoagulantes. Grandes estudos "
            "de suplementação não demonstraram benefício cardiovascular e alguns sugeriram "
            "aumento de mortalidade em altas doses."
        ),
    },
    "vitamin_k": {
        "ref_min": 90.0, "ref_max": None,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 2001",
        "msg_baixo": (
            "Vitamina K é essencial para a coagulação sanguínea e saúde óssea. Deficiência "
            "causa sangramento excessivo e, cronicamente, maior risco de osteoporose e "
            "calcificação arterial. Recém-nascidos têm risco elevado (hemorragia neonatal)."
        ),
        "msg_alto": None,
    },
    "vitamin_b6": {
        "ref_min": 1.3, "ref_max": 100.0,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 1998",
        "msg_baixo": (
            "Deficiência de vitamina B6 causa dermatite seborreica, glossite, anemia microcítica, "
            "depressão e convulsões. É essencial para o metabolismo de aminoácidos e síntese "
            "de neurotransmissores (serotonina, dopamina)."
        ),
        "msg_alto": (
            "Neuropatia periférica (dormência, formigamento) pode ocorrer com ingestão crônica "
            ">100 mg/dia de suplementos. A toxicidade é improvável por fontes alimentares e "
            "é reversível após suspensão da suplementação excessiva."
        ),
    },
    "vitamin_b12": {
        "ref_min": 2.4, "ref_max": None,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 1998",
        "msg_baixo": (
            "Deficiência de vitamina B12 causa anemia megaloblástica, neuropatia (desmielinização "
            "neuronal) e alterações cognitivas — desde depressão até demência irreversível. "
            "Grupos de risco: vegetarianos estritos, veganos, idosos e pessoas com gastrite "
            "atrófica. A deficiência pode levar anos para manifestar sintomas."
        ),
        "msg_alto": None,
    },
    "thiamin": {
        "ref_min": 1.1, "ref_max": None,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 1998",
        "msg_baixo": (
            "Deficiência de tiamina (vitamina B1) causa beribéri (cardíaco ou neurológico) e, "
            "em casos agudos associados ao alcoolismo, a síndrome de Wernicke-Korsakoff "
            "(confusão, ataxia, paralisia ocular e amnésia severa). Essencial para o "
            "metabolismo da glicose e função do sistema nervoso."
        ),
        "msg_alto": None,
    },
    "riboflavin": {
        "ref_min": 1.1, "ref_max": None,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 1998",
        "msg_baixo": (
            "Ariboflavinose (deficiência de vitamina B2) causa queilose angular (rachaduras nos "
            "cantos da boca), glossite, dermatite e fotofobia. Compromete a produção de energia "
            "celular e a ativação de outras vitaminas B (B6, ácido fólico)."
        ),
        "msg_alto": None,
    },
    "niacin": {
        "ref_min": 14.0, "ref_max": 35.0,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 1998",
        "msg_baixo": (
            "Deficiência grave de niacina (vitamina B3) causa pelagra: dermatite em áreas "
            "expostas ao sol, diarreia e demência — os '3 Ds'. Essencial para o metabolismo "
            "energético e reparo do DNA."
        ),
        "msg_alto": (
            "Em doses farmacológicas (>35 mg/dia de suplemento), a niacina causa flushing "
            "(rubor cutâneo), prurido e hepatotoxicidade em uso prolongado. Grandes estudos "
            "questionaram sua eficácia em reduzir eventos cardiovasculares."
        ),
    },
    "folic_acid": {
        "ref_min": 400.0, "ref_max": 1000.0,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 1998",
        "msg_baixo": (
            "Deficiência de folato causa anemia megaloblástica e, em gestantes, defeitos do "
            "tubo neural no feto (anencefalia, espinha bífida). Também eleva a homocisteína "
            "plasmática, fator de risco cardiovascular independente."
        ),
        "msg_alto": (
            "Ingestão muito elevada de ácido fólico sintético (>1000 mcg/dia) pode mascarar "
            "a deficiência de vitamina B12, retardando o diagnóstico de neuropatia grave. "
            "Há também preocupação teórica de promoção de crescimento de tumores preexistentes."
        ),
    },
    "food_folate": {
        "ref_min": 400.0, "ref_max": None,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 1998",
        "msg_baixo": (
            "Baixo consumo de folato natural (vegetais de folha escura, leguminosas, frutas "
            "cítricas) está associado a anemia megaloblástica, maior risco cardiovascular por "
            "elevação da homocisteína e, em gestantes, risco de defeitos do tubo neural."
        ),
        "msg_alto": None,
    },
    "beta_carotene": {
        "ref_min": None, "ref_max": 30000.0,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 2000",
        "msg_baixo": None,
        "msg_alto": (
            "Em doses muito elevadas de suplementos (>30 mg/dia), beta-caroteno aumentou o risco "
            "de câncer de pulmão e mortalidade em fumantes (estudos ATBC e CARET). Fontes "
            "alimentares são seguras. Consumo excessivo pode causar carotenodermia (pele "
            "alaranjada), inofensiva. O risco é exclusivo da suplementação em altas doses."
        ),
    },
    # ── Minerais ──────────────────────────────────────────────────────────────
    "calcium": {
        "ref_min": 1000.0, "ref_max": 2500.0,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 2011",
        "msg_baixo": (
            "Baixo consumo de cálcio ao longo da vida aumenta o risco de osteoporose e fraturas. "
            "Hipocalcemia aguda causa tetania, espasmos musculares, convulsões e arritmias. "
            "O cálcio também é essencial para contração muscular, coagulação e transmissão nervosa."
        ),
        "msg_alto": (
            "Consumo excessivo (hipercalcemia) aumenta o risco de cálculos renais, constipação, "
            "interferência na absorção de ferro e zinco e, possivelmente, risco cardiovascular "
            "por calcificação arterial. O risco é maior com suplementação excessiva do que "
            "com fontes alimentares."
        ),
    },
    "iron": {
        "ref_min": 8.0, "ref_max": 45.0,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 2001",
        "msg_baixo": (
            "Deficiência de ferro é a carência nutricional mais prevalente no mundo. Causa "
            "anemia ferropriva (fadiga, palidez, dispneia), prejudica o desenvolvimento cognitivo "
            "em crianças e reduz a imunidade. Mulheres em idade fértil necessitam de 18 mg/dia."
        ),
        "msg_alto": (
            "Excesso de ferro promove estresse oxidativo (reação de Fenton), danificando células "
            "hepáticas, cardíacas e pancreáticas (hemocromatose). Associado a maior risco de "
            "diabetes tipo 2, doença hepática e câncer colorretal. O risco vem de suplementação "
            "desnecessária ou hemocromatose hereditária."
        ),
    },
    "magnesium": {
        "ref_min": 310.0, "ref_max": 350.0,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 1997",
        "msg_baixo": (
            "Hipomagnesemia está associada a câimbras musculares, arritmias cardíacas (especialmente "
            "fibrilação atrial), hipertensão, resistência à insulina e enxaquecas. O magnésio é "
            "cofator de mais de 300 enzimas e essencial para síntese de ATP. Baixo consumo é "
            "comum em dietas ricas em alimentos ultraprocessados."
        ),
        "msg_alto": (
            "Hipermagnesemia alimentar é extremamente rara em pessoas saudáveis, pois o rim excreta "
            "o excesso eficientemente. O risco de toxicidade existe com suplementação excessiva "
            "em pessoas com insuficiência renal, causando hipotensão e depressão do SNC."
        ),
    },
    "zinc": {
        "ref_min": 8.0, "ref_max": 40.0,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 2001",
        "msg_baixo": (
            "Deficiência de zinco compromete a imunidade, cicatrização, crescimento e "
            "desenvolvimento sexual. Causa perda de paladar e olfato, queda de cabelo e dermatite. "
            "Em crianças, retarda o crescimento e aumenta a morbimortalidade por infecções."
        ),
        "msg_alto": (
            "Suplementação excessiva (>40 mg/dia) inibe a absorção de cobre, podendo causar "
            "deficiência de cobre e anemia. Doses muito altas causam náusea, vômitos e "
            "supressão imunológica paradoxal."
        ),
    },
    "potassium": {
        "ref_min": 2600.0, "ref_max": None,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 2019",
        "msg_baixo": (
            "Baixo consumo de potássio está associado a hipertensão, maior risco de AVC, "
            "arritmias cardíacas e cálculos renais. O potássio contrabalança os efeitos do "
            "sódio na pressão sanguínea. Deficiência severa (hipocalemia) causa fraqueza "
            "muscular grave e paralisia."
        ),
        "msg_alto": None,
    },
    "phosphorus": {
        "ref_min": 700.0, "ref_max": 4000.0,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 1997",
        "msg_baixo": (
            "Hipofosfatemia grave causa fraqueza muscular, dor óssea e encefalopatia. A "
            "deficiência alimentar é rara em dietas ocidentais, mas pode ocorrer em síndromes "
            "de má absorção, alcoolismo e uso prolongado de antiácidos que quelam fósforo."
        ),
        "msg_alto": (
            "Hiperfosfatemia crônica, comum em insuficiência renal, causa calcificações vasculares "
            "e aumenta a mortalidade cardiovascular. O excesso de fósforo de aditivos alimentares "
            "(refrigerantes, embutidos) pode prejudicar a saúde óssea ao alterar o equilíbrio "
            "cálcio-fósforo."
        ),
    },
    "copper": {
        "ref_min": 0.9, "ref_max": 10.0,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 2001",
        "msg_baixo": (
            "Deficiência de cobre causa anemia (similar à ferropriva), neutropenia, fragilidade "
            "óssea, despigmentação e neuropatia. Pode ocorrer por ingestão excessiva de zinco "
            "(competição pela absorção) ou síndromes de má absorção."
        ),
        "msg_alto": (
            "Em doses muito elevadas (>10 mg/dia), causa hepatotoxicidade. A doença de Wilson "
            "(acúmulo genético de cobre) leva a danos hepáticos e neurológicos graves. "
            "Encanamentos antigos de cobre podem ser fonte de exposição excessiva."
        ),
    },
    "selenium": {
        "ref_min": 55.0, "ref_max": 400.0,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 2000",
        "msg_baixo": (
            "Deficiência de selênio está associada à doença de Keshan (cardiomiopatia), doença "
            "de Kashin-Beck (osteoartropatia) e hipotireoidismo. O selênio é essencial para "
            "a conversão do hormônio tireoidiano T4→T3 e para a defesa antioxidante."
        ),
        "msg_alto": (
            "Selenose causa queda de cabelo, fragilidade das unhas, halitose com odor de alho, "
            "náusea e neuropatia periférica. Pode ser fatal em casos extremos. Atenção: "
            "a castanha-do-pará pode conter até 544 mcg por unidade — consumo excessivo "
            "é uma preocupação real no Brasil."
        ),
    },
    "choline": {
        "ref_min": 425.0, "ref_max": 3500.0,
        "tipo": "Ingestão Diária Recomendada", "fonte": "IOM DRI 1998",
        "msg_baixo": (
            "Deficiência de colina causa esteatose hepática (gordura no fígado) e dano muscular. "
            "A colina é precursora da acetilcolina e componente essencial das membranas celulares. "
            "Baixo consumo está associado a maior risco cardiovascular e declínio cognitivo."
        ),
        "msg_alto": (
            "Consumo muito elevado (>3500 mg/dia) produz odor corporal de peixe "
            "(trimetilaminúria), hipotensão e hepatotoxicidade. O excesso alimentar é raro; "
            "o risco vem de suplementação em megadoses."
        ),
    },
}

REF_GROUPS: dict[str, list[str]] = {
    "🩺 Marcadores Clínicos":    ["total_cholesterol", "systolic_bp", "diastolic_bp",
                                   "c_reactive", "bmi", "waist_circ"],
    "🥩 Macronutrientes":        ["protein", "carbohydrates", "sugars", "fiber",
                                   "saturated_fat", "cholesterol", "sodium"],
    "💊 Vitaminas":              ["vitamin_c", "vitamin_d", "vitamin_e", "vitamin_k",
                                   "vitamin_b6", "vitamin_b12", "thiamin", "riboflavin",
                                   "niacin", "folic_acid", "food_folate", "beta_carotene"],
    "⚗️ Minerais":               ["calcium", "iron", "magnesium", "zinc", "potassium",
                                   "phosphorus", "copper", "selenium", "choline"],
}


def lbl(col: str) -> str:
    return LABELS.get(col, col.replace("_", " ").title())


# ── Carregamento de dados ─────────────────────────────────────────────────────
@st.cache_data(show_spinner="Carregando dados de saúde…")
def get_data() -> pd.DataFrame:
    return load_data()


df_full = get_data()

# ── Sidebar – filtros ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="
            background: linear-gradient(145deg, #BD3A9A 0%, #F73670 50%, #FA3939 100%);
            border-radius: 14px;
            padding: 20px 18px 18px 18px;
            margin-bottom: 2px;
            box-shadow: 0 6px 20px rgba(15, 34, 64, 0.45);
        ">
            <div style="display:flex; align-items:center; gap:11px; margin-bottom:8px;">
                <svg width="34" height="34" viewBox="0 0 34 34" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="17" cy="17" r="16" fill="rgba(255,255,255,0.12)" stroke="rgba(255,255,255,0.35)" stroke-width="1.2"/>
                    <path d="M17 27 C17 27 6 19.5 6 13a6 6 0 0 1 11-3.3A6 6 0 0 1 28 13c0 6.5-11 14-11 14z"
                          fill="rgba(255,255,255,0.92)"/>
                    <polyline points="9,17 11,17 13,12 15,22 17,15 19,19 21,17 25,17"
                              stroke="#FF2631" stroke-width="1.6" fill="none"
                              stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span style="
                    font-size: 1.65rem;
                    font-weight: 800;
                    color: #FFFFFF;
                    letter-spacing: -0.4px;
                    text-shadow: 0 2px 8px rgba(0,0,0,0.25);
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                ">MedBoard</span>
            </div>
            <div style="
                color: rgba(255,255,255,0.75);
                font-size: 0.82rem;
                font-weight: 400;
                letter-spacing: 0.4px;
                padding-left: 2px;
            ">Dashboard de Saúde UFSM</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()
    st.caption(f"Fonte dos dados: {get_data_source(df_full)}")

    st.markdown("### 🔍 Filtros Globais")

    # Faixa etária
    age_vals = df_full["age"].dropna()
    age_min, age_max = int(age_vals.min()), int(age_vals.max())

    # IMC
    bmi_vals = df_full["bmi"].dropna()
    bmi_min, bmi_max = round(float(bmi_vals.min()), 1), round(float(bmi_vals.max()), 1)

    # Armazena defaults no session_state para o callback de reset
    st.session_state._age_min = age_min
    st.session_state._age_max = age_max
    st.session_state._bmi_min = bmi_min
    st.session_state._bmi_max = bmi_max

    def _reset_filters():
        st.session_state.age_slider    = (st.session_state._age_min, st.session_state._age_max)
        st.session_state.bmi_slider    = (st.session_state._bmi_min, st.session_state._bmi_max)
        st.session_state.include_no_bmi = True
        for col in CVD_CONDITIONS:
            st.session_state[f"sidebar_cvd_{col}"] = False

    age_range = st.slider(
        "Faixa Etária (anos)",
        min_value=age_min, max_value=age_max,
        value=(age_min, age_max),
        key="age_slider",
        help="Filtra todos os gráficos e a tabela por intervalo de idade.",
    )

    include_no_bmi = st.checkbox("Incluir registros sem IMC", value=True, key="include_no_bmi")
    bmi_range = st.slider(
        "Faixa de IMC (kg/m²)",
        min_value=bmi_min, max_value=bmi_max,
        value=(bmi_min, bmi_max),
        key="bmi_slider",
        help="Índice de Massa Corporal.",
    )

    # Condições cardiovasculares
    st.markdown("**Condições Cardiovasculares**")
    cvd_filter: dict[str, bool] = {}
    for col, label in CVD_CONDITIONS.items():
        if col in df_full.columns:
            cvd_filter[col] = st.checkbox(
                f"Apenas com {label}", value=False, key=f"sidebar_cvd_{col}"
            )

    st.button("↺ Resetar Filtros", use_container_width=True, on_click=_reset_filters)

    st.divider()
    st.markdown(
        "<small style='color:#6B7280'>Projeto de Software 1 · UFSM<br><a href='https://github.com/DiegoRockenbach' target='_blank'>Diego Rockenbach</a> & <a href='https://github.com/lucasaued' target='_blank'>Lucas Aued</a></small>",
        unsafe_allow_html=True,
    )


# ── Aplicar filtros ───────────────────────────────────────────────────────────
def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    mask = pd.Series(True, index=df.index)

    if "age" in df.columns:
        mask &= df["age"].between(age_range[0], age_range[1])

    if "bmi" in df.columns:
        bmi_mask = df["bmi"].between(bmi_range[0], bmi_range[1])
        if include_no_bmi:
            bmi_mask |= df["bmi"].isna()
        mask &= bmi_mask

    for col, selected in cvd_filter.items():
        if selected and col in df.columns:
            mask &= df[col] == True

    return df[mask].copy()


df = apply_filters(df_full)

# ── Abas principais ───────────────────────────────────────────────────────────
tab2, tab1, tab3, tab4, tab5, tab6 = st.tabs([
    "🔍  Explorar Dados",
    "📊  Visão Geral",
    "🥦  Nutrição",
    "❤️  Fatores de Risco",
    "📈  Correlações",
    "🩸  Ref. Clínicas",
])


# ═══════════════════════════════════════════════════════
#  TAB 1 – VISÃO GERAL
# ═══════════════════════════════════════════════════════
with tab1:
    st.subheader("Visão Geral da População")

    # KPIs
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric("👥 Registros", f"{len(df):,}")

    with c2:
        avg_age = df["age"].mean() if "age" in df.columns else 0
        st.metric("📅 Idade Média", f"{avg_age:.1f} anos")

    with c3:
        avg_bmi = df["bmi"].mean() if "bmi" in df.columns else 0
        st.metric("⚖️ IMC Médio", f"{avg_bmi:.1f} kg/m²")

    with c4:
        avg_sbp = df["systolic_bp"].mean() if "systolic_bp" in df.columns else 0
        st.metric("🩺 PA Sistólica Média", f"{avg_sbp:.0f} mmHg")

    with c5:
        cvd_cols_present = [c for c in CVD_CONDITIONS if c in df.columns]
        if cvd_cols_present:
            n_cvd = df[cvd_cols_present].any(axis=1).sum()
            pct_cvd = n_cvd / len(df) * 100 if len(df) else 0
            st.metric("❤️ Com alguma DCV", f"{pct_cvd:.1f}%", f"{n_cvd:,} casos")

    st.divider()

    # ── Distribuições: Idade e IMC ──
    col_age, col_bmi_chart = st.columns(2)

    with col_age:
        st.markdown("#### Distribuição por Idade")
        if "age" in df.columns:
            fig = px.histogram(
                df.dropna(subset=["age"]), x="age", nbins=30,
                color_discrete_sequence=[C_BLUE],
                template=TPLT,
                labels={"age": "Idade (anos)", "count": "Quantidade"},
            )
            fig.update_traces(marker_line_color="white", marker_line_width=0.5)
            fig.update_layout(showlegend=False, height=310,
                              margin=dict(l=0, r=0, t=10, b=0))
            st.plotly_chart(fig, use_container_width=True)

    with col_bmi_chart:
        st.markdown("#### Distribuição do IMC")
        if "bmi" in df.columns:
            fig = px.histogram(
                df.dropna(subset=["bmi"]), x="bmi", nbins=30,
                color_discrete_sequence=[C_GRN],
                template=TPLT,
                labels={"bmi": "IMC (kg/m²)", "count": "Quantidade"},
            )
            for x_val, txt, color in [
                (18.5, "Abaixo do peso", "#94A3B8"),
                (25,   "Sobrepeso",      C_AMB),
                (30,   "Obesidade",      C_RED),
            ]:
                fig.add_vline(x=x_val, line_dash="dot", line_color=color,
                              annotation_text=txt, annotation_font_size=11)
            fig.update_traces(marker_line_color="white", marker_line_width=0.5)
            fig.update_layout(showlegend=False, height=310,
                              margin=dict(l=0, r=0, t=10, b=0))
            st.plotly_chart(fig, use_container_width=True)

    # ── Prevalência CVD ──
    st.markdown("#### Prevalência de Condições Cardiovasculares")
    cvd_rows = []
    for col, label in CVD_CONDITIONS.items():
        if col in df.columns:
            n = int(df[col].sum())
            total = len(df)
            cvd_rows.append({
                "Condição": label,
                "Casos": n,
                "Percentual (%)": round(n / total * 100, 2) if total else 0,
            })

    if cvd_rows:
        df_cvd = pd.DataFrame(cvd_rows)
        fig = px.bar(
            df_cvd, x="Condição", y="Percentual (%)",
            color="Percentual (%)",
            color_continuous_scale=[[0, "#FEF3C7"], [0.5, C_AMB], [1, C_RED]],
            text="Casos",
            template=TPLT,
            labels={"Condição": "", "Percentual (%)": "% da População"},
        )
        fig.update_traces(texttemplate="%{text:,} casos", textposition="outside")
        fig.update_layout(height=350, margin=dict(l=0, r=0, t=10, b=0),
                          coloraxis_showscale=False, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # ── Faixas etárias ──
    col_pie, col_info = st.columns([3, 2])
    with col_pie:
        st.markdown("#### Composição por Faixa Etária")
        if "age" in df.columns:
            bins   = [0, 12, 18, 35, 50, 65, 200]
            labels_age = ["Criança (0–12)", "Adolescente (13–18)",
                          "Adulto jovem (19–35)", "Adulto (36–50)",
                          "Meia-idade (51–65)", "Idoso (65+)"]
            df_tmp = df.copy()
            df_tmp["Faixa"] = pd.cut(df_tmp["age"], bins=bins,
                                     labels=labels_age, right=True)
            counts = df_tmp["Faixa"].value_counts().sort_index()
            fig = px.pie(
                values=counts.values, names=counts.index,
                color_discrete_sequence=px.colors.qualitative.Set2,
                hole=0.42, template=TPLT,
            )
            fig.update_layout(height=340, margin=dict(l=0, r=0, t=10, b=0))
            st.plotly_chart(fig, use_container_width=True)

    with col_info:
        st.markdown("#### Resumo Clínico")
        summary_cols = {
            "systolic_bp":       "PA Sistólica",
            "diastolic_bp":      "PA Diastólica",
            "total_cholesterol": "Colesterol Total",
            "c_reactive":        "Proteína C-Reativa",
            "waist_circ":        "Circ. Abdominal",
        }
        rows = []
        for col, name in summary_cols.items():
            if col in df.columns:
                s = df[col].dropna()
                rows.append({
                    "Indicador": name,
                    "Média": f"{s.mean():.1f}",
                    "Mediana": f"{s.median():.1f}",
                    "Desvio": f"{s.std():.1f}",
                })
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True,
                         hide_index=True)


# ═══════════════════════════════════════════════════════
#  TAB 2 – EXPLORAR DADOS
# ═══════════════════════════════════════════════════════
with tab2:
    all_cols = list(df.columns)
    default_visible = ["seqn", "age", "bmi", "systolic_bp", "diastolic_bp",
                       "total_cholesterol", "c_reactive",
                       "congestive", "coronary", "heart_attack", "stroke", "angina"]
    default_visible = [c for c in default_visible if c in all_cols]

    # Inicializa estado das badges
    PINNED = {"seqn"}  # colunas sempre visíveis e não desselecionáveis

    if "visible_cols" not in st.session_state:
        st.session_state.visible_cols = set(default_visible)
    st.session_state.visible_cols &= set(all_cols)   # remove colunas inexistentes
    st.session_state.visible_cols |= PINNED           # garante pinadas sempre presentes

    def _toggle_col(col_name):
        if col_name in PINNED:
            return
        if col_name in st.session_state.visible_cols:
            st.session_state.visible_cols.discard(col_name)
        else:
            st.session_state.visible_cols.add(col_name)

    def _select_all():
        st.session_state.visible_cols = set(all_cols)

    def _deselect_all():
        st.session_state.visible_cols = set(PINNED)

    # Badges de seleção de colunas (6 por linha → 1 slot livre no final para ações)
    BADGES_PER_ROW = 6
    rows = [all_cols[i : i + BADGES_PER_ROW] for i in range(0, len(all_cols), BADGES_PER_ROW)]

    for idx, row in enumerate(rows):
        is_last = (idx == len(rows) - 1)
        cols_ui = st.columns(BADGES_PER_ROW)

        for j, col_name in enumerate(row):
            with cols_ui[j]:
                st.button(
                    lbl(col_name),
                    key=f"badge_{col_name}",
                    type="primary" if col_name in st.session_state.visible_cols else "secondary",
                    use_container_width=True,
                    on_click=_toggle_col,
                    args=(col_name,),
                    disabled=col_name in PINNED,
                )

        if is_last and len(row) < BADGES_PER_ROW:
            with cols_ui[len(row)]:
                sub1, sub2 = st.columns(2)
                with sub1:
                    st.button("☑", key="btn_sel_all", use_container_width=True,
                              on_click=_select_all, help="Selecionar todas as colunas")
                with sub2:
                    st.button("☐", key="btn_desel_all", use_container_width=True,
                              on_click=_deselect_all, help="Desmarcar todas as colunas")

    selected_cols = [c for c in all_cols if c in st.session_state.visible_cols]

    ctrl_sort, ctrl_dir, ctrl_dl = st.columns([4, 1.2, 1.4])

    with ctrl_sort:
        sort_options = selected_cols if selected_cols else all_cols
        sort_col = st.selectbox("Ordenar por", options=sort_options, format_func=lbl,
                                key="sort_col_key")

    with ctrl_dir:
        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        sort_asc = st.radio("Direção", ["Crescente ▲", "Decrescente ▼"],
                            horizontal=False, label_visibility="collapsed")

    with ctrl_dl:
        st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)
        csv_data = (df[selected_cols] if selected_cols else df).to_csv(index=False).encode("utf-8")
        n_rows = len(df[selected_cols]) if selected_cols else len(df)
        st.download_button(
            label="⬇ Exportar CSV",
            data=csv_data,
            file_name="nhanes_filtrado.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary",
            help=f"Baixar {n_rows:,} registros com {len(selected_cols)} colunas em CSV",
        )

    # Prepara DataFrame de exibição
    disp_df = df[selected_cols].copy() if selected_cols else df.copy()
    if sort_col and sort_col in disp_df.columns:
        disp_df = disp_df.sort_values(sort_col, ascending=(sort_asc == "Crescente ▲"))

    # Paginação
    PAGE_SIZE = 25
    total_rows  = len(disp_df)
    total_pages = max(1, (total_rows - 1) // PAGE_SIZE + 1)

    if "table_page" not in st.session_state:
        st.session_state.table_page = 1
    st.session_state.table_page = min(st.session_state.table_page, total_pages)
    st.session_state._total_pages = total_pages

    def _go_first(): st.session_state.table_page = 1
    def _go_prev():
        if st.session_state.table_page > 1:
            st.session_state.table_page -= 1
    def _go_next():
        if st.session_state.table_page < st.session_state._total_pages:
            st.session_state.table_page += 1
    def _go_last():
        st.session_state.table_page = st.session_state._total_pages

    pg1, pg2, pg3, pg4, pg5 = st.columns([1, 1, 5, 1, 1])
    with pg1:
        st.button("⏮", on_click=_go_first, help="Primeira página")
    with pg2:
        st.button("◀", on_click=_go_prev, help="Página anterior")
    with pg3:
        st.markdown(
            f"<center>Página <b>{st.session_state.table_page}</b> de "
            f"<b>{total_pages}</b> &nbsp;·&nbsp; <b>{total_rows:,}</b> registros</center>",
            unsafe_allow_html=True,
        )
    with pg4:
        st.button("▶", on_click=_go_next, help="Próxima página")
    with pg5:
        st.button("⏭", on_click=_go_last, help="Última página")

    start = (st.session_state.table_page - 1) * PAGE_SIZE
    st.dataframe(
        disp_df.iloc[start : start + PAGE_SIZE],
        use_container_width=True,
        height=540,
        hide_index=True,
    )


# ═══════════════════════════════════════════════════════
#  TAB 3 – NUTRIÇÃO
# ═══════════════════════════════════════════════════════
with tab3:
    st.subheader("Análise Nutricional")

    cat_sel, _ = st.columns([2, 5])
    with cat_sel:
        categoria = st.selectbox(
            "Categoria de Nutrientes",
            ["Macronutrientes", "Vitaminas", "Minerais"],
        )

    cat_map = {
        "Macronutrientes": NUTRIENTS_MACRO,
        "Vitaminas":       NUTRIENTS_VITAMINS,
        "Minerais":        NUTRIENTS_MINERALS,
    }
    nutrients = [n for n in cat_map[categoria] if n in df.columns]

    if not nutrients:
        st.warning("Nenhuma coluna nutricional disponível nesta categoria.")
    else:
        # ── Box plots de distribuição ──
        st.markdown(f"#### Distribuição de {categoria}")
        df_melt = (
            df[nutrients]
            .melt(var_name="Nutriente", value_name="Valor")
            .dropna()
        )
        df_melt["Nutriente"] = df_melt["Nutriente"].map(lbl)

        fig = px.box(
            df_melt, x="Nutriente", y="Valor",
            color="Nutriente",
            color_discrete_sequence=C_SEQ * 4,
            template=TPLT, points=False,
        )
        fig.update_layout(
            showlegend=False, height=400,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis_tickangle=-30,
        )
        st.plotly_chart(fig, use_container_width=True)

        # ── Comparação CVD vs sem CVD ──
        st.markdown("#### Comparação: Com × Sem Condição Cardiovascular")

        cc1, cc2 = st.columns(2)
        with cc1:
            compare_nut = st.selectbox(
                "Nutriente para comparar",
                options=nutrients,
                format_func=lbl,
            )
        with cc2:
            compare_cvd = st.selectbox(
                "Condição cardiovascular",
                options=[c for c in CVD_CONDITIONS if c in df.columns],
                format_func=lambda x: CVD_CONDITIONS[x],
                key="nut_cvd",
            )

        if compare_cvd in df.columns and compare_nut in df.columns:
            df_cmp = df[[compare_nut, compare_cvd]].dropna(subset=[compare_nut])
            df_cmp["Status"] = df_cmp[compare_cvd].apply(
                lambda x: CVD_CONDITIONS[compare_cvd] if x else "Sem condição"
            )
            fig = px.violin(
                df_cmp, x="Status", y=compare_nut,
                color="Status",
                color_discrete_map={
                    CVD_CONDITIONS[compare_cvd]: C_RED,
                    "Sem condição": C_BLUE,
                },
                box=True, points=False, template=TPLT,
                labels={compare_nut: lbl(compare_nut)},
            )
            fig.update_layout(showlegend=False, height=380,
                              margin=dict(l=0, r=0, t=10, b=0))
            st.plotly_chart(fig, use_container_width=True)

        # ── Estatísticas descritivas ──
        st.markdown("#### Estatísticas Descritivas")
        desc = df[nutrients].describe().T
        desc.index = [lbl(i) for i in desc.index]
        desc = desc.rename(columns={
            "count": "Registros", "mean": "Média", "std": "Desvio Padrão",
            "min": "Mínimo", "25%": "P25", "50%": "Mediana",
            "75%": "P75", "max": "Máximo",
        })
        st.dataframe(desc.round(2), use_container_width=True)


# ═══════════════════════════════════════════════════════
#  TAB 4 – FATORES DE RISCO
# ═══════════════════════════════════════════════════════
with tab4:
    st.subheader("Fatores de Risco Cardiovascular")

    # ── Dispersão pressão arterial ──
    if "systolic_bp" in df.columns and "diastolic_bp" in df.columns:
        st.markdown("#### Pressão Arterial por Condição")

        bp_cvd = st.selectbox(
            "Colorir por condição",
            options=[c for c in CVD_CONDITIONS if c in df.columns],
            format_func=lambda x: CVD_CONDITIONS[x],
            key="bp_cvd",
        )

        df_bp = df[["systolic_bp", "diastolic_bp", bp_cvd]].dropna(
            subset=["systolic_bp", "diastolic_bp"]
        )
        df_bp["Status"] = df_bp[bp_cvd].apply(
            lambda x: CVD_CONDITIONS[bp_cvd] if x else "Sem condição"
        )
        sample = df_bp.sample(min(3000, len(df_bp)), random_state=42)

        fig = px.scatter(
            sample, x="systolic_bp", y="diastolic_bp", color="Status",
            color_discrete_map={CVD_CONDITIONS[bp_cvd]: C_RED, "Sem condição": C_BLUE},
            opacity=0.4, template=TPLT,
            labels={"systolic_bp": "PA Sistólica (mmHg)",
                    "diastolic_bp": "PA Diastólica (mmHg)"},
        )
        fig.add_vline(x=130, line_dash="dot", line_color=C_AMB,
                      annotation_text="Hipertensão est. 1 (≥130)", annotation_font_size=11)
        fig.add_hline(y=80, line_dash="dot", line_color=C_AMB)
        fig.update_layout(height=420, margin=dict(l=0, r=0, t=10, b=0),
                          legend=dict(orientation="h", y=1.08))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── IMC médio por condição ──
    col_bmi2, col_chol2 = st.columns(2)

    with col_bmi2:
        st.markdown("#### IMC Médio: Com × Sem DCV")
        if "bmi" in df.columns:
            bmi_rows = []
            for cond, label in CVD_CONDITIONS.items():
                if cond in df.columns:
                    with_c    = df.loc[df[cond] == True,  "bmi"].dropna()
                    without_c = df.loc[df[cond] == False, "bmi"].dropna()
                    if len(with_c) > 5:
                        bmi_rows.append({"Condição": label[:22],
                                         "Com condição": with_c.mean(),
                                         "Sem condição": without_c.mean()})

            if bmi_rows:
                df_bmi2 = pd.DataFrame(bmi_rows).melt(
                    id_vars="Condição", var_name="Status", value_name="IMC Médio"
                )
                fig = px.bar(
                    df_bmi2, x="Condição", y="IMC Médio", color="Status",
                    barmode="group",
                    color_discrete_map={"Com condição": C_RED, "Sem condição": C_BLUE},
                    template=TPLT,
                )
                fig.update_layout(height=370, margin=dict(l=0, r=0, t=10, b=0),
                                  xaxis_tickangle=-20,
                                  legend=dict(orientation="h", y=1.1))
                st.plotly_chart(fig, use_container_width=True)

    with col_chol2:
        st.markdown("#### Colesterol Total por Condição")
        if "total_cholesterol" in df.columns:
            chol_cond = st.selectbox(
                "Condição",
                options=[c for c in CVD_CONDITIONS if c in df.columns],
                format_func=lambda x: CVD_CONDITIONS[x],
                key="chol_cond",
            )
            df_chol = df[["total_cholesterol", chol_cond]].dropna()
            df_chol["Status"] = df_chol[chol_cond].apply(
                lambda x: CVD_CONDITIONS[chol_cond] if x else "Sem condição"
            )
            fig = px.histogram(
                df_chol, x="total_cholesterol", color="Status",
                barmode="overlay", opacity=0.7, nbins=40, template=TPLT,
                color_discrete_map={CVD_CONDITIONS[chol_cond]: C_RED,
                                    "Sem condição": C_BLUE},
                labels={"total_cholesterol": "Colesterol Total (mg/dL)"},
            )
            fig.update_layout(height=370, margin=dict(l=0, r=0, t=10, b=0),
                              legend=dict(orientation="h", y=1.1))
            st.plotly_chart(fig, use_container_width=True)

    # ── Proteína C-Reativa ──
    st.markdown("#### Proteína C-Reativa por Condição Cardiovascular")
    if "c_reactive" in df.columns:
        crp_rows = []
        for cond, label in CVD_CONDITIONS.items():
            if cond in df.columns:
                sub = df[["c_reactive", cond]].dropna(subset=["c_reactive"])
                with_c    = sub.loc[sub[cond] == True,  "c_reactive"]
                without_c = sub.loc[sub[cond] == False, "c_reactive"]
                cap       = sub["c_reactive"].quantile(0.99)
                with_filtered    = with_c[with_c <= cap]
                without_filtered = without_c[without_c <= cap]
                n_sample = min(len(without_filtered), max(len(with_filtered) * 2, 100))
                for v in with_filtered:
                    crp_rows.append({"Condição": label[:20], "Status": "Com condição", "PCR": v})
                for v in without_filtered.sample(n_sample, random_state=42):
                    crp_rows.append({"Condição": label[:20], "Status": "Sem condição", "PCR": v})

        if crp_rows:
            fig = px.box(
                pd.DataFrame(crp_rows), x="Condição", y="PCR", color="Status",
                color_discrete_map={"Com condição": C_RED, "Sem condição": C_BLUE},
                points=False, template=TPLT,
                labels={"PCR": "Proteína C-Reativa (mg/L)"},
            )
            fig.update_layout(height=390, margin=dict(l=0, r=0, t=10, b=0),
                              xaxis_tickangle=-20,
                              legend=dict(orientation="h", y=1.1))
            st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════
#  TAB 5 – CORRELAÇÕES
# ═══════════════════════════════════════════════════════
with tab5:
    st.subheader("Análise de Correlações")

    # ── Mapa de calor ──
    st.markdown("#### Mapa de Correlação — Marcadores Clínicos × Nutrientes-Chave")
    key_nut  = ["protein", "fiber", "sodium", "potassium", "saturated_fat",
                "vitamin_c", "vitamin_d", "calcium", "magnesium"]
    clinical = ["age", "bmi", "systolic_bp", "diastolic_bp",
                "total_cholesterol", "c_reactive"]
    heat_cols = [c for c in key_nut + clinical if c in df.columns]

    if len(heat_cols) >= 4:
        df_corr = df[heat_cols].dropna(thresh=max(2, len(heat_cols) // 2))
        corr    = df_corr.corr()
        corr    = corr.rename(index={c: lbl(c) for c in corr.index},
                              columns={c: lbl(c) for c in corr.columns})

        fig = px.imshow(
            corr, color_continuous_scale="RdBu_r",
            zmin=-1, zmax=1, text_auto=".2f", aspect="auto", template=TPLT,
        )
        fig.update_traces(textfont_size=10)
        fig.update_layout(
            height=520, margin=dict(l=0, r=0, t=10, b=0),
            coloraxis_colorbar=dict(title="Correlação"),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="medboard-info">'
        "Valores próximos de +1 indicam correlação positiva forte; "
        "próximos de −1 indicam correlação negativa forte; "
        "próximos de 0 indicam ausência de relação linear."
        "</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    # ── Dispersão interativa ──
    st.markdown("#### Explorador de Dispersão")

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        x_def = numeric_cols.index("bmi") if "bmi" in numeric_cols else 0
        x_axis = st.selectbox("Eixo X", numeric_cols, index=x_def, format_func=lbl)
    with sc2:
        y_def = numeric_cols.index("total_cholesterol") if "total_cholesterol" in numeric_cols else 1
        y_axis = st.selectbox("Eixo Y", numeric_cols, index=y_def, format_func=lbl)
    with sc3:
        color_opts = ["(nenhum)"] + [c for c in CVD_CONDITIONS if c in df.columns]
        color_by   = st.selectbox(
            "Colorir por",
            options=color_opts,
            format_func=lambda x: "(nenhum)" if x == "(nenhum)" else CVD_CONDITIONS.get(x, x),
        )

    extra = [color_by] if color_by != "(nenhum)" else []

    # Validação: impedir que X e Y sejam iguais
    if x_axis == y_axis:
        st.error("❌ Os eixos X e Y não podem ser a mesma coluna. Selecione colunas diferentes.")
    else:
        df_sc = df[[x_axis, y_axis] + extra].dropna(subset=[x_axis, y_axis])
        df_sc = df_sc.sample(min(3000, len(df_sc)), random_state=42)

        if color_by != "(nenhum)" and color_by in df_sc.columns:
            df_sc["Status"] = df_sc[color_by].apply(
                lambda x: CVD_CONDITIONS[color_by] if x else "Sem condição"
            )
            c_field = "Status"
            c_map   = {CVD_CONDITIONS[color_by]: C_RED, "Sem condição": C_BLUE}
        else:
            c_field = None
            c_map   = None

        fig = px.scatter(
            df_sc, x=x_axis, y=y_axis,
            color=c_field, color_discrete_map=c_map,
            opacity=0.45, trendline="lowess", template=TPLT,
            labels={x_axis: lbl(x_axis), y_axis: lbl(y_axis)},
        )
        fig.update_layout(height=450, margin=dict(l=0, r=0, t=10, b=0),
                          legend=dict(orientation="h", y=1.08))
        st.plotly_chart(fig, use_container_width=True)

        # Coeficiente de correlação
        corr_val = df[[x_axis, y_axis]].dropna().corr().iloc[0, 1]
        strength = (
            "muito fraca" if abs(corr_val) < 0.1 else
            "fraca"       if abs(corr_val) < 0.3 else
            "moderada"    if abs(corr_val) < 0.5 else
            "forte"       if abs(corr_val) < 0.7 else
            "muito forte"
        )
        direction = "positiva" if corr_val >= 0 else "negativa"
        st.info(
            f"Correlação de Pearson entre **{lbl(x_axis)}** e **{lbl(y_axis)}**: "
            f"**{corr_val:.4f}** — correlação **{strength} {direction}**."
        )


def _rfmt(v: float) -> str:
    """Formata um float sem notação científica, com casas decimais adequadas à magnitude."""
    a = abs(v)
    if a >= 1000:  return f"{v:,.0f}"
    if a >= 100:   return f"{v:.1f}"
    if a >= 10:    return f"{v:.2f}"
    if a >= 1:     return f"{v:.3f}"
    return f"{v:.4f}"


# ── Aba 6: Referências Clínicas ───────────────────────────────────────────────
with tab6:
    st.markdown("### 🩸 Comparação com Valores de Referência")
    st.caption(
        "Compara o **valor médio da população NHANES** (aplicando os filtros ativos) com "
        "intervalos de referência clínicos e de ingestão diária recomendada (IDR). "
        "Uso educacional — não substitui avaliação médica individualizada."
    )
    st.divider()

    _col_to_group = {
        col: grp for grp, cols in REF_GROUPS.items() for col in cols
    }
    _ref_cols = [
        col for cols in REF_GROUPS.values()
        for col in cols
        if col in REFERENCE_VALUES and col in df.columns
    ]

    col_sel, _ = st.columns([2, 2])
    with col_sel:
        sel_ref = st.selectbox(
            "Selecione o indicador",
            _ref_cols,
            format_func=lambda c: f"{_col_to_group.get(c, '')}  ·  {lbl(c)}",
            key="ref_sel",
        )

    ref      = REFERENCE_VALUES[sel_ref]
    ref_min  = ref["ref_min"]
    ref_max  = ref["ref_max"]
    col_data = df[sel_ref].dropna()
    mean_val = float(col_data.mean())
    med_val  = float(col_data.median())

    # ── Status ────────────────────────────────────────────────────────────────
    if ref_min is not None and mean_val < ref_min:
        status = "baixo"
    elif ref_max is not None and mean_val > ref_max:
        status = "alto"
    else:
        status = "normal"

    # ── % fora do intervalo ───────────────────────────────────────────────────
    if ref_min is not None and ref_max is not None:
        pct_out = float(((col_data < ref_min) | (col_data > ref_max)).mean() * 100)
    elif ref_max is not None:
        pct_out = float((col_data > ref_max).mean() * 100)
    elif ref_min is not None:
        pct_out = float((col_data < ref_min).mean() * 100)
    else:
        pct_out = 0.0

    # ── Métricas ──────────────────────────────────────────────────────────────
    if ref_min is not None and ref_max is not None:
        ref_str = f"{_rfmt(ref_min)} – {_rfmt(ref_max)}"
    elif ref_max is not None:
        ref_str = f"< {_rfmt(ref_max)}"
    else:
        ref_str = f"≥ {_rfmt(ref_min)}"

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Média (dataset)", _rfmt(mean_val))
    m2.metric("Mediana (dataset)", _rfmt(med_val))
    m3.metric("Intervalo de referência", ref_str)
    m4.metric("Fora do intervalo", f"{pct_out:.1f}%")

    # ── Gauge ─────────────────────────────────────────────────────────────────
    p5  = float(col_data.quantile(0.05))
    p95 = float(col_data.quantile(0.95))

    g_candidates_min = [p5 * 0.8]
    if ref_min is not None:
        g_candidates_min.append(ref_min * 0.5)
    g_min = max(0.0, min(g_candidates_min))

    g_candidates_max = [p95 * 1.2, mean_val * 1.1]
    if ref_max is not None:
        g_candidates_max.append(ref_max * 1.3)
    if ref_min is not None:
        g_candidates_max.append(ref_min * 2.0)
    g_max = max(g_candidates_max)

    bar_color = C_GRN if status == "normal" else (C_AMB if status == "baixo" else C_RED)

    if ref_min is not None and ref_max is not None:
        gauge_steps = [
            {"range": [g_min, ref_min], "color": "#FEE2E2"},
            {"range": [ref_min, ref_max], "color": "#D1FAE5"},
            {"range": [ref_max, g_max], "color": "#FEE2E2"},
        ]
    elif ref_max is not None:
        gauge_steps = [
            {"range": [g_min, ref_max], "color": "#D1FAE5"},
            {"range": [ref_max, g_max], "color": "#FEE2E2"},
        ]
    else:
        gauge_steps = [
            {"range": [g_min, ref_min], "color": "#FEE2E2"},
            {"range": [ref_min, g_max], "color": "#D1FAE5"},
        ]

    _gauge_fmt = ",.0f" if mean_val >= 100 else (".1f" if mean_val >= 10 else ".3f")

    fig_ref = go.Figure(go.Indicator(
        mode="gauge+number",
        value=mean_val,
        title={"text": lbl(sel_ref), "font": {"size": 15}},
        number={"font": {"size": 32}, "valueformat": _gauge_fmt},
        gauge={
            "axis": {"range": [g_min, g_max], "tickfont": {"size": 11}},
            "bar": {"color": bar_color, "thickness": 0.28},
            "steps": gauge_steps,
            "threshold": {
                "line": {"color": bar_color, "width": 4},
                "thickness": 0.75,
                "value": mean_val,
            },
        },
    ))
    fig_ref.update_layout(height=270, margin={"t": 60, "b": 10, "l": 30, "r": 30}, template=TPLT)
    st.plotly_chart(fig_ref, use_container_width=True)

    st.caption(f"Tipo: **{ref['tipo']}** · Fonte: **{ref['fonte']}**")
    st.divider()

    # ── Interpretação clínica ─────────────────────────────────────────────────
    if status == "normal":
        st.success(
            f"✅ **Dentro do intervalo de referência.** "
            f"O valor médio da população filtrada ({_rfmt(mean_val)}) está dentro do intervalo "
            f"considerado normal ({ref_str})."
        )
    elif status == "baixo":
        st.warning(
            f"⬇ **Abaixo do intervalo de referência.** "
            f"O valor médio da população filtrada ({_rfmt(mean_val)}) está abaixo do mínimo "
            f"recomendado ({_rfmt(ref_min)})."
        )
    else:
        st.error(
            f"⬆ **Acima do intervalo de referência.** "
            f"O valor médio da população filtrada ({_rfmt(mean_val)}) está acima do máximo "
            f"recomendado ({_rfmt(ref_max)})."
        )

    if ref.get("msg_baixo"):
        with st.expander("⬇ O que significa estar baixo neste indicador?",
                         expanded=(status == "baixo")):
            st.markdown(ref["msg_baixo"])

    if ref.get("msg_alto"):
        with st.expander("⬆ O que significa estar alto neste indicador?",
                         expanded=(status == "alto")):
            st.markdown(ref["msg_alto"])


# ── Rodapé ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<center><small style='color:#6B7280'>"
    "MedBoard &nbsp;·&nbsp; "
    "<a href='https://github.com/DiegoRockenbach' target='_blank'>Diego Rockenbach</a>"
    " &amp; "
    "<a href='https://github.com/lucasaued' target='_blank'>Lucas Aued</a>"
    " &nbsp;·&nbsp; UFSM"
    "</small></center>",
    unsafe_allow_html=True,
)
