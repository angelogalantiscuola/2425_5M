CREATE TABLE CAMERA (
    numero INT PRIMARY KEY,
    tipo VARCHAR(50),
    disponibile BOOLEAN,
    prezzo INT,
    numero_posti INT
);

CREATE TABLE PRENOTAZIONE (
    id INT PRIMARY KEY,
    data_arrivo DATE,
    data_partenza DATE,
    nome_cliente VARCHAR(100)
);

CREATE TABLE CAMERAPRENOTAZIONE (
    id_camera INT,
    id_prenotazione INT,
    PRIMARY KEY (id_camera, id_prenotazione),
    FOREIGN KEY (id_camera) REFERENCES CAMERA(numero),
    FOREIGN KEY (id_prenotazione) REFERENCES PRENOTAZIONE(id)
);

-- Insert mock data
INSERT INTO CAMERA (numero, tipo, disponibile, prezzo, numero_posti) VALUES
(101, 'Singola', TRUE, 50, 1),
(102, 'Doppia', TRUE, 80, 2),
(103, 'Suite', FALSE, 150, 4);

INSERT INTO PRENOTAZIONE (id, data_arrivo, data_partenza, nome_cliente) VALUES
(1, '2023-10-01', '2023-10-05', 'Mario Rossi'),
(2, '2023-10-10', '2023-10-15', 'Luigi Bianchi');

INSERT INTO CAMERAPRENOTAZIONE (id_camera, id_prenotazione) VALUES
(101, 1),
(102, 2);