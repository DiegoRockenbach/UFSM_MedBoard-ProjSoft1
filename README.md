# UFSM_MedBoard-ProjSoft1

Projeto de Software 1 com Lucas Aued ministrado pelo prof Joaquim UFSM

---

## MedBoard — Dashboard de Saúde NHANES

Plataforma web para visualização e análise de dados de saúde cardiovascular do
dataset **NHANES** (National Health and Nutrition Examination Survey),
com 27.493 registros e 46 variáveis clínicas e nutricionais.

### Funcionalidades

- **Visão Geral** — KPIs populacionais, distribuições de idade/IMC, prevalência de doenças cardiovasculares
- **Explorar Dados** — Tabela paginada, ordenável, filtrável e exportável em CSV
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

# 2. Criar e ativar ambiente virtual
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt
```

---

## Configuração do Supabase (opcional)

O sistema funciona **sem Supabase** — sem configuração, os dados são lidos
diretamente do CSV local. Para usar o Supabase:

1. Crie um projeto em https://app.supabase.com
2. Execute o script `schema.sql` no **SQL Editor** do Supabase
3. Copie `.env.example` para `.env` e preencha as credenciais:

```bash
cp .env.example .env
# edite .env com sua URL e chave do projeto
```

4. Importe os dados:

```bash
python scripts/import_data.py
```

---

## Executar o Dashboard

```bash
streamlit run app/main.py
```

Acesse http://localhost:8501 no navegador.

---

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
