import pickle
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Bank Customer Churn Prediction",
    page_icon="🏦",
    layout="wide"
)

# ──────────────────────────────────────────────
# Professional Banking Theme – CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
/* ── Import Inter from Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Root variables ── */
:root {
    --navy:       #0a1628;
    --navy-light: #1b2a4a;
    --blue:       #1a73e8;
    --blue-light: #4a9af5;
    --blue-glow:  rgba(26, 115, 232, .12);
    --teal:       #00bfa5;
    --white:      #ffffff;
    --off-white:  #f4f6fa;
    --gray-50:    #f8f9fc;
    --gray-100:   #e8ecf1;
    --gray-200:   #d0d5dd;
    --gray-500:   #667085;
    --gray-700:   #344054;
    --gray-900:   #101828;
    --red:        #e53935;
    --red-bg:     rgba(229, 57, 53, .08);
    --green:      #2e7d32;
    --green-bg:   rgba(46, 125, 50, .08);
    --shadow-sm:  0 1px 3px rgba(0,0,0,.06), 0 1px 2px rgba(0,0,0,.04);
    --shadow-md:  0 4px 12px rgba(0,0,0,.07), 0 2px 4px rgba(0,0,0,.04);
    --shadow-lg:  0 10px 30px rgba(0,0,0,.08), 0 4px 8px rgba(0,0,0,.04);
    --radius:     12px;
    --radius-sm:  8px;
}

/* ── Global resets ── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
}

.stApp {
    background: var(--off-white) !important;
}

/* ── Hide default Streamlit branding ── */
#MainMenu, footer, header {visibility: hidden;}

/* ── Main container ── */
.block-container {
    max-width: 1200px !important;
    padding: 1.5rem 2rem 3rem !important;
}

/* ── Header Banner ── */
.header-banner {
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy-light) 50%, var(--blue) 100%);
    border-radius: var(--radius);
    padding: 2.25rem 2.5rem;
    margin-bottom: 2rem;
    box-shadow: var(--shadow-lg);
    position: relative;
    overflow: hidden;
}
.header-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 500px;
    height: 500px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,.04) 0%, transparent 70%);
    pointer-events: none;
}
.header-banner h1 {
    color: var(--white) !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    margin: 0 0 .35rem 0 !important;
    letter-spacing: -.02em;
    line-height: 1.2;
}
.header-banner p {
    color: rgba(255,255,255,.72) !important;
    font-size: .95rem !important;
    margin: 0 !important;
    font-weight: 400;
}
.header-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,.12);
    backdrop-filter: blur(6px);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: .75rem;
    font-weight: 500;
    color: rgba(255,255,255,.88);
    margin-bottom: .75rem;
    border: 1px solid rgba(255,255,255,.12);
}

/* ── Section Card ── */
.section-card {
    background: var(--white);
    border-radius: var(--radius);
    padding: 1.75rem 2rem;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--gray-100);
    margin-bottom: 1.5rem;
    transition: box-shadow .2s ease;
}
.section-card:hover {
    box-shadow: var(--shadow-md);
}
.section-title {
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    color: var(--gray-900) !important;
    margin: 0 0 .25rem 0 !important;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-subtitle {
    font-size: .82rem !important;
    color: var(--gray-500) !important;
    margin: 0 0 1.25rem 0 !important;
    font-weight: 400;
}

/* ── Input styling ── */
.stNumberInput > div > div > input,
.stSelectbox > div > div > div {
    border-radius: var(--radius-sm) !important;
    border-color: var(--gray-200) !important;
    font-size: .9rem !important;
    transition: border-color .15s ease, box-shadow .15s ease;
}
.stNumberInput > div > div > input:focus,
.stSelectbox > div > div > div:focus-within {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 3px var(--blue-glow) !important;
}

.stNumberInput label, .stSelectbox label {
    font-size: .82rem !important;
    font-weight: 500 !important;
    color: var(--gray-700) !important;
}

/* ── Primary Button ── */
.stButton > button[kind="primary"],
.stButton > button {
    background: linear-gradient(135deg, var(--blue), var(--blue-light)) !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    color: var(--white) !important;
    font-weight: 600 !important;
    font-size: .95rem !important;
    padding: .75rem 1.5rem !important;
    letter-spacing: .01em;
    box-shadow: 0 2px 8px rgba(26,115,232,.25) !important;
    transition: transform .15s ease, box-shadow .15s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(26,115,232,.35) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Progress bar ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--blue), var(--blue-light)) !important;
    border-radius: 6px !important;
}
.stProgress > div > div {
    background: var(--gray-100) !important;
    border-radius: 6px !important;
    height: 8px !important;
}

/* ── Metric card ── */
[data-testid="stMetric"] {
    background: var(--gray-50);
    border-radius: var(--radius-sm);
    padding: 1rem 1.25rem;
    border: 1px solid var(--gray-100);
}
[data-testid="stMetricLabel"] {
    font-size: .8rem !important;
    font-weight: 500 !important;
    color: var(--gray-500) !important;
    text-transform: uppercase;
    letter-spacing: .04em;
}
[data-testid="stMetricValue"] {
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: var(--navy) !important;
}

/* ── Alert boxes ── */
.stAlert {
    border-radius: var(--radius-sm) !important;
    border: none !important;
    font-weight: 500 !important;
}

