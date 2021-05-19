"""Defines all the functions related to the database"""
from app import db
import hashlib
import random

def insert_new_user(user_id: str, password: str) ->  str:
    """Insert new user to users table.
    Args:
        text (str): Task description
    Returns: The task ID for the inserted entry
    """

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = db.connect()
    query = 'Insert Into Users (username, password_hash) VALUES ("{}", "{}");'.format(
        user_id, password_hash)
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    user_id = query_results[0][0]
    conn.close()

    return user_id

def login_user(user_id:str, password:str) -> str:
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = db.connect()
    query = 'SELECT password_hash FROM Users WHERE username = "{}";'.format(user_id)
    query_results = conn.execute(query).fetchall()

    if (not query_results):
        return 'No User Found'

    for result in query_results:
        if (not (password_hash == result[0])):
            return 'Wrong Password'
    conn.close()
    return 'Success'

def find_urls(username):
    conn = db.connect()
    query = 'SELECT short_url, long_url FROM Urls WHERE username="{}";'.format(username)
    query_results = conn.execute(query).fetchall()

    output = []
    for result in query_results:
        curr_dict = {'short_url': result[0], 'long_url': result[1]}
        output.append(curr_dict)
    conn.close()
    return output

def insert_new_url(long_url, username):
    conn = db.connect()
    rng = random.randint(0, 62**7 - 1)
    short_url = base62_encode(rng)
    
    short_url_count = 1
    while (short_url_count > 0):
        query = 'SELECT short_url FROM Urls WHERE short_url="{}"'.format(short_url)
        query_results = conn.execute(query).fetchall()
        short_url_count = len(query_results)

        if (short_url_count > 0):
            rng = random.randint(0, 62**7 - 1)
            short_url = base62_encode(rng)
        
    insertion = 'INSERT INTO Urls (short_url, long_url, username) VALUES ("{}", "{}", "{}")'.format(short_url, long_url, username)
    conn.execute(insertion)
    insert_results = conn.execute("Select LAST_INSERT_ID();")
    
    insert_results = [x for x in insert_results]
    used_short_url = insert_results[0][0]
    conn.close()

    return used_short_url

def base62_encode(num):
    """Encode a positive number into Base X and return the string.

    Arguments:
    - `num`: The number to encode
    - `alphabet`: The alphabet to use for encoding
    """
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if num == 0:
        return alphabet[0]
    arr = []
    arr_append = arr.append  # Extract bound-method for faster access.
    _divmod = divmod  # Access to locals is faster.
    base = len(alphabet)
    while num:
        num, rem = _divmod(num, base)
        arr_append(alphabet[rem])
    arr.reverse()
    init_string = ''
    if (len(arr) < 7):
      init_string = (7 - len(arr))*'0'
    base62_num = ''.join(arr)
    return init_string + base62_num

def delete_url(short_url):
    conn = db.connect()
    query = 'DELETE FROM Urls WHERE short_url="{}"'.format(short_url)
    conn.execute(query)
    conn.close()

def change_url(short_url, new_long_url):
    conn = db.connect()
    query = 'UPDATE Urls SET long_url="{}" WHERE short_url="{}";'.format(new_long_url, short_url)
    conn.execute(query)
    conn.close()

def find_long_url(short_url):
    conn = db.connect()
    query = 'SELECT long_url FROM Urls WHERE short_url="{}"'.format(short_url)
    query_results = conn.execute(query).fetchall()
    return query_results[0][0]

