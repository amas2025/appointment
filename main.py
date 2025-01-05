import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Configuration (Replace these with your own values)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "meriwanmirany1991@gmail.com"
EMAIL_PASSWORD = "your_email_password"
NOTIFICATION_EMAIL = "meriwanmirany1991@gmail.com"

# Function to send email
def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = NOTIFICATION_EMAIL
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

    except Exception as e:
        st.error(f"Error sending email: {e}")

# Streamlit App
def main():
    st.title("Supplier Appointment Booking")

    st.header("Fill in your details to book an appointment")

    with st.form("appointment_form"):
        # Personal details
        full_name = st.text_input("Full Name", "")
        phone_number = st.text_input("Phone Number", "")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        age = st.number_input("Age", min_value=1, max_value=120, step=1)

        # Appointment details
        appointment_date = st.date_input("Select a Date")
        appointment_time = st.time_input("Select a Time")
        topic = st.text_area("What do you want to talk about?")

        submitted = st.form_submit_button("Book Appointment")

    if submitted:
        if not full_name or not phone_number or not topic:
            st.error("Please fill out all required fields!")
        else:
            # Save or process the appointment details
            email_subject = f"New Appointment from {full_name}"
            email_body = (
                f"New appointment details:\n\n"
                f"Full Name: {full_name}\n"
                f"Phone Number: {phone_number}\n"
                f"Gender: {gender}\n"
                f"Age: {age}\n"
                f"Date: {appointment_date}\n"
                f"Time: {appointment_time}\n"
                f"Topic: {topic}\n"
            )

            # Send email notification
            send_email(email_subject, email_body)
            
            st.success("Your appointment has been booked. We will contact you soon!")

if __name__ == "__main__":
    main()
