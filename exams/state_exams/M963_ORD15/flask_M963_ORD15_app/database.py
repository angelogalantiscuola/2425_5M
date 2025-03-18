import sqlite3
from flask import g

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('eventi_community.db')
        db.row_factory = sqlite3.Row
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def get_eventi_gia_svolti():
    db = get_db()
    query = """
        SELECT e.titolo, e.data, e.provincia, c.nome AS categoria
        FROM EVENTO e
        JOIN CATEGORIA c ON e.categoria_id = c.id
        WHERE e.data < CURRENT_DATE
        ORDER BY e.provincia ASC, e.data DESC
    """
    cursor = db.execute(query)
    eventi = [dict(row) for row in cursor.fetchall()]
    return eventi

def get_membri_senza_commenti():
    db = get_db()
    query = """
        SELECT m.id, m.nickname, m.nome, m.cognome
        FROM MEMBRO m
        WHERE m.id NOT IN (
            SELECT DISTINCT c.membro_id
            FROM COMMENTO c
        )
    """
    cursor = db.execute(query)
    membri = [dict(row) for row in cursor.fetchall()]
    return membri

def get_voto_medio_per_evento():
    db = get_db()
    query = """
        SELECT e.id, e.titolo, c.nome AS categoria,
               COALESCE(AVG(com.voto), 0) AS voto_medio
        FROM EVENTO e
        JOIN CATEGORIA c ON e.categoria_id = c.id
        LEFT JOIN COMMENTO com ON e.id = com.evento_id
        GROUP BY e.id
        ORDER BY c.nome, e.titolo
    """
    cursor = db.execute(query)
    eventi = [dict(row) for row in cursor.fetchall()]
    return eventi

def get_utente_con_piu_eventi():
    db = get_db()
    query = """
        SELECT m.id, m.nickname, m.nome, m.cognome, m.email, m.provincia, COUNT(e.id) AS num_eventi
        FROM MEMBRO m
        JOIN EVENTO e ON m.id = e.membro_id
        GROUP BY m.id
        ORDER BY num_eventi DESC
        LIMIT 1
    """
    cursor = db.execute(query)
    row = cursor.fetchone()
    utente = dict(row) if row else None
    return utente