/* ── Result cards (custom) ── */
.result-card {
    border-radius: var(--radius);
    padding: 1.5rem 1.75rem;
    text-align: center;
}
.result-churn {
    background: var(--red-bg);
    border: 1px solid rgba(229,57,53,.18);
}
.result-stay {
    background: var(--green-bg);
    border: 1px solid rgba(46,125,50,.18);
}
.result-icon {
    font-size: 2.25rem;
    margin-bottom: .5rem;
}
.result-label {
    font-size: 1.05rem;
    font-weight: 600;
    margin: 0;
}
.result-churn .result-label { color: var(--red); }
.result-stay  .result-label { color: var(--green); }

.prob-card {
    background: var(--blue-glow);
    border: 1px solid rgba(26,115,232,.18);
    border-radius: var(--radius);
    padding: 1.5rem 1.75rem;
    text-align: center;
}
.prob-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--blue);
    margin: .25rem 0 .15rem;
}
.prob-label {
    font-size: .8rem;
    font-weight: 500;
    color: var(--gray-500);
    text-transform: uppercase;
    letter-spacing: .04em;
    margin: 0;
}

/* ── Caption ── */
.caption-text {
    font-size: .8rem;
    color: var(--gray-500);
    text-align: center;
    margin-top: .75rem;
    padding: 0 1rem;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 1.25rem 0 .5rem;
    color: var(--gray-500);
    font-size: .78rem;
    border-top: 1px solid var(--gray-100);
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Load model artifacts (unchanged)
# ──────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    with open("bank_churn_model.pkl", "rb") as file:
        model = pickle.load(file)

    with open("feature_names.pkl", "rb") as file:
        feature_names = pickle.load(file)

    with open("preprocessing_mappings.pkl", "rb") as file:
        mappings = pickle.load(file)

    return model, feature_names, mappings

model, feature_names, mappings = load_artifacts()

# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
    <div class="header-badge">🏦 Churn Analytics Platform</div>
    <h1>Bank Customer Churn Prediction</h1>
    <p>Enter customer details below to estimate their probability of churning. Powered by machine-learning models trained on real banking data.</p>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Customer Details Input Form
# ──────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:-10px;">
    <p class="section-title">📋 Customer Information</p>
    <p class="section-subtitle">Fill in each field to describe the customer profile</p>
</div>
""", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns(2, gap="large")

    with col1:
        credit_score = st.number_input(
            "Credit Score",
            min_value=300,
            max_value=900,
            value=650,
            step=1
        )

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=35,
            step=1
        )

        tenure = st.number_input(
            "Tenure",
            min_value=0,
            max_value=10,
            value=5,
            step=1
        )

        balance = st.number_input(
            "Balance",
            min_value=0.0,
            value=75000.0,
            step=1000.0
        )

        num_of_products = st.number_input(
            "Number of Products",
            min_value=1,
            max_value=4,
            value=1,
            step=1
        )

        has_cr_card = st.selectbox(
            "Has Credit Card",
            ["Yes", "No"]
        )

    with col2:
        is_active_member = st.selectbox(
            "Is Active Member",
            ["Yes", "No"]
        )

        estimated_salary = st.number_input(
            "Estimated Salary",
            min_value=0.0,
            value=75000.0,
            step=1000.0
        )

        geography = st.selectbox(
            "Geography",
            ["France", "Spain", "Germany"]
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female"]
        )

        month = st.selectbox(
            "Bank Joining Month",
            list(mappings["month"].keys())
        )

# ──────────────────────────────────────────────
# Predict Button
# ──────────────────────────────────────────────
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

if st.button("🔍  Predict Churn", type="primary", use_container_width=True):

    # ── Build input (unchanged) ──
    input_data = {
        "CreditScore": credit_score,
        "Age": age,
        "Tenure": tenure,
        "Balance": balance,
        "NumOfProducts": num_of_products,
        "HasCrCard": 1 if has_cr_card == "Yes" else 0,
        "IsActiveMember": 1 if is_active_member == "Yes" else 0,
        "EstimatedSalary": estimated_salary,
        "GeographyLocation": mappings["geography"][geography],
        "GenderCategory": mappings["gender"][gender],
        "Month": mappings["month"][month]
    }

    customer_df = pd.DataFrame([input_data])

    customer_df = customer_df[feature_names]

    prediction = model.predict(customer_df)[0]
    probability = model.predict_proba(customer_df)[0][1]

    # ── Results ──
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-bottom:-10px;">
        <p class="section-title">📊 Prediction Result</p>
        <p class="section-subtitle">Model output for the customer profile above</p>
    </div>
    """, unsafe_allow_html=True)

    result_col, prob_col = st.columns(2, gap="large")

    with result_col:
        if prediction == 1:
            st.markdown("""
            <div class="result-card result-churn">
                <div class="result-icon">⚠️</div>
                <p class="result-label">Customer is likely to churn</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="result-card result-stay">
                <div class="result-icon">✅</div>
                <p class="result-label">Customer is likely to stay</p>
            </div>
            """, unsafe_allow_html=True)

    with prob_col:
        st.markdown(f"""
        <div class="prob-card">
            <p class="prob-label">Churn Probability</p>
            <p class="prob-value">{probability * 100:.2f}%</p>
            <p class="prob-label">Model Confidence Score</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    st.progress(float(probability))

    st.markdown(
        '<p class="caption-text">The probability shown is the model\'s estimated likelihood of churn for the entered customer profile.</p>',
        unsafe_allow_html=True
    )

# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.markdown(
    '<div class="footer">Built with Streamlit · Bank Customer Churn Analytics</div>',
    unsafe_allow_html=True
)
