import sqlite3
import hashlib
from sqlite3 import Error

USER_TABLE = """CREATE TABLE IF NOT EXISTS user(id integer PRIMARY KEY, username text NOT NULL UNIQUE,password TEXT)"""


def connect_dbs(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        print('Table Created')
    except Error as e:
        print(e)


def view_data(conn, table_name):
    """Select data from database table.
    :param conn: Connection object    
    :param table_name: table name.
    :return: rows of the table.
    """
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()
        return rows
    except Error as e:
        print(e)


def hashing(pwd):
    """encrypt the password field.
    :param pwd: password.
    :return: hash password.
    """
    hash_object = hashlib.md5(bytes(str(pwd), encoding='utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig


def Insert(conn, table_name, username, password):
    """Insert data into tables.
    :param conn: Connection object    
    :param table_name: table name.
    :param username: username.
    :param password: password.
    :return:
    """
    try:
        cur = conn.cursor()
        cur.execute(
            f"Insert into {table_name}('username','password') values (?,?)", (username, hashing(password)))
        conn.commit()
        return {'status': 'Data inserted successfully'}
    except Exception as e:
        return {'Error', str(e)}


# function to fetch password
def password_fetch(conn, table_name, username):
    """Fetch the password of the username.
    :param conn: Connection object
    :param username: username.
    :return : password.
    """
    try:
        cur = conn.cursor()
        cur.execute(
            f"SELECT password FROM {table_name} WHERE username=?", (username,))
        rows = cur.fetchall()
        if rows != None:
            return rows
        else:
            return {'status': '400'}
    except Exception as e:
        return {'Error', str(e)}


if __name__ == "__main__":
    conn = connect_dbs(r'JARVIS\modules\face_identification\face_detection\password.db')
    create_table(conn, USER_TABLE)
    print(Insert(conn, 'user', 'admin', 'admin123'))
