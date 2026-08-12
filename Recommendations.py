import streamlit as st
import requests
from urllib.parse import quote

from pypdf import PdfReader
from docx import Document


from auth import require_login

require_login()
st.set_page_config(
    page_title="Job Recommendations",
    page_icon="🤖",
    layout="wide"
)


# =====================================================
# LOGIN
# =====================================================

if not st.session_state.get("logged_in", False):

    st.warning("🔐 Please login first.")
    st.stop()


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🎓 Opportunity Hub")

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


# =====================================================
# INDIAN CITIES
# =====================================================

CITIES = [

    "All India",

    "Ahmedabad",
    "Bengaluru",
    "Bhopal",
    "Bhubaneswar",
    "Chandigarh",
    "Chennai",
    "Coimbatore",
    "Delhi",
    "Faridabad",
    "Ghaziabad",
    "Gurugram",
    "Guwahati",
    "Hyderabad",
    "Indore",
    "Jaipur",
    "Jamshedpur",
    "Kanpur",
    "Kochi",
    "Kolkata",
    "Lucknow",
    "Ludhiana",
    "Madurai",
    "Mangaluru",
    "Mohali",
    "Mumbai",
    "Mysuru",
    "Nagpur",
    "Nashik",
    "Noida",
    "Patna",
    "Pune",
    "Raipur",
    "Rajkot",
    "Ranchi",
    "Surat",
    "Thiruvananthapuram",
    "Tiruchirappalli",
    "Udaipur",
    "Vadodara",
    "Varanasi",
    "Vijayawada",
    "Visakhapatnam",
    "Warangal"
]


# =====================================================
# SKILLS
# =====================================================

SKILLS = [

    "python",
    "java",
    "c++",
    "javascript",
    "typescript",

    "html",
    "css",
    "react",
    "angular",
    "node",

    "sql",
    "mysql",
    "postgresql",
    "mongodb",

    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",

    "pandas",
    "numpy",
    "tensorflow",
    "pytorch",

    "power bi",
    "tableau",
    "excel",

    "aws",
    "azure",
    "google cloud",

    "docker",
    "kubernetes",

    "git",
    "github",

    "linux",

    "cyber security",

    "django",
    "flask",
    "spring boot",

    "data analysis",
    "data analytics"
]


# =====================================================
# COMPANY DATABASE
# =====================================================

