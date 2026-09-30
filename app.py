import pickle
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Bank Customer Churn Prediction",
    page_icon="🏦",
    layout="wide"
)

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

st.title("🏦 Bank Customer Churn Prediction")
st.write("Enter customer details to estimate the probability of churn.")

st.divider()

col1, col2 = st.columns(2)

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

st.divider()

if st.button("Predict Churn", type="primary", use_container_width=True):

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

    st.divider()
    st.subheader("Prediction Result")

    result_col1, result_col2 = st.columns(2)

    with result_col1:
        if prediction == 1:
            st.error("⚠️ Customer is likely to churn")
        else:
            st.success("✅ Customer is likely to stay")

    with result_col2:
        st.metric(
            "Churn Probability",
            f"{probability * 100:.2f}%"
        )

    st.progress(float(probability))

    st.caption(
        "The probability is the model's estimated likelihood of churn for the entered customer."
    )
