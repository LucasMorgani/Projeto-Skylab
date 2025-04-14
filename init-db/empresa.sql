-- init-db/empresa.sql
DO $$
BEGIN
    -- Criação do banco se não existir
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'Empresa') THEN
        CREATE DATABASE Empresa;
    END IF;
END $$;

\c Empresa

-- Tabelas com IF NOT EXISTS
CREATE TABLE IF NOT EXISTS Departamento (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Cargo (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Funcionario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cargo_id INT NOT NULL,
    departamento_id INT NOT NULL,
    FOREIGN KEY (cargo_id) REFERENCES Cargo(id) ON DELETE CASCADE,
    FOREIGN KEY (departamento_id) REFERENCES Departamento(id) ON DELETE CASCADE
);

-- Inserções iniciais condicionais
INSERT INTO Departamento (nome) VALUES 
('TI'), 
('RH'), 
('Financeiro'), 
('Marketing'), 
('Vendas')
ON CONFLICT (nome) DO NOTHING;

INSERT INTO Cargo (nome) VALUES 
('Analista de Sistemas'), 
('Gerente de TI'), 
('Gerente de RH'), 
('Analista de Marketing'), 
('Coordenador de Vendas'),
('Assistente de TI')
ON CONFLICT (nome) DO NOTHING;