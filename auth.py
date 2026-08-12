import streamlit as st
import sqlite3
import hashlib
import os


DB_NAME = "users.db"


# =========================================================
# DATABASE
# =========================================================

def create_database():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# PASSWORD HASHING
# =========================================================

def hash_password(password, salt=None):

    if salt is None:
        salt = os.urandom(32)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000
    )

    return (
        password_hash.hex(),
        salt.hex()
    )


# =========================================================
# VERIFY PASSWORD
# =========================================================

def verify_password(password, stored_hash, stored_salt):

    salt = bytes.fromhex(stored_salt)

    password_hash, _ = hash_password(
        password,
        salt
    )

    return password_hash == stored_hash


# =========================================================
# REGISTER USER
# =========================================================

def register_user(username, password):

    username = username.strip()

    if username == "":
        return False, "Username cannot be empty."

    if len(password) < 6:
        return False, "Password must contain at least 6 characters."

    password_hash, salt = hash_password(password)

    try:

        conn = sqlite3.connect(DB_NAME)

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users
            (username, password_hash, salt)
            VALUES (?, ?, ?)
            """,
            (
                username,
                password_hash,
                salt
            )
        )

        conn.commit()
        conn.close()

        return True, "Account created successfully."

    except sqlite3.IntegrityError:

        return False, "Username already exists."

    except Exception as e:

        return False, str(e)


# =========================================================
# LOGIN USER
# =========================================================

def login_user(username, password):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT username, password_hash, salt
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = cursor.fetchone()

    conn.close()

    if user is None:

        return False

    stored_username = user[0]
    stored_hash = user[1]
    stored_salt = user[2]

    if verify_password(
        password,
        stored_hash,
        stored_salt
    ):

        st.session_state["logged_in"] = True
        st.session_state["username"] = stored_username

        return True

    return False


# =========================================================
# LOGOUT
# =========================================================

def logout_user():

    st.session_state["logged_in"] = False

    st.session_state["username"] = ""


# =========================================================
# CHECK LOGIN
# =========================================================

def is_logged_in():

    return st.session_state.get(
        "logged_in",
        False
    )


# =========================================================
# PROTECT PAGE
# =========================================================

def require_login():

    create_database()

    if not is_logged_in():

        st.warning(
            "🔐 Please login to access this page."
        )

        st.stop()