import sys
from pathlib import Path

import streamlit as st


# =========================================================
# PATH SETUP
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))

from troubleshooter import identify_issue
from llm_client import generate_ai_response


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Linux Troubleshooting Assistant",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# RESPONSIVE STYLING
# =========================================================

st.markdown(
    """
<style>

/* Main content width */
.block-container {
    max-width: 1100px;
    padding-top: 3rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* Main title */
h1 {
    font-size: clamp(1.9rem, 3.2vw, 2.6rem) !important;
    line-height: 1.3 !important;
    padding-top: 0.2rem !important;
    padding-bottom: 0.2rem !important;
    margin-bottom: 0.2rem !important;
}

/* Subtitle */
.app-subtitle {
    font-size: clamp(0.9rem, 1.5vw, 1.05rem);
    line-height: 1.5;
    opacity: 0.68;
    margin-top: -0.2rem;
    margin-bottom: 1.6rem;
}

/* Buttons */
div.stButton > button {
    min-height: 3rem;
    border-radius: 8px;
    font-weight: 600;
}

/* Text area */
textarea {
    border-radius: 8px !important;
}

/* Retrieval metric cards */
div[data-testid="stMetric"] {
    border: 1px solid rgba(128, 128, 128, 0.25);
    padding: 1rem;
    border-radius: 10px;
}

/* Tablet */
@media (max-width: 900px) {

    .block-container {
        padding-left: 1.2rem;
        padding-right: 1.2rem;
    }

    h1 {
        font-size: 2rem !important;
    }
}

/* Mobile */
@media (max-width: 600px) {

    .block-container {
        padding-top: 1rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    h1 {
        font-size: 1.6rem !important;
        line-height: 1.3 !important;
    }

    .app-subtitle {
        font-size: 0.88rem;
    }

    div[data-testid="stMetric"] {
        padding: 0.7rem;
    }
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.title("🛠️ AI-Powered Linux Troubleshooting Assistant")

st.markdown(
    '<div class="app-subtitle">'
    'Retrieval-grounded AI assistance for Linux infrastructure '
    'troubleshooting'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# INTRODUCTION
# =========================================================

st.write(
    "Describe a Linux infrastructure problem and the assistant "
    "will retrieve relevant troubleshooting knowledge and use an "
    "LLM to generate diagnostic guidance."
)

st.info(
    "🔒 This assistant provides diagnostic guidance only. "
    "It does not execute commands or make changes to your system."
)


# =========================================================
# SESSION STATE
# =========================================================

if "analysis" not in st.session_state:
    st.session_state.analysis = None


# =========================================================
# INPUT SECTION
# =========================================================

st.subheader("Describe your Linux issue")

user_problem = st.text_area(
    "Linux issue",
    label_visibility="collapsed",
    placeholder=(
        "Example: SSH connection to my Linux server is timing out. "
        "The server was reachable earlier but now I cannot connect "
        "on port 22."
    ),
    height=130
)

analyze = st.button(
    "🔍 Analyze Issue",
    type="primary",
    use_container_width=True
)


# =========================================================
# ANALYZE
# =========================================================

if analyze:

    if not user_problem.strip():

        st.warning(
            "Please describe a Linux issue first."
        )

    else:

        (
            issue_id,
            issue_data,
            score,
            matched_keywords
        ) = identify_issue(user_problem)

        st.session_state.analysis = {
            "problem": user_problem,
            "issue_id": issue_id,
            "issue_data": issue_data,
            "score": score,
            "matched_keywords": matched_keywords,
            "response": None,
            "ai_success": False
        }

        try:

            with st.spinner(
                "Retrieving troubleshooting knowledge "
                "and analyzing the issue..."
            ):

                response = generate_ai_response(
                    user_problem,
                    issue_data
                )

            st.session_state.analysis["response"] = response
            st.session_state.analysis["ai_success"] = True

        except Exception:

            st.session_state.analysis["ai_success"] = False


# =========================================================
# RESULTS
# =========================================================

if st.session_state.analysis:

    result = st.session_state.analysis

    issue_data = result["issue_data"]
    score = result["score"]
    matched_keywords = result["matched_keywords"]

    st.divider()

    # -----------------------------------------------------
    # RETRIEVAL ANALYSIS
    # -----------------------------------------------------

    st.subheader("🔎 Retrieval Analysis")

    if issue_data:

        col1, col2 = st.columns(
            [2, 1],
            gap="medium"
        )

        with col1:

            st.metric(
                "Detected Category",
                issue_data["name"]
            )

        with col2:

            st.metric(
                "Retrieval Score",
                score
            )

        if matched_keywords:

            indicators = " ".join(
                f"`{keyword}`"
                for keyword in matched_keywords
            )

            st.markdown(
                f"**Matched Indicators:** {indicators}"
            )

    else:

        st.warning(
            "No direct match was found in the local knowledge base. "
            "The AI analyzed the issue with limited local context."
        )


    # -----------------------------------------------------
    # AI ANALYSIS
    # -----------------------------------------------------

    st.divider()

    st.subheader("🤖 AI Troubleshooting Analysis")

    if result["ai_success"]:

        st.success(
            "Analysis completed successfully."
        )

        st.markdown(
            result["response"]
        )


    # -----------------------------------------------------
    # FALLBACK
    # -----------------------------------------------------

    else:

        st.error(
            "The AI service is currently unavailable."
        )

        if issue_data:

            st.warning(
                "Showing guidance from the local "
                "troubleshooting knowledge base."
            )

            st.markdown("#### Possible Causes")

            for cause in issue_data["possible_causes"]:

                st.markdown(
                    f"- {cause}"
                )

            st.markdown(
                "#### Recommended Diagnostic Commands"
            )

            for command in issue_data["diagnostic_commands"]:

                st.code(
                    command,
                    language="bash"
                )

            st.info(
                "Review the diagnostic output before "
                "performing remediation."
            )

        else:

            st.warning(
                "No troubleshooting guidance is "
                "currently available for this issue."
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Built with Python • Streamlit • Linux Knowledge Retrieval • "
    "LLM Integration"
)