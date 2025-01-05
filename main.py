import streamlit as st
import pandas as pd
from datetime import date, datetime

# Set up the page title
st.set_page_config(page_title="Appointment Booking System")
st.title("Appointment Booking System")

# Introduction
st.markdown("Please fill out the form below to schedule an appointment.")

# Form to collect user information
with st.form("appointment_form"):
    st.subheader("Personal Information")
    full_name = st.text_input("Full Name", placeholder="Required")
    phone_number = st.text_input("Phone Number", placeholder="Required")
    gender = st.radio("Gender", ("Male", "Female", "Other"))
    age = st.number_input("Age", min_value=18, max_value=60, step=1)

    st.subheader("Appointment Details")
    appointment_date = st.date_input("Select a Date", min_value=date.today())
    appointment_time = st.time_input("Select a Time")
    topic = st.text_area("Topic of Discussion")

    # Submit button
    submitted = st.form_submit_button("Submit")

    if submitted:
        if not full_name.strip() or not phone_number.strip() or not topic.strip():
            st.error("Please fill in all the required fields.")
        else:
            # Save appointment data
            data = {
                "Full Name": full_name,
                "Phone Number": phone_number,
                "Gender": gender,
                "Age": age,
                "Appointment Date": appointment_date,
                "Appointment Time": appointment_time.strftime("%H:%M"),
                "Topic": topic,
            }
            df = pd.DataFrame([data])

            # Save to a CSV file
            try:
                df.to_csv("appointments.csv", mode="a", index=False, header=False)
                st.success("Your appointment has been booked successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Display existing appointments
st.subheader("Scheduled Appointments")
try:
    appointments = pd.read_csv("appointments.csv", names=[
        "Full Name", "Phone Number", "Gender", "Age", "Appointment Date", "Appointment Time", "Topic"
    ])
    st.dataframe(appointments)
except FileNotFoundError:
    st.info("No appointments have been scheduled yet.")
