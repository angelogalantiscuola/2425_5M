-- Create tables
CREATE TABLE ALLENATORE (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL
);

CREATE TABLE SQUADRA (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    sede VARCHAR(100) NOT NULL,
    allenatore_id INTEGER,
    FOREIGN KEY (allenatore_id) REFERENCES ALLENATORE(id)
);

CREATE TABLE PARTITA (
    id INTEGER PRIMARY KEY,
    data DATE NOT NULL
);

CREATE TABLE SQUADRA_PARTITA (
    partita_id INTEGER,
    squadra_id INTEGER,
    goal_squadra INTEGER NOT NULL,
    PRIMARY KEY (partita_id, squadra_id),
    FOREIGN KEY (partita_id) REFERENCES PARTITA(id),
    FOREIGN KEY (squadra_id) REFERENCES SQUADRA(id)
);

-- Insert sample data
INSERT INTO ALLENATORE (id, nome, cognome) VALUES
(1, 'José', 'Mourinho'),
(2, 'Carlo', 'Ancelotti'),
(3, 'Pep', 'Guardiola');

INSERT INTO SQUADRA (id, nome, sede, allenatore_id) VALUES
(1, 'AS Roma', 'Roma', 1),
(2, 'Real Madrid', 'Madrid', 2),
(3, 'Manchester City', 'Manchester', 3);

INSERT INTO PARTITA (id, data) VALUES
(1, '2025-02-15'),
(2, '2025-02-20'),
(3, '2025-02-25');

INSERT INTO SQUADRA_PARTITA (partita_id, squadra_id, goal_squadra) VALUES
(1, 1, 2),
(1, 2, 1),
(2, 2, 3),
(2, 3, 2),
(3, 1, 1),
(3, 3, 1);