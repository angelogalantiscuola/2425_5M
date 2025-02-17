# Piattaforma Giochi Educativi

Una semplice applicazione Flask per gestire una piattaforma di giochi educativi.

## Requisiti

- Python 3.8 o superiore
- Flask 3.0.0
- SQLite3

## Installazione

1. Clona il repository o scarica i file

2. Crea un ambiente virtuale e attivalo:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# oppure
.venv\Scripts\activate     # Windows
```

3. Installa le dipendenze:

```bash
pip install -r requirements.txt
```

## Esecuzione

Per avviare l'applicazione:

```bash
python app.py
```

L'applicazione sarà disponibile all'indirizzo `http://localhost:5000`

## Struttura del Progetto

```
soluzione_A038_app/
├── app.py              # Applicazione Flask principale
├── requirements.txt    # Dipendenze del progetto
├── README.md          # Questo file
├── queries/           # Query SQL e utility
│   ├── queries.py     # QueryLoader e definizioni query
│   ├── schema.sql     # Schema del database
│   ├── data.sql       # Dati di esempio
│   └── queries.sql    # Query SQL principali
├── static/            # File statici (CSS, immagini)
└── templates/         # Template HTML
    ├── base.html      # Template base
    ├── giochi.html    # Lista dei giochi
    └── gioco.html     # Dettaglio del gioco
```

## Sistema di Query

L'applicazione utilizza un sistema di query SQL modulare:

- Le query sono definite in file .sql separati nella cartella `queries/`
- Ogni query è identificata da un commento SQL che ne definisce il nome
- Il `QueryLoader` carica dinamicamente le query dai file .sql
- Le query possono essere richiamate per nome usando `QUERIES.get("nome_query")`

## Funzionalità Implementate

- Visualizzazione catalogo giochi
- Dettaglio singolo gioco
- Classifica studenti per gioco
- Database SQLite con dati di esempio

## Note per lo Sviluppo

- Il database viene creato automaticamente al primo avvio
- Sono inseriti alcuni dati di esempio
- L'applicazione è in modalità debug per lo sviluppo
