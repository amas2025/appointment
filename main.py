import streamlit as st
import pandas as pd
from datetime import date, datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials

# Google Drive Folder ID
GOOGLE_DRIVE_FOLDER_ID = "1C3-yfqeYAi90wCA6KXosm5YBOW_zWiB_"
# Path to your service account key file
SERVICE_ACCOUNT_FILE = "service_account.json"

# Authenticate with Google Drive API
def authenticate_google_drive():
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    drive_service = build('drive', 'v3', credentials=credentials)
    return drive_service

# Upload file to Google Drive
def upload_to_google_drive(file_name, folder_id):
    drive_service = authenticate_google_drive()
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_name, mimetype='text/csv')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

# Set up the page title
st.set_page_config(page_title="Appointment Booking System")
st.title("Appointment Booking System")

# Introduction
st.markdown("Please fill out the form below to schedule an appointment.")

# Form to collect user information
with st.form("appointment_form"):
    st.subheader("Personal Information")
    full_name = st.text_input("Full Name", placeholder="Required")
    phone_number = st.text_input("Phone Number (e.g., 07xxxxxxxxx)", placeholder="Required", help="Enter a valid Iraqi phone number starting with 07.")
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
        elif not phone_number.startswith("07") or len(phone_number) != 11 or not phone_number.isdigit():
            st.error("Please enter a valid Iraqi phone number.")
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

            # Save to a local CSV file
            csv_file_name = "appointments.csv"
            try:
                df.to_csv(csv_file_name, mode="a", index=False, header=False)

                # Upload to Google Drive
                file_id = upload_to_google_drive(csv_file_name, GOOGLE_DRIVE_FOLDER_ID)
                st.success(f"Your appointment has been booked successfully! File ID: {file_id}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Hide the display of existing appointments
st.markdown("### Scheduled Appointments")
st.info("Appointment data is stored internally and uploaded to Google Drive.")
