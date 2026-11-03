
# FILE 6: DATABASE CONNECTION

import oracledb

DB_USER = "campus_app"
DB_PASSWORD = "2004"
DB_DSN = "localhost:1521/ORCLPDB"


def get_connection():
    return oracledb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        dsn=DB_DSN
    )


def execute_procedure(name, values):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.callproc(name, values)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def fetch_all(statement, values=None):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(statement, values or {})
            columns = [col[0].lower() for col in cursor.description]
            return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
    finally:
        connection.close()


def fetch_value(statement, values=None):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(statement, values or {})
            row = cursor.fetchone()
            return row[0] if row else 0
    finally:
        connection.close()
