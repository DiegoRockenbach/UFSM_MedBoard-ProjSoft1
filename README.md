# UFSM_MedBoard-ProjSoft1

Software desenvolvido na disciplina 'Projeto de Software 1', realizada no sexto semestre da faculdade de 'Sistemas de Informação', na UFSM.
A cadeira foi ministrada pelo professor Joaquim V. C. Assunção, e o projeto foi desenvolvido em conjunto com Lucas Aued.

---

## MedBoard — Dashboard de Saúde UFSM

Plataforma web para visualização e análise de dados de saúde cardiovascular do
dataset **NHANES** (National Health and Nutrition Examination Survey),
com 27.493 registros e 46 variáveis clínicas e nutricionais.

### Funcionalidades

- **Explorar Dados** — Tabela paginada, ordenável, filtrável e exportável em CSV
- **Visão Geral** — KPIs populacionais, distribuições de idade/IMC, prevalência de doenças cardiovasculares
- **Nutrição** — Box plots e violinos por categoria (macronutrientes, vitaminas, minerais), comparação entre grupos CVD
- **Fatores de Risco** — Pressão arterial, IMC, colesterol e PCR estratificados por condição
- **Correlações** — Mapa de calor e dispersão interativa com linha de tendência

### Tecnologias

| Camada    | Tecnologia          |
|-----------|---------------------|
| Frontend  | Streamlit (Python)  |
| Backend   | Python 3.11+        |
| Banco     | Supabase (PostgreSQL)|
| Gráficos  | Plotly Express      |
| Dados     | Pandas / NumPy      |

---

## Instalação

```bash
# 1. Clonar o repositório
git clone <url-do-repo>
cd UFSM_MedBoard-ProjSoft1

# 2. Instalar dependências
pip install -r requirements.txt
```

---

## Executar o Dashboard

```bash
streamlit run app/main.py
```

## Estrutura do Projeto

```
UFSM_MedBoard-ProjSoft1/
├── app/
│   ├── main.py          # Dashboard Streamlit (frontend + lógica)
│   └── database.py      # Camada de dados (Supabase + fallback CSV)
├── scripts/
│   └── import_data.py   # Importação CSV → Supabase (uso único)
├── Dataset/
│   └── Nhanes_cvd_raw.csv
├── schema.sql            # DDL da tabela Supabase
├── requirements.txt
├── .env.example
└── README.md
```
