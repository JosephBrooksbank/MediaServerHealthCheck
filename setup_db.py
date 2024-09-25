import sqlite3


def setup():
    connection = sqlite3.connect('src/data.db')
    cursor = connection.cursor()
    cursor.execute(
        "CREATE table if not exists healthcheck (id INTEGER PRIMARY KEY autoincrement, status TEXT, timestamp TEXT)")
    cursor.execute(
        "CREATE table if not exists sent_failure(id INTEGER PRIMARY KEY, did_send BOOLEAN)"
    )
    cursor.execute(
        "INSERT INTO sent_failure (id, did_send) VALUES (0, false)"
    )
    connection.commit()


if __name__ == '__main__':
    setup()