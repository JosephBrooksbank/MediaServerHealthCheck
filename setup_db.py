import sqlite3


def setup():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute(
        "CREATE table if not exists healthcheck (id INTEGER PRIMARY KEY autoincrement, status TEXT, timestamp TEXT)")
    connection.commit()


if __name__ == '__main__':
    setup()