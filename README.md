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
- **Fatores de Risco** — Pressão arterial, IMC, colesterol e PCR estratificados por condição cardiovascular
- **Correlações** — Mapa de calor e dispersão interativa com linha de tendência
- **Ref. Clínicas** — Comparação do valor médio da população com intervalos de referência clínicos e IDR (ingestão diária recomendada)

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

Antes de rodar o dashboard localmente, crie o arquivo `.env` a partir do modelo `.env.example`.

No Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

No macOS/Linux:

```bash
cp .env.example .env
```

---

## Executar o Dashboard

```bash
python -m streamlit run app/main.py
```

## Estrutura do Projeto

```
UFSM_MedBoard-ProjSoft1/
├── app/
│   ├── main.py           # Dashboard Streamlit (frontend + lógica)
│   ├── database.py       # Camada de dados (Supabase)
│   └── nhanes_mapping.py # Mapeamento de colunas CSV → banco
├── scripts/
│   └── import_data.py    # Importação CSV → Supabase (uso único)
├── Dataset/
│   └── Nhanes_cvd_raw.csv  # Dataset original (apenas fallback local)
├── schema.sql            # DDL da tabela Supabase
├── requirements.txt
├── .env.example
└── README.md
```
