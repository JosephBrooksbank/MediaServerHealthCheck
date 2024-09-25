import sqlite3
from datetime import datetime
from dotenv import dotenv_values
config = dotenv_values("../.env", encoding="utf-8")

class Database:
    def __enter__(self):
        self.connection = sqlite3.connect('./data.db')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def record_timestamp(self, status):
        print(f"Saving {status} at {datetime.now()}")
        self.connection.cursor().execute("INSERT INTO healthcheck (status, timestamp) VALUES (?, ?)",
                                         (status, datetime.now()))
        self.clear_old_logs()
        self.connection.commit()

    def clear_old_logs(self):
        self.connection.cursor().execute(f"""
        delete from healthcheck
        where id not in (
            select id
            from healthcheck
            order by timestamp desc
            limit {config['MAX_RECORDS']})
        """)
        self.connection.commit()

    def get_sent_failure(self) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("SELECT did_send FROM sent_failure WHERE id=0")
        return cursor.fetchone()[0]

    def set_sent_failure(self, did_send: bool):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE sent_failure SET did_send=? WHERE id=0", (did_send,))
        self.connection.commit()

    def get_latest_alive(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM healthcheck WHERE status='Alive!' ORDER BY timestamp DESC LIMIT 1")
        # get the latest timestamp from the database string
        time = datetime.strptime(cursor.fetchone()[2], "%Y-%m-%d %H:%M:%S.%f")

        time_diff = datetime.now() - time
        return time_diff.seconds

