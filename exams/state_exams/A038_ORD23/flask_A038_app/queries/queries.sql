-- Get all games
SELECT v.*, a.nome as argomento
FROM Videogioco v
JOIN Argomento a ON v.argomento_id = a.id
ORDER BY v.titolo;

-- Get game details
SELECT v.*, a.nome as argomento
FROM Videogioco v
JOIN Argomento a ON v.argomento_id = a.id
WHERE v.id = :game_id;

-- Get game leaderboard
SELECT s.nome, s.cognome, ps.monete_raccolte
FROM Studente s
JOIN ProgressoStudente ps ON s.id = ps.studente_id
WHERE ps.videogioco_id = :game_id
ORDER BY ps.monete_raccolte DESC
LIMIT 10;