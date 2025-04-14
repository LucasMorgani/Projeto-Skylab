-- Criação do banco de dados
CREATE DATABASE Empresa;

\c Empresa;

-- =============================================
-- TABELAS PRINCIPAIS
-- =============================================

-- Tabela de departamentos
CREATE TABLE IF NOT EXISTS Departamento (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

-- Tabela de cargos
CREATE TABLE IF NOT EXISTS Cargo (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

-- Tabela de funcionários
CREATE TABLE IF NOT EXISTS Funcionario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cargo_id INT NOT NULL,
    departamento_id INT NOT NULL,
    aprovado BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (cargo_id) REFERENCES Cargo(id) ON DELETE CASCADE,
    FOREIGN KEY (departamento_id) REFERENCES Departamento(id) ON DELETE CASCADE
);

-- Tabela de usuários do sistema (unificada)
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    admin BOOLEAN NOT NULL DEFAULT FALSE,
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

-- =============================================
-- DADOS INICIAIS
-- =============================================

-- Departamentos
INSERT INTO Departamento (nome) VALUES 
('TI'), 
('RH'), 
('Financeiro'), 
('Marketing'), 
('Vendas');

-- Cargos
INSERT INTO Cargo (nome) VALUES 
('Analista de Sistemas'), 
('Gerente de TI'), 
('Gerente de RH'), 
('Analista de Marketing'), 
('Coordenador de Vendas'),
('Assistente de TI');

-- Funcionários
INSERT INTO Funcionario (nome, cargo_id, departamento_id, aprovado) VALUES 
('Lucas Morgani', 1, 1, TRUE),
('Ana Souza', 2, 2, TRUE),
('Marcos Pereira', 3, 1, TRUE),
('Julia Costa', 4, 4, TRUE),
('Carlos Silva', 5, 5, TRUE),
('Rafael Santos', 6, 1, TRUE),
('Andre Luiz', 6, 1, TRUE);

-- Usuário admin com senha "admin123" hasheada
INSERT INTO usuarios (username, password, admin, ativo) VALUES (
    'admin', 
    '$pbkdf2-sha256$260000$N9XUyRz3p0L1UeAod7xzHA$znJmAilFZDfTxKnvXAWmmlNHFtfkGJkGmkpVbIJprIY', 
    TRUE, 
    TRUE
);