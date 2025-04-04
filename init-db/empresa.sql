-- Criação do banco de dados
CREATE DATABASE Empresa;
\c Empresa;

-- Criação da tabela Departamento
CREATE TABLE Departamento (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

-- Criação da tabela Cargo
CREATE TABLE Cargo (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

-- Criação da tabela Funcionario
CREATE TABLE Funcionario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cargo_id INT NOT NULL,
    departamento_id INT NOT NULL,
    FOREIGN KEY (cargo_id) REFERENCES Cargo(id) ON DELETE CASCADE,
    FOREIGN KEY (departamento_id) REFERENCES Departamento(id) ON DELETE CASCADE
);
-- Populando a tabela Departamento
INSERT INTO Departamento (nome) VALUES 
('TI'), 
('RH'), 
('Financeiro'), 
('Marketing'), 
('Vendas');

-- Populando a tabela Cargo
INSERT INTO Cargo (nome) VALUES 
('Analista de Sistemas'), 
('Gerente de TI'), 
('Gerente de RH'), 
('Analista de Marketing'), 
('Coordenador de Vendas'),
('Assistente de TI');

-- Populando a tabela Funcionario
INSERT INTO Funcionario (nome, cargo_id, departamento_id) VALUES 
('Lucas Morgani', 1, 1),          -- Analista de Sistemas, TI
('Ana Souza', 2, 2),              -- Gerente de TI, RH
('Marcos Pereira', 3, 1),         -- Gerente de RH, TI
('Julia Costa', 4, 4),            -- Analista de Marketing, Marketing
('Carlos Silva', 5, 5),           -- Coordenador de Vendas, Vendas
('Rafael Santos', 6, 1),          -- Assistente de TI, TI
('Andre Luiz', 6, 1);          -- Assistente de TI, TI

-- Consultar todos os funcionários com cargos e departamentos
SELECT f.id, f.nome, c.nome AS cargo, d.nome AS departamento
FROM Funcionario f
JOIN Cargo c ON f.cargo_id = c.id
JOIN Departamento d ON f.departamento_id = d.id;
