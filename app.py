
import streamlit as st
import pandas as pd
import re
from datetime import date
import importlib

# 1. ALWAYS SET PAGE CONFIG FIRST
st.set_page_config(page_title="AI Health App", layout="wide")

# 2. LOAD YOUR CSS AFTER THE PAGE IS CONFIGURED
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

import database
importlib.reload(database)
from ai_prediction import predict

database.create_table()

# st.title("🏥 AI Health Prediction System")
st.title("🏥 AI Health Prediction System")
st.markdown("### Smart analysis of blood test reports using AI logic")

menu = st.sidebar.selectbox("Menu", ["Dashboard", "Add Patient", "View Patients", "Update Patient"])

# ---------------- DASHBOARD ----------------
# if menu == "Dashboard":

#     st.subheader("📊 Dashboard")

#     data = get_patients()

#     total_patients = len(data)

#     st.metric("Total Patients", total_patients)



if menu == "Dashboard":

    st.subheader("📊 Health Dashboard")

    data = database.get_patients()

    total_patients = len(data)

    if total_patients > 0:

        total_glucose = sum(float(row[4]) for row in data)
        total_hb = sum(float(row[5]) for row in data)
        total_cholesterol = sum(float(row[6]) for row in data)

        avg_glucose = total_glucose / total_patients
        avg_hb = total_hb / total_patients
        avg_cholesterol = total_cholesterol / total_patients

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Patients",
            total_patients
        )

        col2.metric(
            "Avg Glucose",
            round(avg_glucose, 2)
        )

        col3.metric(
            "Avg Hb",
            round(avg_hb, 2)
        )

        col4.metric(
            "Avg Cholesterol",
            round(avg_cholesterol, 2)
        )

    else:
        st.warning("No patient records available.")


# ---------------- ADD PATIENT ----------------

elif menu == "Add Patient":

    st.subheader("Enter Patient Details")

    with st.form("patient_form"):

        fullname = st.text_input("Full Name")

        dob = st.date_input(
            "Date of Birth",
            value=date.today(),
            min_value=date(1900, 1, 1),
            max_value=date.today()
        )

        email = st.text_input("Email")
        glucose = st.number_input("Glucose", min_value=0.0)
        haemoglobin = st.number_input("Haemoglobin", min_value=0.0)
        cholesterol = st.number_input("Cholesterol", min_value=0.0)

        submit = st.form_submit_button("Predict & Save")

    if submit:

        email_clean = email.strip().lower()

        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        if not fullname.strip():
            st.error("Full Name is required")

        elif not email_clean:
            st.error("Email is required")

        elif not re.match(email_regex, email_clean):
            st.error("Invalid Email")

        elif database.patient_exists(email_clean):
            st.warning("⚠️ Patient already exists with this email")

        elif glucose <= 0:
            st.error("Glucose must be positive")

        elif haemoglobin <= 0:
            st.error("Haemoglobin must be positive")

        elif cholesterol <= 0:
            st.error("Cholesterol must be positive")

        else:
            with st.spinner("Analyzing health data..."):

                remarks = predict(glucose, haemoglobin, cholesterol)

                database.insert_patient((
                    fullname,
                    str(dob),
                    email_clean,
                    glucose,
                    haemoglobin,
                    cholesterol,
                    remarks
                ))

            st.success("Patient Saved Successfully")
            st.info(remarks)

# ---------------- VIEW PATIENTS ----------------
# else:

#     st.subheader("Patient Records")

#     data = get_patients()

#     if data:
#         for row in data:
#             st.write(row)

#         pid = st.number_input("Enter ID to delete", min_value=1)

#         if st.button("Delete"):
#             delete_patient(pid)
#             st.success("Deleted Successfully")



elif menu == "View Patients":

    st.subheader("📋 Patient Records")

    data = database.get_patients()
    if data:

        # Convert to DataFrame
        df = pd.DataFrame(
            data,
            columns=[
                "ID",
                "Name",
                "DOB",
                "Email",
                "Glucose",
                "Haemoglobin",
                "Cholesterol",
                "Remarks"
            ]
        )

        # Search
        search = st.text_input("🔍 Search Patient")

        if search:
            df = df[df["Name"].str.lower().str.contains(search.lower())]

        if df.empty:
            st.warning("No matching patients found")
        else:
            st.dataframe(df, use_container_width=True)

            # ---------------- CSV DOWNLOAD ----------------
            csv = df.to_csv(index=False)

            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name="patients.csv",
                mime="text/csv"
            )

        st.markdown("---")

        pid = st.number_input(
            "Enter Patient ID to Delete",
            min_value=1
        )

        if st.button("Delete Record"):
            database.delete_patient(pid)
            st.success("Deleted Successfully")

    else:
        st.warning("No patient records found.")

# ---------------- UPDATE PATIENT ----------------
# elif menu == "Update Patient":

#     st.subheader("✏️ Update Patient")

#     st.info(
#         "Update functionality can be added later. "
#         "Current project already demonstrates Create, Read and Delete operations."
#     )


elif menu == "Update Patient":

    st.subheader("✏️ Update Patient Record")

    data = database.get_patients()

    if data:

    # Get all patient IDs
        patient_ids = [str(row[0]) for row in data]

    # # Show available IDs
    # st.write("Available Patient IDs:", ", ".join(patient_ids))

    # User enters ID
    entered_id = st.text_input("Enter Patient ID")

    # Check if ID exists
    if entered_id:
        if entered_id not in patient_ids:
            st.warning("⚠️ Patient ID does not exist.")
        else:
            st.success("✅ Patient ID found.")
        
        # Get selected patient
        selected_patient = None
        for row in data:
            if str(row[0]) == entered_id:
                selected_patient = row
                break

        # Continue with your update form here

        if selected_patient:

            fullname = st.text_input("Full Name", selected_patient[1])
            # dob = st.date_input("Date of Birth", value=pd.to_datetime(selected_patient[2]))
            dob = st.date_input(
                        "Date of Birth",
                        value=date.today(),
                        min_value=date(1900, 1, 1),
                        max_value=date.today()
                    )
            email = st.text_input("Email", selected_patient[3])
            glucose = st.number_input("Glucose", value=float(selected_patient[4]))
            haemoglobin = st.number_input("Haemoglobin", value=float(selected_patient[5]))
            cholesterol = st.number_input("Cholesterol", value=float(selected_patient[6]))

            if st.button("Update & Recalculate"):

                email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

                if fullname.strip() == "":
                    st.error("Name required")

                elif not re.match(email_regex, email):
                    st.error("Invalid Email")

                elif glucose <= 0 or haemoglobin <= 0 or cholesterol <= 0:
                    st.error("Blood values must be positive")

                else:
                    with st.spinner("Recalculating AI prediction..."):

                        remarks = predict(glucose, haemoglobin, cholesterol)

                        database.update_patient(
                            int(entered_id),
                            (
                                fullname,
                                str(dob),
                                email,
                                glucose,
                                haemoglobin,
                                cholesterol,
                                remarks
                            )
                        )

                    st.success("Patient Updated Successfully")
                    st.info(remarks)

    # else:
    #     st.warning("No patient records found.")