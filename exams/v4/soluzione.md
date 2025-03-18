## Esercizio

### Testo

L'amministrazione di diverse strutture sanitarie necessita di un sistema per gestire le informazioni. Nel sistema devono essere registrati i dati principali della struttura come denominazione e ubicazione. La struttura è organizzata in diverse aree specialistiche, ognuna con un proprio codice identificativo. Il personale è composto da medici specialisti e infermieri che prestano servizio nelle varie aree. Ogni membro del personale, sia esso medico o infermiere, viene identificato univocamente ed è caratterizzato dalla propria qualifica professionale. I medici hanno anche una specializzazione specifica.

I degenti vengono registrati con le loro generalità anagrafiche e lo stato di salute attuale. Per il ricovero, i pazienti vengono assegnati a delle camere, ciascuna contraddistinta da un numero e dalla tipologia di degenza. Durante la loro permanenza, i degenti ricevono assistenza sia dai medici che dagli infermieri delle diverse aree.

La struttura offre anche un servizio mensa per i visitatori e dispone di un ampio parcheggio. Le camere possono accogliere più persone contemporaneamente, in base alla loro capienza. La struttura organizza periodicamente giornate informative aperte al pubblico.

### Compito

1. **Progettazione Concettuale:**

   - Crea un diagramma ER che rappresenti questo scenario.
   - Identifica le entità, gli attributi e le relazioni.
   - Specifica la cardinalità delle relazioni.
   - Analizza il testo e giustifica le tue scelte.

2. **Progettazione Logica:**

   - Traduci il diagramma ER in uno schema relazionale.
   - Definisci le tabelle e le colonne.
   - Individua le chiavi primarie (PK) e le chiavi esterne (FK) per mantenere l'integrità dei dati.

3. **Normalizzazione:**

   - Normalizza il modello logico del database per rispettare la Prima Forma Normale (1NF), la Seconda Forma Normale (2NF) e la Terza Forma Normale (3NF).

4. **Creazione delle Tabelle in SQL:**

   - Scrivi le istruzioni SQL per creare le tabelle normalizzate.

5. **Inserimento dei Dati in SQL:**
   - Scrivi le istruzioni SQL per inserire alcuni dati di esempio nelle tabelle create.

### Considerazioni sul testo dell'esercizio

### Modello ER

```mermaid
erDiagram
    OSPEDALE {
        int id PK
        String nome
        String indirizzo
    }

    REPARTO {
        String id PK
        String nome
    }
    PERSONALE {
        String id PK
        String nome
        String specializzazione
        String ruolo
    }
    PAZIENTE {
        String id PK
        String nome
        int eta
        String diagnosi
    }
    STANZA {
        String numero PK
        String tipo
    }

    OSPEDALE ||--o{ REPARTO : contiene
    REPARTO ||--o{ PERSONALE : ha
    PERSONALE }o--o{ PAZIENTE : cura
    STANZA ||--o{ PAZIENTE : ospita
```

### Progettazione Logica

Di seguito lo schema logico della base di dati, con le chiavi primarie sottolineate e le chiavi esterne indicate con FK:

- OSPEDALE(**id**, nome, indirizzo)
- REPARTO(**id**, nome, ospedale_id[FK])
- PERSONALE(**id**, nome, specializzazione, ruolo, reparto_id[FK])
- PAZIENTE(**id**, nome, eta, diagnosi, stanza_numero[FK], personale_id[FK])
- STANZA(**numero**, tipo)

### Normalizzazione

1. **Prima Forma Normale (1NF)**

   - Assicurarsi che ogni colonna contenga solo valori atomici e che ogni tabella abbia una chiave primaria.

2. **Seconda Forma Normale (2NF)**

   - Assicurarsi che tutte le colonne non chiave dipendano interamente dalla chiave primaria.

3. **Terza Forma Normale (3NF)**
   - Assicurarsi che tutte le colonne non chiave dipendano solo dalla chiave primaria e non da altre colonne non chiave.

### Creazione delle Tabelle in SQL

```sql
CREATE TABLE OSPEDALE (
    id INT PRIMARY KEY,
    nome VARCHAR(100),
    indirizzo VARCHAR(200)
);

CREATE TABLE REPARTO (
    id VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(100),
    ospedale_id INT,
    FOREIGN KEY (ospedale_id) REFERENCES OSPEDALE(id)
);

CREATE TABLE PERSONALE (
    id INT PRIMARY KEY,
    nome VARCHAR(100),
    specializzazione VARCHAR(100),
    ruolo VARCHAR(50),
    reparto_id VARCHAR(50),
    FOREIGN KEY (reparto_id) REFERENCES REPARTO(id)
);

CREATE TABLE PAZIENTE (
    id INT PRIMARY KEY,
    nome VARCHAR(100),
    eta INT,
    diagnosi VARCHAR(200),
    stanza_numero INT,
    personale_id INT,
    FOREIGN KEY (stanza_numero) REFERENCES STANZA(numero),
    FOREIGN KEY (personale_id) REFERENCES PERSONALE(id)
);

CREATE TABLE STANZA (
    numero INT PRIMARY KEY,
    tipo VARCHAR(50)
);
```

### Inserimento dei Dati in SQL

```sql
INSERT INTO OSPEDALE (id, nome, indirizzo) VALUES
(1, 'Ospedale Maggiore', 'Via Roma, 1'),
(2, 'Ospedale Civile', 'Piazza Italia, 10');

INSERT INTO REPARTO (id, nome, ospedale_id) VALUES
('cardio', 'Cardiologia', 1),
('neuro', 'Neurologia', 2);

INSERT INTO PERSONALE (id, nome, specializzazione, ruolo, reparto_id) VALUES
(1, 'Mario Rossi', 'Cardiologo', 'Medico', 'cardio'),
(2, 'Luigi Verdi', 'Neurologo', 'Medico', 'neuro');

INSERT INTO STANZA (numero, tipo) VALUES
(101, 'Singola'),
(102, 'Doppia');

INSERT INTO PAZIENTE (id, nome, eta, diagnosi, stanza_numero, personale_id) VALUES
(1, 'Giuseppe Bianchi', 70, 'Infarto', 101, 1),
(2, 'Anna Neri', 80, 'Ictus', 102, 2);
