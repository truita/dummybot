import os
import sqlite3

workingDirectory = os.path.realpath(os.path.dirname(__file__))
db_dir = os.path.join(workingDirectory, "db")

if not os.path.isdir(db_dir):
    os.mkdir(db_dir)


def get_conn(guild_id) -> sqlite3.Connection:
    db_path = os.path.join(db_dir, f"{guild_id}.sqlite3")
    return sqlite3.connect(db_path, isolation_level=None)


def execute_on_all_db(sql):
    for db_file in os.listdir(db_dir):
        conn = sqlite3.connect(db_file, isolation_level=None)
        conn.execute(sql)
