-- Tabelle principali
CREATE TABLE Docente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE Studente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE ClasseVirtuale (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50) NOT NULL,
    materia VARCHAR(50) NOT NULL,
    codice_iscrizione VARCHAR(20) NOT NULL UNIQUE,
    docente_id INTEGER NOT NULL,
    FOREIGN KEY (docente_id) REFERENCES Docente(id)
);

CREATE TABLE Videogioco (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titolo VARCHAR(100) NOT NULL,
    descrizione_breve VARCHAR(160) NOT NULL CHECK (LENGTH(descrizione_breve) <= 160),
    descrizione_estesa TEXT NOT NULL,
    monete_totali INTEGER NOT NULL CHECK (monete_totali > 0),
    immagine1 VARCHAR(255) NOT NULL,
    immagine2 VARCHAR(255),
    immagine3 VARCHAR(255),
    argomento_id INTEGER NOT NULL,
    FOREIGN KEY (argomento_id) REFERENCES Argomento(id)
);

CREATE TABLE Argomento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50) NOT NULL UNIQUE
);

-- Tabelle di relazione
CREATE TABLE Iscrizione (
    studente_id INTEGER,
    classe_id INTEGER,
    PRIMARY KEY (studente_id, classe_id),
    FOREIGN KEY (studente_id) REFERENCES Studente(id),
    FOREIGN KEY (classe_id) REFERENCES ClasseVirtuale(id)
);

CREATE TABLE VideogiochiClasse (
    classe_id INTEGER,
    videogioco_id INTEGER,
    PRIMARY KEY (classe_id, videogioco_id),
    FOREIGN KEY (classe_id) REFERENCES ClasseVirtuale(id),
    FOREIGN KEY (videogioco_id) REFERENCES Videogioco(id)
);

CREATE TABLE ProgressoStudente (
    studente_id INTEGER,
    videogioco_id INTEGER,
    monete_raccolte INTEGER NOT NULL DEFAULT 0 CHECK (monete_raccolte >= 0),
    PRIMARY KEY (studente_id, videogioco_id),
    FOREIGN KEY (studente_id) REFERENCES Studente(id),
    FOREIGN KEY (videogioco_id) REFERENCES Videogioco(id)
);