COMPANIES = [

    {
        "name": "TCS",
        "cities": [
            "Bengaluru",
            "Chennai",
            "Hyderabad",
            "Kolkata",
            "Mumbai",
            "Pune",
            "Delhi"
        ],
        "skills": [
            "python",
            "java",
            "sql",
            "javascript",
            "data analysis"
        ],
        "url": "https://www.tcs.com/careers"
    },

    {
        "name": "Infosys",
        "cities": [
            "Bengaluru",
            "Hyderabad",
            "Pune",
            "Chennai",
            "Mysuru"
        ],
        "skills": [
            "python",
            "java",
            "sql",
            "javascript",
            "cloud"
        ],
        "url": "https://www.infosys.com/careers/"
    },

    {
        "name": "Wipro",
        "cities": [
            "Bengaluru",
            "Hyderabad",
            "Chennai",
            "Pune",
            "Noida"
        ],
        "skills": [
            "python",
            "java",
            "sql",
            "cloud",
            "javascript"
        ],
        "url": "https://careers.wipro.com/"
    },

    {
        "name": "Accenture",
        "cities": [
            "Bengaluru",
            "Hyderabad",
            "Chennai",
            "Pune",
            "Mumbai",
            "Gurugram",
            "Noida"
        ],
        "skills": [
            "python",
            "java",
            "sql",
            "aws",
            "azure",
            "data analysis"
        ],
        "url": "https://www.accenture.com/in-en/careers"
    },

    {
        "name": "Deloitte",
        "cities": [
            "Hyderabad",
            "Bengaluru",
            "Mumbai",
            "Pune",
            "Gurugram",
            "Chennai"
        ],
        "skills": [
            "python",
            "sql",
            "power bi",
            "excel",
            "data analysis"
        ],
        "url": "https://www.deloitte.com/careers"
    },

    {
        "name": "Amazon",
        "cities": [
            "Bengaluru",
            "Hyderabad",
            "Chennai",
            "Mumbai",
            "Pune",
            "Delhi"
        ],
        "skills": [
            "python",
            "java",
            "c++",
            "sql",
            "aws"
        ],
        "url": "https://www.amazon.jobs/"
    },

    {
        "name": "Microsoft",
        "cities": [
            "Hyderabad",
            "Bengaluru",
            "Noida"
        ],
        "skills": [
            "python",
            "java",
            "c++",
            "sql",
            "azure"
        ],
        "url": "https://careers.microsoft.com/"
    },

    {
        "name": "Google",
        "cities": [
            "Bengaluru",
            "Hyderabad",
            "Mumbai"
        ],
        "skills": [
            "python",
            "java",
            "c++",
            "sql",
            "machine learning"
        ],
        "url": "https://www.google.com/about/careers/applications/"
    },

    {
        "name": "IBM",
        "cities": [
            "Bengaluru",
            "Hyderabad",
            "Pune",
            "Chennai",
            "Noida"
        ],
        "skills": [
            "python",
            "java",
            "sql",
            "cloud",
            "machine learning"
        ],
        "url": "https://www.ibm.com/careers"
    },

    {
        "name": "Capgemini",
        "cities": [
            "Bengaluru",
            "Hyderabad",
            "Pune",
            "Mumbai",
            "Chennai",
            "Kolkata"
        ],
        "skills": [
            "python",
            "java",
            "sql",
            "javascript",
            "cloud"
        ],
        "url": "https://www.capgemini.com/in-en/careers/"
    },

    {
        "name": "Cognizant",
        "cities": [
            "Chennai",
            "Bengaluru",
            "Hyderabad",
            "Pune",
            "Kolkata",
            "Coimbatore"
        ],
        "skills": [
            "python",
            "java",
            "sql",
            "javascript",
            "cloud"
        ],
        "url": "https://careers.cognizant.com/"
    },

    {
        "name": "HCLTech",
        "cities": [
            "Noida",
            "Chennai",
            "Bengaluru",
            "Hyderabad",
            "Pune",
            "Lucknow"
        ],
        "skills": [
            "python",
            "java",
            "sql",
            "javascript",
            "cloud"
        ],
        "url": "https://www.hcltech.com/careers"
    },

    {
        "name": "Tech Mahindra",
        "cities": [
            "Pune",
            "Hyderabad",
            "Bengaluru",
            "Chennai",
            "Noida",
            "Mumbai"
        ],
        "skills": [
            "python",
            "java",
            "sql",
            "javascript",
            "cloud"
        ],
        "url": "https://careers.techmahindra.com/"
    },

    {
        "name": "Oracle",
        "cities": [
            "Bengaluru",
            "Hyderabad",
            "Pune",
            "Noida"
        ],
        "skills": [
            "java",
            "python",
            "sql",
            "cloud",
            "database"
        ],
        "url": "https://www.oracle.com/careers/"
    },

    {
        "name": "Salesforce",
        "cities": [
            "Bengaluru",
            "Hyderabad",
            "Mumbai"
        ],
        "skills": [
            "javascript",
            "python",
            "sql",
            "cloud"
        ],
        "url": "https://www.salesforce.com/company/careers/"
    }

]


# =====================================================
# PDF READER
# =====================================================

def read_pdf(file):

    try:

        reader = PdfReader(file)

        text = ""

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

        return text

    except Exception:

        return ""


# =====================================================
# DOCX READER
# =====================================================

def read_docx(file):

    try:

        document = Document(file)

        text = ""

        for paragraph in document.paragraphs:

            text += paragraph.text + "\n"

        return text

    except Exception:

        return ""


# =====================================================
# RESUME READER
# =====================================================

def extract_resume(file):

    filename = file.name.lower()

    if filename.endswith(".pdf"):

        return read_pdf(file)

    if filename.endswith(".docx"):

        return read_docx(file)

    return ""


# =====================================================
# SKILL DETECTOR
# =====================================================

def find_skills(text):

    text = text.lower()

    detected = []

    for skill in SKILLS:

        if skill in text:

            detected.append(skill)

    return list(
        dict.fromkeys(detected)
    )


