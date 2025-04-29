
-- Cria a tabela de usuários, se não existir
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    tipo TEXT NOT NULL
);

-- Insere o usuário administrador padrão
INSERT OR IGNORE INTO usuarios (email, senha, tipo)
VALUES (
    'admin@admin.com',
    'pbkdf2:sha256:600000$5YkkY8xt7HvszIdk$ab15a72ae60747c981b5d00e88850b15946df36fda7d0a230d6bdf244e404bb4',
    'admin'
);
