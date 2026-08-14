import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from faq_data import FAQ_DATA


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FAQ Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM BLACK PROFESSIONAL THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background: #000000;
        color: #ffffff;
    }

    .main {
        background: #000000;
    }

    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* ========================================================
       HEADER
       ======================================================== */

    .hero {
        background: linear-gradient(
            135deg,
            #111111 0%,
            #181818 50%,
            #0a0a0a 100%
        );

        border: 1px solid #2f2f2f;
        border-radius: 24px;

        padding: 32px;

        margin-bottom: 24px;

        box-shadow:
            0 10px 40px rgba(0, 0, 0, 0.65);
    }

    .hero-top {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .bot-icon {
        width: 54px;
        height: 54px;

        display: flex;
        align-items: center;
        justify-content: center;

        background: #ffffff;
        color: #000000;

        border-radius: 16px;

        font-size: 28px;
    }

    .hero-title {
        font-size: 30px;
        font-weight: 700;
        color: #ffffff;

        margin: 0;
        line-height: 1.2;
    }

    .hero-subtitle {
        color: #a3a3a3;
        font-size: 14px;

        margin-top: 8px;
    }

    .online-status {
        display: inline-flex;
        align-items: center;

        gap: 7px;

        margin-top: 18px;

        padding: 7px 13px;

        border-radius: 30px;

        background: #151515;
        border: 1px solid #303030;

        color: #d4d4d4;

        font-size: 12px;
    }

    .online-dot {
        width: 8px;
        height: 8px;

        background: #ffffff;

        border-radius: 50%;
    }


    /* ========================================================
       WELCOME CARD
       ======================================================== */

    .welcome-card {
        background: #0d0d0d;

        border: 1px solid #252525;

        border-radius: 18px;

        padding: 22px;

        margin-bottom: 22px;
    }

    .welcome-title {
        color: #ffffff;

        font-size: 19px;
        font-weight: 600;
    }

    .welcome-description {
        color: #9ca3af;

        font-size: 14px;

        line-height: 1.6;

        margin-top: 6px;
    }


    /* ========================================================
       SECTION TITLE
       ======================================================== */

    .section-title {
        color: #d4d4d4;

        font-size: 14px;

        font-weight: 600;

        margin-bottom: 12px;

        letter-spacing: 0.3px;
    }


    /* ========================================================
       QUICK QUESTION BUTTONS
       ======================================================== */

    .stButton > button {

        background: #0d0d0d;

        color: #d4d4d4;

        border: 1px solid #292929;

        border-radius: 12px;

        min-height: 42px;

        font-size: 13px;

        transition: all 0.2s ease;
    }

    .stButton > button:hover {

        background: #ffffff;

        color: #000000;

        border-color: #ffffff;

        transform: translateY(-1px);
    }


    /* ========================================================
       CHAT MESSAGES
       ======================================================== */

    [data-testid="stChatMessage"] {

        background: #0d0d0d;

        border: 1px solid #252525;

        border-radius: 16px;

        margin-bottom: 12px;

        padding: 6px;
    }


    /* ========================================================
       CHAT INPUT
       ======================================================== */

    [data-testid="stChatInput"] {

        background: #0d0d0d;

        border: 1px solid #333333;

        border-radius: 16px;
    }

    [data-testid="stChatInput"] textarea {

        color: #ffffff !important;

        background: #0d0d0d !important;
    }


    /* ========================================================
       CLEAR BUTTON
       ======================================================== */

    .clear-container {
        margin-top: 12px;
        text-align: right;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {

        text-align: center;

        color: #666666;

        font-size: 12px;

        line-height: 1.6;

        padding-top: 30px;

        padding-bottom: 10px;
    }

    .footer strong {
        color: #a3a3a3;
    }


    /* ========================================================
       RESPONSIVE
       ======================================================== */

    @media (max-width: 600px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero {
            padding: 24px;
        }

        .hero-title {
            font-size: 25px;
        }

        .bot-icon {
            width: 48px;
            height: 48px;
            font-size: 24px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PREPARE FAQ DATA
# ============================================================

faq_questions = [
    item["question"]
    for item in FAQ_DATA
]

faq_answers = [
    item["answer"]
    for item in FAQ_DATA
]


# ============================================================
# MACHINE LEARNING MODEL
# ============================================================

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english"
)

faq_vectors = vectorizer.fit_transform(faq_questions)


def get_answer(user_question):

    """
    Find the most relevant FAQ answer using
    TF-IDF and cosine similarity.
    """

    user_vector = vectorizer.transform(
        [user_question]
    )

    similarity_scores = cosine_similarity(
        user_vector,
        faq_vectors
    )[0]

    best_match_index = similarity_scores.argmax()

    best_score = similarity_scores[best_match_index]

    # Similarity threshold
    if best_score < 0.20:

        return (
            "I'm sorry, I couldn't find a relevant answer "
            "to your question. Please try asking about "
            "orders, delivery, refunds, payments, accounts "
            "or customer support."
        )

    return faq_answers[best_match_index]


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-top">

            <div class="bot-icon">
                🤖
            </div>

            <div>
                <div class="hero-title">
                    FAQ Assistant
                </div>

                <div class="hero-subtitle">
                    Smart customer support powered by Machine Learning
                </div>
            </div>

        </div>

        <div class="online-status">

            <span class="online-dot"></span>

            AI Assistant Online

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# WELCOME CARD
# ============================================================

st.markdown(
    """
    <div class="welcome-card">

        <div class="welcome-title">
            How can I help you?
        </div>

        <div class="welcome-description">
            Ask me anything related to our frequently asked questions.
            You can type your question below or choose a quick question.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# QUICK QUESTIONS
# ============================================================

st.markdown(
    '<div class="section-title">Quick Questions</div>',
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)


selected_question = None


with col1:

    if st.button(
        "🕐 Working Hours",
        use_container_width=True
    ):

        selected_question = "What are your working hours?"


with col2:

    if st.button(
        "📦 Track Order",
        use_container_width=True
    ):

        selected_question = "How can I track my order?"


with col3:

    if st.button(
        "💳 Payment Methods",
        use_container_width=True
    ):

        selected_question = (
            "What payment methods do you accept?"
        )


# ============================================================
# CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# Display existing messages

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )


# ============================================================
# QUICK QUESTION RESPONSE
# ============================================================

if selected_question:

    # Add user question

    st.session_state.messages.append(
        {
            "role": "user",
            "content": selected_question
        }
    )

    # Generate answer

    answer = get_answer(
        selected_question
    )

    # Add bot response

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.rerun()


# ============================================================
# USER CHAT INPUT
# ============================================================

user_question = st.chat_input(
    "Type your question here..."
)


if user_question:

    # Add user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    # Generate response

    answer = get_answer(
        user_question
    )

    # Add assistant message

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.rerun()


# ============================================================
# CLEAR CONVERSATION
# ============================================================

if st.session_state.messages:

    st.markdown(
        '<div class="clear-container">',
        unsafe_allow_html=True
    )

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=False
    ):

        st.session_state.messages = []

        st.rerun()

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        <strong>FAQ Assistant</strong>
        &nbsp;•&nbsp;
        Machine Learning FAQ Chatbot

        <br>

        Built with Python, Streamlit & Scikit-learn

    </div>
    """,
    unsafe_allow_html=True
)
