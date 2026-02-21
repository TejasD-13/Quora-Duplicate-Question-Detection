import streamlit as st
import helper
import pickle
import time
import nltk

# Download NLTK stopwords if not already present
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Load model
model = pickle.load(open('model.pkl', 'rb'))

# Page config
st.set_page_config(
    page_title="Quora Duplicate Detector",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #ff3333;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
        transform: translateY(-2px);
    }
    .result-card {
        padding: 2rem;
        border-radius: 15px;
        background: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        text-align: center;
        margin-top: 2rem;
    }
    .header-style {
        color: #1e1e1e;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
        padding-bottom: 2rem;
    }
    .stTextArea textarea {
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# App Title and Header
st.markdown("<h1 class='header-style'>🔍 Quora Duplicate Question Detector</h1>", unsafe_allow_html=True)

# Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Enter Questions to Compare")
    q1 = st.text_area("Question 1", placeholder="Example: How can I learn Python?", height=120)
    q2 = st.text_area("Question 2", placeholder="Example: What is the best way to learn Python for a beginner?", height=120)

    if st.button("Check Similarity"):
        if q1.strip() == "" or q2.strip() == "":
            st.warning("⚠️ Please fill in both question fields.")
        else:
            with st.spinner("🧠 Analyzing semantic similarity..."):
                # Simulate a little bit of processing for better UX
                time.sleep(0.5)
                query = helper.query_point_creator(q1, q2)
                result = model.predict(query)[0]

            st.markdown("---")
            if result:
                st.success("### ✅ Result: Duplicate Detected!")
                st.balloons()
                st.markdown("""
                    <div style='background-color: #d4edda; color: #155724; padding: 20px; border-radius: 10px; border: 1px solid #c3e6cb;'>
                        <strong>Interpretation:</strong> These questions are semantically identical or very similar in meaning.
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error("### ❌ Result: Not Duplicates")
                st.markdown("""
                    <div style='background-color: #f8d7da; color: #721c24; padding: 20px; border-radius: 10px; border: 1px solid #f5c6cb;'>
                        <strong>Interpretation:</strong> These questions appear to be asking different things or have distinct intents.
                    </div>
                """, unsafe_allow_html=True)

with col2:
    st.markdown("### 🤖 About the Model")
    st.info("""
    This system uses a **Random Forest / XGBoost** model trained on the Quora Question Pairs dataset.
    
    **Features extracted:**
    - **Token Features:** Common word counts, stopword ratios.
    - **Fuzzy Features:** Partial ratio, Token sort ratio.
    - **Length Features:** Absolute length diff, common tokens.
    - **NLP:** Bag of Words (CountVectorizer).
    """)
    
    with st.expander("🛠️ How it works"):
        st.write("""
        1. **Preprocessing:** Text is cleaned, lowercased, and contractions are expanded.
        2. **Feature Engineering:** We calculate 22 manual features describing the relationship between the questions.
        3. **Vectorization:** Questions are converted to numeric vectors using Bag of Words.
        4. **Prediction:** The concatenated features are fed into the machine learning model.
        """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: grey;'>NLP Duplicate Question Detector | Built by Tejas Divekar 🚀</div>", 
    unsafe_allow_html=True
)