# =====================================================
# JOB SEARCH URL
# =====================================================

def create_job_search_url(
    skill,
    city
):

    query = quote(
        f"{skill} jobs {city} India"
    )

    return (
        "https://www.google.com/search?"
        f"q={query}"
    )


# =====================================================
# PAGE
# =====================================================

st.title(
    "🤖 Resume Based Job Recommendations"
)

st.write(
    "Upload your resume, select a city and "
    "find companies matching your skills."
)

st.divider()


# =====================================================
# CITY
# =====================================================

selected_city = st.selectbox(
    "📍 Select Job Location",
    CITIES
)


st.info(
    f"Searching opportunities for: {selected_city}"
)


# =====================================================
# UPLOAD
# =====================================================

resume = st.file_uploader(
    "📄 Upload Resume",
    type=["pdf", "docx"]
)


if resume:

    st.success(
        f"Uploaded: {resume.name}"
    )

    if st.button(
        "🤖 Analyze Resume & Recommend Jobs",
        use_container_width=True
    ):

        with st.spinner(
            "Analyzing your resume..."
        ):

            resume_text = extract_resume(
                resume
            )

            detected_skills = find_skills(
                resume_text
            )


        # =================================================
        # RESUME TEXT CHECK
        # =================================================

        if not resume_text.strip():

            st.error(
                "Could not read this resume. "
                "Please upload a text-based PDF or DOCX."
            )

            st.stop()


        # =================================================
        # SKILLS
        # =================================================

        st.subheader(
            "🧠 Skills Detected"
        )

        if detected_skills:

            st.success(
                ", ".join(
                    skill.title()
                    for skill in detected_skills
                )
            )

        else:

            st.warning(
                "No supported skills were detected."
            )

            st.info(
                "Add skills such as Python, Java, "
                "SQL, Machine Learning, AWS etc."
            )


        st.divider()


        # =================================================
        # COMPANY MATCHING
        # =================================================

        st.subheader(
            "🏢 Recommended Companies"
        )

        matches = []

        for company in COMPANIES:

            company_cities = company["cities"]

            # City filtering

            if selected_city != "All India":

                if selected_city not in company_cities:

                    continue


            matched_skills = []

            for skill in detected_skills:

                if skill in company["skills"]:

                    matched_skills.append(
                        skill
                    )


            if matched_skills:

                if detected_skills:

                    score = (
                        len(matched_skills)
                        /
                        len(detected_skills)
                    ) * 100

                else:

                    score = 0


                matches.append(
                    (
                        company,
                        matched_skills,
                        score
                    )
                )


        matches.sort(
            key=lambda x: x[2],
            reverse=True
        )


        # =================================================
        # DISPLAY
        # =================================================

        if matches:

            st.success(
                f"{len(matches)} companies matched your profile."
            )

            for company, matched, score in matches:

                with st.container(
                    border=True
                ):

                    st.subheader(
                        "🏢 " +
                        company["name"]
                    )

                    st.write(
                        "📍 Available cities: "
                        +
                        ", ".join(
                            company["cities"]
                        )
                    )

                    st.write(
                        f"🎯 Skill Match: {score:.0f}%"
                    )

                    st.progress(
                        min(
                            int(score),
                            100
                        )
                    )

                    st.write(
                        "🧠 Matching Skills: "
                        +
                        ", ".join(
                            matched
                        )
                    )

                    st.link_button(
                        "🚀 Company Careers / Apply",
                        company["url"],
                        use_container_width=True
                    )


        else:

            st.warning(
                "No company matched your detected skills "
                "for the selected city."
            )


        # =================================================
        # JOB SEARCH
        # =================================================

        st.divider()

        st.subheader(
            "🔎 Search Jobs For Your Skills"
        )

        if detected_skills:

            for skill in detected_skills[:10]:

                if selected_city == "All India":

                    search_city = "India"

                else:

                    search_city = selected_city


                url = create_job_search_url(
                    skill,
                    search_city
                )

                st.link_button(
                    f"🔎 {skill.title()} Jobs - {search_city}",
                    url,
                    use_container_width=True
                )

        else:

            st.info(
                "Skills are required to generate job searches."
            )