-- ============================================================
-- MedBoard – Schema Supabase/PostgreSQL
-- Execute no SQL Editor do Supabase antes de importar os dados
-- ============================================================

CREATE TABLE IF NOT EXISTS nhanes_cvd (
    seqn BIGINT PRIMARY KEY,

    -- Macronutrientes (g/dia)
    protein              FLOAT,
    carbohydrates        FLOAT,
    sugars               FLOAT,
    fiber                FLOAT,
    saturated_fat        FLOAT,
    monounsaturated_fat  FLOAT,
    polyunsaturated_fat  FLOAT,
    cholesterol          FLOAT,

    -- Vitaminas
    beta_carotene        FLOAT,
    cryptoxanthin        FLOAT,
    lutein_zeaxanthin    FLOAT,
    thiamin              FLOAT,
    riboflavin           FLOAT,
    niacin               FLOAT,
    vitamin_b6           FLOAT,
    folic_acid           FLOAT,
    food_folate          FLOAT,
    folate_dfe           FLOAT,
    vitamin_b12          FLOAT,
    vitamin_c            FLOAT,
    vitamin_d            FLOAT,
    vitamin_e            FLOAT,
    vitamin_k            FLOAT,

    -- Minerais
    -- Ausente no CSV atual: o campo chamado "Iron" no arquivo local e folato DFE.
    iron                 FLOAT,
    choline              FLOAT,
    calcium              FLOAT,
    phosphorus           FLOAT,
    magnesium            FLOAT,
    zinc                 FLOAT,
    copper               FLOAT,
    sodium               FLOAT,
    potassium            FLOAT,
    selenium             FLOAT,

    -- Outros nutrientes
    theobromine          FLOAT,
    moisture             FLOAT,

    -- Condições cardiovasculares (TRUE = possui a condição)
    congestive           BOOLEAN,
    coronary             BOOLEAN,
    heart_attack         BOOLEAN,
    stroke               BOOLEAN,
    angina               BOOLEAN,

    -- Dados demográficos e clínicos
    age                  INTEGER,
    bmi                  FLOAT,
    waist_circ           FLOAT,
    systolic_bp          FLOAT,
    diastolic_bp         FLOAT,
    total_cholesterol    FLOAT,
    c_reactive           FLOAT,

    created_at           TIMESTAMPTZ DEFAULT NOW()
);

-- Migracao para bancos ja criados antes da correcao do cabecalho "Iron" no CSV.
ALTER TABLE nhanes_cvd
    ADD COLUMN IF NOT EXISTS folate_dfe FLOAT;

UPDATE nhanes_cvd
SET folate_dfe = iron,
    iron = NULL
WHERE folate_dfe IS NULL
  AND iron > 100;

-- Row Level Security
ALTER TABLE nhanes_cvd ENABLE ROW LEVEL SECURITY;

-- Leitura pública (necessário para o dashboard)
CREATE POLICY "Leitura pública" ON nhanes_cvd
    FOR SELECT USING (true);

-- Índices para filtros comuns
CREATE INDEX IF NOT EXISTS idx_nhanes_age           ON nhanes_cvd (age);
CREATE INDEX IF NOT EXISTS idx_nhanes_bmi           ON nhanes_cvd (bmi);
CREATE INDEX IF NOT EXISTS idx_nhanes_congestive    ON nhanes_cvd (congestive);
CREATE INDEX IF NOT EXISTS idx_nhanes_coronary      ON nhanes_cvd (coronary);
CREATE INDEX IF NOT EXISTS idx_nhanes_heart_attack  ON nhanes_cvd (heart_attack);
CREATE INDEX IF NOT EXISTS idx_nhanes_stroke        ON nhanes_cvd (stroke);
CREATE INDEX IF NOT EXISTS idx_nhanes_angina        ON nhanes_cvd (angina);
