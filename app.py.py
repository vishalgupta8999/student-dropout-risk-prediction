import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("student_dropout_model.pkl")

# Title
st.title("Student Dropout Risk Prediction")

# Student inputs
attendance = st.number_input("Attendance (%)")
marks = st.number_input("Marks")
study_hours = st.number_input("Study Hours")
backlogs = st.number_input("Backlogs", min_value=0, step=1)
previous_failures = st.number_input("Previous Failures", min_value=0, step=1)
assignments = st.number_input("Assignment (%)")

fees = st.selectbox("Fees Pending?", ["No", "Yes"])

# Prediction button
if st.button("Predict Risk"):

    # Convert fees into 0 and 1
    if fees == "Yes":
        fees_pending = 1
    else:
        fees_pending = 0

    # Create student data
    student = pd.DataFrame([[
        attendance,
        marks,
        study_hours,
        backlogs,
        previous_failures,
        assignments,
        fees_pending
    ]], columns=[
        "Attendance",
        "Marks",
        "Study_Hours",
        "Backlogs",
        "Previous_Failures",
        "Assignments",
        "Fees_Pending"
    ])

    # Predict
    prediction = model.predict(student)[0]

    # Display prediction
    st.write("Predicted Risk:", prediction)

    # Generate reasons
    reasons = []

    if attendance < 75:
        reasons.append("Attendance is below 75%")

    if marks < 50:
        reasons.append("Marks are below 50%")

    if study_hours < 2:
        reasons.append("Study hours are low")

    if backlogs > 0:
        reasons.append("Student has backlogs")

    if previous_failures > 0:
        reasons.append("Student has previous failures")

    if assignments < 60:
        reasons.append("Assignment performance is low")

    if fees_pending == 1:
        reasons.append("Fees are pending")

    # Display reasons
    st.write("Reasons:")

    if len(reasons) == 0:
        st.write("No major risk indicators found.")
    else:
        for reason in reasons:
            st.write("-", reason)