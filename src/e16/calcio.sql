-- Create tables
CREATE TABLE ALLENATORE (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL
);

CREATE TABLE GIOCATORE (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    ruolo VARCHAR(20) NOT NULL,
    allenatore_id INTEGER,
    FOREIGN KEY (allenatore_id) REFERENCES ALLENATORE(id)
);

CREATE TABLE PARTITA (
    id INTEGER PRIMARY KEY,
    data DATE NOT NULL,
    squadra_casa VARCHAR(50) NOT NULL,
    squadra_ospite VARCHAR(50) NOT NULL
);

CREATE TABLE GIOCATORE_PARTITA (
    partita_id INTEGER,
    giocatore_id INTEGER,
    ha_segnato BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (partita_id, giocatore_id),
    FOREIGN KEY (partita_id) REFERENCES PARTITA(id),
    FOREIGN KEY (giocatore_id) REFERENCES GIOCATORE(id)
);

-- Insert sample data
INSERT INTO ALLENATORE (id, nome, cognome) VALUES
(1, 'José', 'Mourinho'),
(2, 'Carlo', 'Ancelotti'),
(3, 'Pep', 'Guardiola');

INSERT INTO GIOCATORE (id, nome, cognome, ruolo, allenatore_id) VALUES
(1, 'Paulo', 'Dybala', 'Attaccante', 1),
(2, 'Luka', 'Modric', 'Centrocampista', 2),
(3, 'Erling', 'Haaland', 'Attaccante', 3),
(4, 'Lorenzo', 'Pellegrini', 'Centrocampista', 1),
(5, 'Toni', 'Kroos', 'Centrocampista', 2),
(6, 'Kevin', 'De Bruyne', 'Centrocampista', 3);

INSERT INTO PARTITA (id, data, squadra_casa, squadra_ospite) VALUES
(1, '2025-02-15', 'Roma', 'Real Madrid'),
(2, '2025-02-20', 'Real Madrid', 'Manchester City'),
(3, '2025-02-25', 'Manchester City', 'Roma');

INSERT INTO GIOCATORE_PARTITA (partita_id, giocatore_id, ha_segnato) VALUES
(1, 1, TRUE),
(1, 2, FALSE),
(1, 3, TRUE),
(2, 2, TRUE),
(2, 4, FALSE),
(2, 5, TRUE),
(3, 1, TRUE),
(3, 6, TRUE);