import streamlit as st
import sqlite3
import hashlib
import re
import os


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Student Opportunity Hub",
    page_icon="🎓",
    layout="centered"
)


# =========================================================
# DATABASE
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(
    BASE_DIR,
    "users.db"
)

conn = sqlite3.connect(
    DB_PATH,
    timeout=10
)

cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

conn.commit()


# =========================================================
# PASSWORD HASH
# =========================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# =========================================================
# EMAIL VALIDATION
# =========================================================

def valid_email(email):

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return re.match(
        pattern,
        email
    )


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:

    st.session_state.page = "login"


if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if "google_page" not in st.session_state:

    st.session_state.google_page = False


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    .block-container {
        max-width: 430px;
        padding-top: 35px;
    }

    .logo {
        text-align: center;
        margin-bottom: 25px;
    }

    h1 {
        text-align: center;
        font-size: 25px !important;
    }

    .stTextInput input {
        height: 42px;
        border-radius: 6px;
    }

    .stButton button {
        width: 100%;
        height: 42px;
        border-radius: 6px;
    }

    .account-card {
        border: 1px solid #dadce0;
        border-radius: 10px;
        padding: 14px;
        margin: 10px 0;
    }

    .account-name {
        font-size: 15px;
        font-weight: 500;
    }

    .account-email {
        font-size: 13px;
        color: #666;
    }

    .google-title {
        text-align: center;
        font-size: 24px;
        margin-top: 10px;
    }

    .google-subtitle {
        text-align: center;
        color: #555;
        margin-bottom: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOGO
# =========================================================





def show_logo(icon="🎓"):
    st.markdown(
        f"""
        <div style="
            width:55px;
            height:55px;
            border-radius:50%;
            border:3px solid #4285f4;
            display:flex;
            align-items:center;
            justify-content:center;
            margin:auto;
            font-size:28px;
        ">
            {icon}
        </div>
        """,
        unsafe_allow_html=True
    )




# =========================================================
# LOGIN
# =========================================================

def login_page():

    show_logo()

    st.title(
        "Log in to your account"
    )


    email = st.text_input(
        "Email",
        key="login_email"
    )


    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )


    st.checkbox(
        "Remember me",
        key="remember_me"
    )


    # -----------------------------------------------------
    # SIGN IN
    # -----------------------------------------------------

    if st.button(
        "Sign in",
        key="sign_in"
    ):

        if email == "" or password == "":

            st.warning(
                "Please enter email and password."
            )

        else:

            cursor.execute(
                """
                SELECT * FROM users
                WHERE email = ?
                """,
                (email,)
            )

            user = cursor.fetchone()


            if user is None:

                st.error(
                    "Account not created. First Signup cheyyi."
                )

            else:

                entered_password = hash_password(
                    password
                )


                if user[2] == entered_password:

                    st.session_state.logged_in = True

                    st.session_state.page = "dashboard"

                    st.switch_page(
                        "dashboard.py"
                    )

                else:

                    st.error(
                        "Incorrect password."
                    )


    # -----------------------------------------------------
    # OR
    # -----------------------------------------------------

    st.markdown(
        """
        <div style="
            text-align:center;
            margin:18px 0;
            color:#999;
        ">
            or
        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # GOOGLE
    # -----------------------------------------------------

    if st.button(
        "🌈 Continue with Google",
        key="google_login"
    ):

        st.session_state.google_page = True

        st.rerun()


    st.markdown(
        """
        <p style="text-align:center;">
            Don't have an account?
        </p>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # SIGN UP
    # -----------------------------------------------------

    if st.button(
        "Sign up",
        key="go_signup"
    ):

        st.session_state.page = "signup"

        st.rerun()


# =========================================================
# GOOGLE ACCOUNTS
# =========================================================

def google_accounts():

    show_logo()


    st.markdown(
        """
        <div class="google-title">
            Choose an account
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="google-subtitle">
            to continue to your application
        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # ACCOUNT 1
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="account-card">

            <div class="account-name">
                👤 Alekhya
            </div>

            <div class="account-email">
                alekhya@gmail.com
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    if st.button(
        "Continue as Alekhya",
        key="google_alekhya"
    ):

        st.session_state.logged_in = True

        st.session_state.google_page = False

        st.session_state.page = "dashboard"

        st.switch_page(
            "dashboard.py"
        )


    # -----------------------------------------------------
    # ACCOUNT 2
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="account-card">

            <div class="account-name">
                👤 User
            </div>

            <div class="account-email">
                user@gmail.com
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    if st.button(
        "Continue as User",
        key="google_user"
    ):

        st.session_state.logged_in = True

        st.session_state.google_page = False

        st.session_state.page = "dashboard"

        st.switch_page(
            "dashboard.py"
        )


    st.divider()


    if st.button(
        "➕ Use another account",
        key="another_account"
    ):

        st.session_state.page = "signup"

        st.session_state.google_page = False

        st.rerun()


    if st.button(
        "← Back to Login",
        key="back_login"
    ):

        st.session_state.google_page = False

        st.rerun()


# =========================================================
# SIGNUP
# =========================================================

def signup_page():

    show_logo()

    st.title(
        "Create your account"
    )


    email = st.text_input(
        "Email",
        key="signup_email"
    )


    password = st.text_input(
        "Password",
        type="password",
        key="signup_password"
    )


    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        key="confirm_password"
    )


    if st.button(
        "Create Account",
        key="create_account"
    ):

        if (
            email == ""
            or password == ""
            or confirm_password == ""
        ):

            st.warning(
                "Please fill all fields."
            )


        elif not valid_email(email):

            st.error(
                "Please enter a valid email."
            )


        elif len(password) < 6:

            st.error(
                "Password must contain at least 6 characters."
            )


        elif password != confirm_password:

            st.error(
                "Passwords do not match."
            )


        else:

            try:

                hashed_password = hash_password(
                    password
                )


                cursor.execute(
                    """
                    INSERT INTO users
                    (email, password)
                    VALUES (?, ?)
                    """,
                    (
                        email,
                        hashed_password
                    )
                )


                conn.commit()


                st.success(
                    "Account successfully created! 🎉"
                )


                st.session_state.page = "login"

                st.rerun()


            except sqlite3.IntegrityError:

                st.error(
                    "This account already exists."
                )


    if st.button(
        "Back to Login",
        key="back_to_login"
    ):

        st.session_state.page = "login"

        st.rerun()


# =========================================================
# MAIN
# =========================================================

if st.session_state.logged_in:

    st.switch_page(
        "dashboard.py"
    )


elif st.session_state.google_page:

    google_accounts()


elif st.session_state.page == "login":

    login_page()


elif st.session_state.page == "signup":

    signup_page()
