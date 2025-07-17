import os
from dotenv import load_dotenv
load_dotenv()

# import psycopg
# from psycopg import Connection
from psycopg_pool import ConnectionPool
# from psycopg.rows import dict_row
DB_URL = os.environ.get('DB_URL')

def get_db():
    global pool
    pool = ConnectionPool(DB_URL, min_size=1, max_size=10)

    with pool.connection() as con:
        yield con