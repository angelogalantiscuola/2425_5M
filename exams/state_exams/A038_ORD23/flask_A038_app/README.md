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
├── schema.sql         # Schema del database
├── static/            # File statici (CSS, immagini)
└── templates/         # Template HTML
    ├── base.html      # Template base
    ├── giochi.html    # Lista dei giochi
    └── gioco.html     # Dettaglio del gioco
```

## Funzionalità Implementate

- Visualizzazione catalogo giochi
- Dettaglio singolo gioco
- Classifica studenti per gioco
- Database SQLite con dati di esempio

## Note per lo Sviluppo

- Il database viene creato automaticamente al primo avvio
- Sono inseriti alcuni dati di esempio
- L'applicazione è in modalità debug per lo sviluppo
