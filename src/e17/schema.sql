-- Creazione della tabella TELESCOPIO
CREATE TABLE TELESCOPIO (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL UNIQUE,
    posizione VARCHAR(255) NOT NULL,
    apertura FLOAT NOT NULL CHECK (apertura > 0),
    tipo VARCHAR(50) NOT NULL
);

-- Creazione della tabella CORPO_CELESTE
CREATE TABLE CORPO_CELESTE (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL UNIQUE,
    categoria VARCHAR(50) NOT NULL,
    magnitudine FLOAT NOT NULL,
    distanza_parsec FLOAT NOT NULL CHECK (distanza_parsec >= 0)
);

-- Creazione della tabella RICERCATORE
CREATE TABLE RICERCATORE (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    istituzione VARCHAR(150) NOT NULL,
    UNIQUE(nome, cognome)
);

-- Creazione della tabella OSSERVAZIONE
CREATE TABLE OSSERVAZIONE (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    durata_minuti FLOAT NOT NULL CHECK (durata_minuti > 0),
    condizioni_meteo VARCHAR(50) NOT NULL,
    note TEXT,
    telescopio_id INTEGER NOT NULL,
    corpo_celeste_id INTEGER NOT NULL,
    FOREIGN KEY (telescopio_id) REFERENCES TELESCOPIO(id),
    FOREIGN KEY (corpo_celeste_id) REFERENCES CORPO_CELESTE(id)
);

-- Creazione della tabella ponte per la relazione N:N tra RICERCATORE e OSSERVAZIONE
CREATE TABLE RICERCATORE_OSSERVAZIONE (
    ricercatore_id INTEGER,
    osservazione_id INTEGER,
    PRIMARY KEY (ricercatore_id, osservazione_id),
    FOREIGN KEY (ricercatore_id) REFERENCES RICERCATORE(id),
    FOREIGN KEY (osservazione_id) REFERENCES OSSERVAZIONE(id)
);

-- Inserimento dati nella tabella TELESCOPIO
INSERT INTO TELESCOPIO (id, nome, posizione, apertura, tipo) VALUES
(1, 'Very Large Telescope', 'Cerro Paranal, Cile', 8.2, 'Riflettore'),
(2, 'Hubble Space Telescope', 'Orbita terrestre', 2.4, 'Riflettore spaziale'),
(3, 'Arecibo', 'Puerto Rico', 305, 'Radiotelescopo'),
(4, 'Atacama Large Millimeter Array', 'Deserto di Atacama, Cile', 12, 'Interferometro'),
(5, 'Subaru Telescope', 'Mauna Kea, Hawaii', 8.2, 'Riflettore');

-- Inserimento dati nella tabella CORPO_CELESTE
INSERT INTO CORPO_CELESTE (id, nome, categoria, magnitudine, distanza_parsec) VALUES
(1, 'M87', 'Galassia', 8.6, 16800000),
(2, 'Proxima Centauri', 'Stella', 11.05, 1.3),
(3, 'Nebulosa di Orione', 'Nebulosa', 4.0, 412),
(4, 'Sagittarius A*', 'Buco nero', 0, 8178),
(5, 'Europa', 'Satellite', 5.29, 0.00425),
(6, 'Pulsar del Granchio', 'Pulsar', 16.0, 2000);

-- Inserimento dati nella tabella RICERCATORE
INSERT INTO RICERCATORE (id, nome, cognome, email, istituzione) VALUES
(1, 'Elena', 'Rossi', 'elena.rossi@astro.it', 'INAF'),
(2, 'John', 'Smith', 'jsmith@nasa.gov', 'NASA'),
(3, 'Maria', 'González', 'mgonzalez@eso.org', 'ESO'),
(4, 'Hiroshi', 'Nakamura', 'hnakamura@jaxa.jp', 'JAXA'),
(5, 'Sophie', 'Dubois', 'sdubois@esa.int', 'ESA');

-- Inserimento dati nella tabella OSSERVAZIONE
INSERT INTO OSSERVAZIONE (id, timestamp, durata_minuti, condizioni_meteo, note, telescopio_id, corpo_celeste_id) VALUES
(1, '2023-07-15 22:30:00', 120, 'Sereno', 'Ottima visibilità', 1, 1),
(2, '2023-08-02 20:15:00', 90, 'Poco nuvoloso', 'Interferenze minime', 2, 3),
(3, '2023-08-10 23:00:00', 180, 'Sereno', 'Immagini ad alta risoluzione ottenute', 5, 4),
(4, '2023-09-05 21:45:00', 150, 'Sereno', 'Osservazione di routine', 2, 2),
(5, '2023-09-20 04:30:00', 240, 'Sereno', 'Attività insolita rilevata', 3, 6),
(6, '2023-10-12 19:20:00', 100, 'Nuvoloso', 'Qualità osservazione compromessa', 4, 1),
(7, '2023-11-08 22:10:00', 135, 'Sereno', 'Nuovi dati sulla rotazione', 1, 5),
(8, '2023-12-01 23:50:00', 200, 'Sereno', 'Spettroscopia dettagliata completata', 5, 3);

-- Inserimento dati nella tabella ponte RICERCATORE_OSSERVAZIONE
INSERT INTO RICERCATORE_OSSERVAZIONE (ricercatore_id, osservazione_id) VALUES
(1, 1), -- Elena Rossi partecipa all'osservazione 1
(2, 1), -- John Smith partecipa all'osservazione 1
(3, 2), -- Maria González partecipa all'osservazione 2
(4, 3), -- Hiroshi Nakamura partecipa all'osservazione 3
(1, 4), -- Elena Rossi partecipa all'osservazione 4
(5, 4), -- Sophie Dubois partecipa all'osservazione 4
(2, 5), -- John Smith partecipa all'osservazione 5
(3, 6), -- Maria González partecipa all'osservazione 6
(5, 6), -- Sophie Dubois partecipa all'osservazione 6
(4, 7), -- Hiroshi Nakamura partecipa all'osservazione 7
(1, 7), -- Elena Rossi partecipa all'osservazione 7
(3, 8), -- Maria González partecipa all'osservazione 8
(5, 8); -- Sophie Dubois partecipa all'osservazione 8