# Database Schema - Calcio

```mermaid
erDiagram
    ALLENATORE {
        int id PK
        varchar nome
        varchar cognome
    }
    GIOCATORE {
        int id PK
        varchar nome
        varchar cognome
        varchar ruolo
        int allenatore_id FK
    }
    PARTITA {
        int id PK
        date data
    }
    GIOCATORE_PARTITA {
        int partita_id PK,FK
        int giocatore_id PK,FK
        boolean ha_segnato
    }

    ALLENATORE ||--o{ GIOCATORE : allena
    GIOCATORE ||--o{ GIOCATORE_PARTITA : partecipa
    PARTITA ||--o{ GIOCATORE_PARTITA : include
```

The diagram shows the relationships between the tables:
- One ALLENATORE can coach zero or many GIOCATORE (1:N)
- One GIOCATORE can participate in zero or many PARTITA through GIOCATORE_PARTITA (N:M)
- One PARTITA involves multiple GIOCATORE through GIOCATORE_PARTITA
