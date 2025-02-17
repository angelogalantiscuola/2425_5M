-- Creazione della tabella TipologiaMiele
CREATE TABLE TipologiaMiele (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50) NOT NULL UNIQUE
);

-- Creazione della tabella Miele
CREATE TABLE Miele (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    denominazione VARCHAR(100) NOT NULL UNIQUE,
    tipologia_id INTEGER NOT NULL,
    FOREIGN KEY (tipologia_id) REFERENCES TipologiaMiele(id)
);

-- Creazione della tabella Apicoltore
CREATE TABLE Apicoltore (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Creazione della tabella Apiario
CREATE TABLE Apiario (
    codice VARCHAR(20) PRIMARY KEY,
    numero_arnie INTEGER NOT NULL CHECK (numero_arnie > 0),
    localita VARCHAR(100) NOT NULL,
    comune VARCHAR(100) NOT NULL,
    provincia VARCHAR(2) NOT NULL,
    regione VARCHAR(50) NOT NULL,
    anno INTEGER NOT NULL,
    quantita_prodotta FLOAT NOT NULL CHECK (quantita_prodotta >= 0),
    apicoltore_id INTEGER NOT NULL,
    miele_id INTEGER NOT NULL,
    FOREIGN KEY (apicoltore_id) REFERENCES Apicoltore(id),
    FOREIGN KEY (miele_id) REFERENCES Miele(id)
);

-- Inserting data into TipologiaMiele
INSERT INTO TipologiaMiele (nome) VALUES
    ('Millefiori'),
    ('Acacia'),
    ('Castagno'),
    ('Tiglio'),
    ('Eucalipto');

-- Inserting data into Miele
INSERT INTO Miele (denominazione, tipologia_id) VALUES
    ('Miele Millefiori Alpino', 1),
    ('Miele di Acacia della Toscana', 2),
    ('Miele di Castagno dell''Appennino', 3),
    ('Miele di Tiglio della Pianura Padana', 4),
    ('Miele di Eucalipto Siciliano', 5);

-- Inserting data into Apicoltore
INSERT INTO Apicoltore (nome, cognome, email, password) VALUES
    ('Marco', 'Rossi', 'marco.rossi@email.it', 'hashed_password_1'),
    ('Laura', 'Bianchi', 'laura.bianchi@email.it', 'hashed_password_2'),
    ('Giuseppe', 'Verdi', 'giuseppe.verdi@email.it', 'hashed_password_3'),
    ('Anna', 'Ferrari', 'anna.ferrari@email.it', 'hashed_password_4'),
    ('Paolo', 'Romano', 'paolo.romano@email.it', 'hashed_password_5');

-- Inserting data into Apiario
INSERT INTO Apiario (codice, numero_arnie, localita, comune, provincia, regione, anno, quantita_prodotta, apicoltore_id, miele_id) VALUES
    ('API001', 25, 'Valle Verde', 'Siena', 'SI', 'Toscana', 2024, 750.5, 1, 2),
    ('API002', 15, 'Monte Alto', 'Bologna', 'BO', 'Emilia-Romagna', 2024, 450.0, 2, 3),
    ('API003', 30, 'Piana dei Fiori', 'Palermo', 'PA', 'Sicilia', 2024, 900.0, 3, 5),
    ('API004', 20, 'Colle Sereno', 'Trento', 'TN', 'Trentino-Alto Adige', 2024, 600.0, 4, 1),
    ('API005', 18, 'Valle degli Ulivi', 'Lucca', 'LU', 'Toscana', 2024, 540.0, 5, 2);