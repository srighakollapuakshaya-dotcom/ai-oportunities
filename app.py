import streamlit as st

from auth import (
    create_database,
    register_user,
    login_user,
    logout_user,
    is_logged_in
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Student Opportunity Hub",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# DATABASE
# =========================================================

create_database()


# =========================================================
# LOGIN / REGISTER PAGE
# =========================================================

if not is_logged_in():

    st.markdown(
        """
        <style>

        .main-title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
        }

        .sub-title {
            text-align: center;
            font-size: 18px;
            color: gray;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-title">'
        '🎓 Student Opportunity Hub'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">'
        'Scholarships • Internships • Resume • Jobs'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # =====================================================
    # TABS
    # =====================================================

    login_tab, register_tab = st.tabs(
        [
            "🔐 Login",
            "📝 Create Account"
        ]
    )


    # =====================================================
    # LOGIN
    # =====================================================

    with login_tab:

        st.subheader(
            "🔐 Login"
        )

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            if username == "" or password == "":

                st.error(
                    "Please enter username and password."
                )

            else:

                success = login_user(
                    username,
                    password
                )

                if success:

                    st.success(
                        "Login successful! 🎉"
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Invalid username or password."
                    )


    # =====================================================
    # REGISTER
    # =====================================================

    with register_tab:

        st.subheader(
            "📝 Create New Account"
        )

        new_username = st.text_input(
            "Create Username",
            key="register_username"
        )

        new_password = st.text_input(
            "Create Password",
            type="password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="confirm_password"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            if new_username == "":
                st.error(
                    "Please enter a username."
                )

            elif new_password == "":
                st.error(
                    "Please enter a password."
                )

            elif new_password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            else:

                success, message = register_user(
                    new_username,
                    new_password
                )

                if success:

                    st.success(
                        "✅ Account created successfully!"
                    )

                    st.info(
                        "Now go to the Login tab and login."
                    )

                else:

                    st.error(
                        message
                    )

    st.stop()


# =========================================================
# LOGGED-IN USER
# =========================================================

username = st.session_state.get(
    "username",
    "Student"
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title(
    "🎓 Opportunity Hub"
)

st.sidebar.success(
    f"👤 {username}"
)

st.sidebar.divider()


# =========================================================
# NAVIGATION
# =========================================================

st.sidebar.page_link(
    "app.py",
    label="🏠 Home"
)

st.sidebar.page_link(
    "pages/Scholarships.py",
    label="🎓 Scholarships"
)

st.sidebar.page_link(
    "pages/Internships.py",
    label="💼 Internships"
)

st.sidebar.page_link(
    "pages/Resume.py",
    label="📄 Create Resume"
)

st.sidebar.page_link(
    "pages/Recommendations.py",
    label="🤖 Job Recommendations"
)


st.sidebar.divider()


# =========================================================
# LOGOUT
# =========================================================

if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True
):

    logout_user()

    st.rerun()


# =========================================================
# HOME PAGE
# =========================================================

st.title(
    f"Welcome, {username}! 👋"
)

st.header(
    "🎓 Student Opportunity Hub"
)

st.write(
    "Your single platform for discovering "
    "scholarships, internships and jobs."
)

st.divider()


# =========================================================
# SCHOLARSHIPS
# =========================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader(
        "🎓 Scholarships"
    )

    st.write(
        "Find latest scholarship updates "
        "and application opportunities."
    )

    if st.button(
        "🔎 Find Scholarships",
        use_container_width=True,
        key="scholarship_home"
    ):

        st.switch_page(
            "pages/Scholarships.py"
        )


# =========================================================
# INTERNSHIPS
# =========================================================

with col2:

    st.subheader(
        "💼 Internships"
    )

    st.write(
        "Find internship opportunities "
        "across India."
    )

    if st.button(
        "🔎 Find Internships",
        use_container_width=True,
        key="internship_home"
    ):

        st.switch_page(
            "pages/Internships.py"
        )


# =========================================================
# RESUME
# =========================================================

col3, col4 = st.columns(2)


with col3:

    st.subheader(
        "📄 Resume Builder"
    )

    st.write(
        "Create your professional resume."
    )

    if st.button(
        "📄 Create Resume",
        use_container_width=True,
        key="resume_home"
    ):

        st.switch_page(
            "pages/Resume.py"
        )


# =========================================================
# JOB RECOMMENDATION
# =========================================================

with col4:

    st.subheader(
        "🤖 Job Recommendations"
    )

    st.write(
        "Upload your resume and find "
        "suitable job opportunities."
    )

    if st.button(
        "🤖 Find Recommended Jobs",
        use_container_width=True,
        key="jobs_home"
    ):

        st.switch_page(
            "pages/Recommendations.py"
        )


# =========================================================
# FEATURES
# =========================================================

st.divider()

st.header(
    "✨ Platform Features"
)

f1, f2, f3, f4 = st.columns(4)


with f1:

    st.info(
        "🎓 **Scholarships**\n\n"
        "Latest scholarship updates."
    )


with f2:

    st.info(
        "💼 **Internships**\n\n"
        "Find internship opportunities."
    )


with f3:

    st.info(
        "📄 **Resume Builder**\n\n"
        "Create your resume."
    )


with f4:

    st.info(
        "🤖 **Job Recommendations**\n\n"
        "Get suitable jobs."
    )