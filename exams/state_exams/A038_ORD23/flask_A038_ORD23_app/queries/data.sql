-- Populate Docenti (Teachers)
INSERT INTO Docente (nome, cognome, email, password) VALUES
    ('Mario', 'Rossi', 'mario.rossi@scuola.it', 'password123'),
    ('Anna', 'Bianchi', 'anna.bianchi@scuola.it', 'password123'),
    ('Luigi', 'Verdi', 'luigi.verdi@scuola.it', 'password123');

-- Populate Studenti (Students)
INSERT INTO Studente (nome, cognome, email, password) VALUES
    ('Marco', 'Ferrari', 'marco.ferrari@studenti.it', 'student123'),
    ('Laura', 'Romano', 'laura.romano@studenti.it', 'student123'),
    ('Giuseppe', 'Colombo', 'giuseppe.colombo@studenti.it', 'student123'),
    ('Sofia', 'Ricci', 'sofia.ricci@studenti.it', 'student123'),
    ('Luca', 'Marino', 'luca.marino@studenti.it', 'student123');

-- Populate Argomenti (Topics)
INSERT INTO Argomento (nome) VALUES 
    ('Matematica'),
    ('Fisica'),
    ('Italiano'),
    ('Storia'),
    ('Geografia');

-- Populate Classi Virtuali (Virtual Classes)
INSERT INTO ClasseVirtuale (nome, materia, codice_iscrizione, docente_id) VALUES
    ('3A', 'Matematica', 'MATH3A2024', 1),
    ('3B', 'Fisica', 'PHYS3B2024', 2),
    ('4A', 'Italiano', 'ITA4A2024', 3);

-- Populate Videogiochi (Games)
INSERT INTO Videogioco (titolo, descrizione_breve, descrizione_estesa, monete_totali, immagine1, argomento_id) VALUES 
    ('Geometria Divertente', 'Impara i triangoli giocando', 'Un gioco educativo per imparare tutti i tipi di triangoli e le loro proprietà.', 100, '/static/images/geometria.jpg', 1),
    ('Le Leggi di Newton', 'Scopri la fisica attraverso il gioco', 'Esplora le leggi del movimento e della gravità in modo interattivo.', 150, '/static/images/fisica.jpg', 2),
    ('Grammatica in Gioco', 'Esercizi di grammatica interattivi', 'Migliora le tue competenze grammaticali attraverso sfide divertenti.', 120, '/static/images/grammatica.jpg', 3),
    ('Viaggio nel Tempo', 'Esplora la storia antica', 'Un avventura attraverso le civiltà del passato.', 200, '/static/images/storia.jpg', 4),
    ('GeoExplorer', 'Scopri il mondo giocando', 'Impara geografia esplorando continenti e culture.', 180, '/static/images/geografia.jpg', 5);

-- Populate Iscrizioni (Enrollments)
INSERT INTO Iscrizione (studente_id, classe_id) VALUES
    (1, 1), -- Marco in 3A Matematica
    (2, 1), -- Laura in 3A Matematica
    (3, 2), -- Giuseppe in 3B Fisica
    (4, 2), -- Sofia in 3B Fisica
    (5, 3); -- Luca in 4A Italiano

-- Populate Videogiochi nelle Classi (Games in Classes)
INSERT INTO VideogiochiClasse (classe_id, videogioco_id) VALUES
    (1, 1), -- Geometria Divertente in 3A
    (2, 2), -- Le Leggi di Newton in 3B
    (3, 3); -- Grammatica in Gioco in 4A

-- Populate Progressi degli Studenti (Student Progress)
INSERT INTO ProgressoStudente (studente_id, videogioco_id, monete_raccolte) VALUES
    (1, 1, 75),  -- Marco in Geometria Divertente
    (2, 1, 90),  -- Laura in Geometria Divertente
    (3, 2, 120), -- Giuseppe in Le Leggi di Newton
    (4, 2, 85),  -- Sofia in Le Leggi di Newton
    (5, 3, 100); -- Luca in Grammatica in Gioco
