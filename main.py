import streamlit as st
from google.cloud import aiplatform
import json

# ------------------------------------------
# Initialize Vertex AI endpoint
# ------------------------------------------
ENDPOINT_ID = "projects/PROJECT_ID/locations/us-central1/endpoints/ENDPOINT_ID"

aiplatform.init(project="PROJECT_ID", location="us-central1")
endpoint = aiplatform.Endpoint(endpoint_name=ENDPOINT_ID)

st.title("📉 Customer Churn Prediction (Vertex AI)")
st.write("Fill out the customer information below and get churn probability.")

# ------------------------------------------
# Streamlit Form Inputs
# ------------------------------------------

gender = st.selectbox("Gender", ["Male", "Female"])
SeniorCitizen = st.selectbox("Senior Citizen?", ["No", "Yes"])
Partner = st.selectbox("Has Partner?", ["Yes", "No"])
Dependents = st.selectbox("Has Dependents?", ["Yes", "No"])
tenure = st.text_input("Tenure (Months)", "12")

PhoneService = st.selectbox("Phone Service", ["Yes", "No"])
MultipleLines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])

InternetService = st.selectbox("Internet Service",
                               ["DSL", "Fiber optic", "No"])

OnlineSecurity = st.selectbox("Online Security", ["Yes", "No"])
OnlineBackup = st.selectbox("Online Backup", ["Yes", "No"])
DeviceProtection = st.selectbox("Device Protection", ["Yes", "No"])
TechSupport = st.selectbox("Tech Support", ["Yes", "No"])
StreamingTV = st.selectbox("Streaming TV", ["Yes", "No"])
StreamingMovies = st.selectbox("Streaming Movies", ["Yes", "No"])

Contract = st.selectbox("Contract",
                        ["Month-to-month", "One year", "Two year"])
PaperlessBilling = st.selectbox("Paperless Billing", ["Yes", "No"])
PaymentMethod = st.selectbox("Payment Method",
                             ["Electronic check", "Mailed check",
                              "Bank transfer (automatic)",
                              "Credit card (automatic)"])

MonthlyCharges = st.text_input("Monthly Charges", "75.50")
TotalCharges = st.text_input("Total Charges", "840.75")

# ------------------------------------------
# Prediction Button
# ------------------------------------------
if SeniorCitizen=="yes":
    SeniorCitizen="1"
else:
    SeniorCitizen="0"

if st.button("Predict Churn"):
    instance = {
        "gender": gender,
        "SeniorCitizen": SeniorCitizen,
        "Partner": Partner,
        "Dependents": Dependents,
        "tenure": tenure,
        "PhoneService": PhoneService,
        "MultipleLines": MultipleLines,
        "InternetService": InternetService,
        "OnlineSecurity": OnlineSecurity,
        "OnlineBackup": OnlineBackup,
        "DeviceProtection": DeviceProtection,
        "TechSupport": TechSupport,
        "StreamingTV": StreamingTV,
        "StreamingMovies": StreamingMovies,
        "Contract": Contract,
        "PaperlessBilling": PaperlessBilling,
        "PaymentMethod": PaymentMethod,
        "MonthlyCharges": MonthlyCharges,
        "TotalCharges": TotalCharges,
    }

    response = endpoint.predict([instance])
    pred = response.predictions[0]

    churn_prob = pred['scores'][1]
    not_churn_prob = pred['scores'][0]
    predicted_class = "Churn" if churn_prob > 0.5 else "Not Churn"

    st.subheader("🔮 Prediction Results")
    st.write(f"**Predicted Class:** {predicted_class}")
    st.write(f"**Churn Probability:** {churn_prob*100:.2f}%")
    st.write(f"**Not Churn Probability:** {not_churn_prob*100:.2f}%")

    # Color indicator
    if churn_prob > 0.75:
        st.error("High Risk of Churn ⚠️")
    elif churn_prob > 0.5:
        st.warning("Moderate Risk of Churn 🟡")
    else:
        st.success("Low Risk of Churn ✅")
