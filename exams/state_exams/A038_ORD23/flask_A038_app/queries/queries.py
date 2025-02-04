# SQL query to get all games with their topics
GET_ALL_GAMES = """
    SELECT v.*, a.nome as argomento
    FROM Videogioco v
    JOIN Argomento a ON v.argomento_id = a.id
    ORDER BY v.titolo
"""

# SQL query to get specific game details
GET_GAME_DETAILS = """
    SELECT v.*, a.nome as argomento
    FROM Videogioco v
    JOIN Argomento a ON v.argomento_id = a.id
    WHERE v.id = ?
"""

# SQL query to get game leaderboard
GET_GAME_LEADERBOARD = """
    SELECT s.nome, s.cognome, ps.monete_raccolte
    FROM Studente s
    JOIN ProgressoStudente ps ON s.id = ps.studente_id
    WHERE ps.videogioco_id = ?
    ORDER BY ps.monete_raccolte DESC
    LIMIT 10
"""
