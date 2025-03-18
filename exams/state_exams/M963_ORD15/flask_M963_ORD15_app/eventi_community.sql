-- Creazione delle tabelle principali
CREATE TABLE MEMBRO (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nickname VARCHAR(50) NOT NULL UNIQUE,
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    provincia VARCHAR(2) NOT NULL
);

CREATE TABLE CATEGORIA (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50) NOT NULL UNIQUE,
    descrizione TEXT
);

CREATE TABLE EVENTO (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titolo VARCHAR(100) NOT NULL,
    data DATE NOT NULL,
    provincia VARCHAR(2) NOT NULL,
    membro_id INTEGER NOT NULL,
    categoria_id INTEGER NOT NULL,
    FOREIGN KEY (membro_id) REFERENCES MEMBRO(id),
    FOREIGN KEY (categoria_id) REFERENCES CATEGORIA(id)
);

CREATE TABLE ARTISTA (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE COMMENTO (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    testo TEXT NOT NULL,
    voto INTEGER NOT NULL CHECK (voto BETWEEN 1 AND 5),
    data_inserimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    membro_id INTEGER NOT NULL,
    evento_id INTEGER NOT NULL,
    FOREIGN KEY (membro_id) REFERENCES MEMBRO(id),
    FOREIGN KEY (evento_id) REFERENCES EVENTO(id)
);

-- Tabelle di relazione molti-a-molti
CREATE TABLE MEMBRO_CATEGORIA (
    membro_id INTEGER,
    categoria_id INTEGER,
    PRIMARY KEY (membro_id, categoria_id),
    FOREIGN KEY (membro_id) REFERENCES MEMBRO(id),
    FOREIGN KEY (categoria_id) REFERENCES CATEGORIA(id)
);

CREATE TABLE EVENTO_ARTISTA (
    evento_id INTEGER,
    artista_id INTEGER,
    PRIMARY KEY (evento_id, artista_id),
    FOREIGN KEY (evento_id) REFERENCES EVENTO(id),
    FOREIGN KEY (artista_id) REFERENCES ARTISTA(id)
);

-- Populating MEMBRO table
INSERT INTO MEMBRO (nickname, nome, cognome, email, password, provincia) VALUES
('Marco82', 'Marco', 'Rossi', 'marco.rossi@example.com', 'password123', 'RM'),
('LauraF', 'Laura', 'Ferrari', 'laura.ferrari@example.com', 'securePass', 'MI'),
('Alex91', 'Alessandro', 'Bianchi', 'alex.bianchi@example.com', 'al3xPass', 'NA');

-- Populating CATEGORIA table
INSERT INTO CATEGORIA (nome, descrizione) VALUES
('Concerto', 'Eventi musicali dal vivo'),
('Mostra', 'Esposizioni artistiche e culturali'),
('Teatro', 'Rappresentazioni teatrali di vario genere');

-- Populating EVENTO table
INSERT INTO EVENTO (titolo, data, provincia, membro_id, categoria_id) VALUES
('Concerto di Capodanno', '2024-12-31', 'RM', 1, 1),
('Mostra di Arte Moderna', '2025-01-15', 'MI', 2, 2),
('Romeo e Giulietta', '2025-02-14', 'NA', 1, 3);

-- Populating ARTISTA table
INSERT INTO ARTISTA (nome) VALUES
('The Kolors'),
('Uffizi Esposizioni'),
('William Shakespeare Company');

-- Populating COMMENTO table
INSERT INTO COMMENTO (testo, voto, membro_id, evento_id) VALUES
('Bellissimo concerto, atmosfera fantastica!', 5, 1, 1),
('Mostra interessante, ma un po'' affollata.', 4, 3, 1),
('Emozionante rappresentazione, attori bravissimi.', 5, 3, 3);

-- Populating MEMBRO_CATEGORIA table
INSERT INTO MEMBRO_CATEGORIA (membro_id, categoria_id) VALUES
(1, 1),
(2, 2),
(3, 3);

-- Populating EVENTO_ARTISTA table
INSERT INTO EVENTO_ARTISTA (evento_id, artista_id) VALUES
(1, 1),
(2, 2),
(3, 3);
