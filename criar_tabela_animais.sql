
CREATE TABLE IF NOT EXISTS animais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    especie TEXT,
    idade TEXT,
    sexo TEXT,
    observacoes TEXT,
    disponivel INTEGER DEFAULT 1
);
