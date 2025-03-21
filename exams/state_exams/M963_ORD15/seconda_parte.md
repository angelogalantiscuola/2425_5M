# Domande seconda parte

## Domanda 3

Si consideri la seguente tabella: 

Il candidato verifichi le proprietà di normalizzazione e proponga uno schema equivalente che 
rispetti la 3^ Forma Normale, motivando le scelte effettuate.

Cognome Nome Telefono Livello Tutor Tel-tutor Anticipo versato 
Verdi Luisa 345698741 avanzato Bianca 334563215 100 
Neri Enrico 348523698 avanzato Carlo 369852147 150 
Rosi Rosa 347532159 base Alessio 333214569 120 
Bianchi Paolo 341236547 base Carlo 369852147 150 
Rossi Mario 349567890 base Carlo 369852147 90 
Neri Enrico 348523698 complementi Dina 373564987 100

**Schema Proposto**

Informazioni sul tutor: Tel-tutor dipende funzionalmente da Tutor. Ciò significa che conoscere il nome del Tutor determina il Tel-tutor. Pertanto è necessario creare una tabella separata per le informazioni sul tutor.

La presenza di "Neri Enrico" con due tutor diversi crea un problema. Per gestire la possibilità che un candidato abbia più tutor, introduciamo una terza tabella di collegamento.

**Tabella Candidati:**

*   `Cognome` (VARCHAR)
*   `Nome` (VARCHAR)
*   `Telefono` (VARCHAR) - *Chiave primaria alternativa*
*   `Livello` (VARCHAR)
*   `Anticipo versato` (DECIMAL)
*   `PRIMARY KEY (Cognome, Nome)`

**Tabella Tutor:**

*   `TutorID` (INT) *(Chiave primaria)*
*   `Tutor` (VARCHAR)
*   `Tel-tutor` (VARCHAR)
*   `PRIMARY KEY (TutorID)`

**Tabella Candidati_Tutor (Tabella di collegamento):**

*   `Cognome` (VARCHAR)
*   `Nome` (VARCHAR)
*   `TutorID` (INT)
*   `PRIMARY KEY (Cognome, Nome, TutorID)`
*   `FOREIGN KEY (Cognome, Nome) REFERENCES Candidati(Cognome, Nome)`
*   `FOREIGN KEY (TutorID) REFERENCES Tutor(TutorID)`

**Spiegazione delle Modifiche**

1.  **Tabella di Collegamento:** La tabella `Candidati_Tutor` risolve la relazione molti-a-molti tra candidati e tutor. Ogni riga in questa tabella rappresenta l'associazione di un candidato a un tutor specifico.
2.  **Chiavi Esterne:** La tabella `Candidati_Tutor` ha due chiavi esterne: una che fa riferimento alla tabella `Candidati` (usando `Cognome` e `Nome`) e una che fa riferimento alla tabella `Tutor` (usando `TutorID`).
3.  **Chiave Primaria Composta:** La chiave primaria della tabella `Candidati_Tutor` è composta da `(Cognome, Nome, TutorID)`, garantendo che non ci siano duplicati per la stessa associazione candidato-tutor.

**Come Funziona con l'Esempio**

Per l'esempio fornito, la tabella `Candidati_Tutor` conterrebbe le seguenti righe per "Neri Enrico":

*   `Cognome: Neri, Nome: Enrico, TutorID: (ID di Carlo)`
*   `Cognome: Neri, Nome: Enrico, TutorID: (ID di Dina)`

Questo schema permette a "Neri Enrico" di essere associato a entrambi i tutor senza duplicare le informazioni del candidato nella tabella `Candidati`.