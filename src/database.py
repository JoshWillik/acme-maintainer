import sqlite3
import settings

FETCH_TABLE_STATEMENT = """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
        AND name = ?;
"""

connection = None

tables = [
    ('Certificates', """
        CREATE TABLE Certificates (
            id INTEGER PRIMARY KEY,
            name VARCHAR(40),
            domains TEXT,
            first_created DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_updated DATETIME
        );
    """)
]

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def init():
    connection = sqlite3.connect(settings.DB_PATH, check_same_thread=False)
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    for name, create_statement in tables:
        if not table_exists(cursor, name):
            print('[db] Creating table', name)
            cursor.execute(create_statement)
    connection.commit()
    cursor.close()
    return connection

def table_exists(cursor, name):
    table = cursor.execute(FETCH_TABLE_STATEMENT, (name,)).fetchone()
    return table is not None
