import streamlit as st
import pandas as pd
import re
from datetime import date

def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

from database import *
from ai_prediction import predict

create_table()

st.set_page_config(page_title="AI Health App", layout="wide")

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

    data = get_patients()

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

    fullname = st.text_input("Full Name")
    dob = st.date_input("Date of Birth", max_value=date.today())
    email = st.text_input("Email")
    glucose = st.number_input("Glucose")
    haemoglobin = st.number_input("Haemoglobin")
    cholesterol = st.number_input("Cholesterol")

    if st.button("Predict & Save"):

        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if fullname.strip() == "":
            st.error("Full Name is required")

        elif not re.match(email_regex, email):
            st.error("Invalid Email")

        elif glucose <= 0:
            st.error("Glucose must be positive")

        elif haemoglobin <= 0:
            st.error("Haemoglobin must be positive")

        elif cholesterol <= 0:
            st.error("Cholesterol must be positive")

        else:
            with st.spinner("Analyzing health data..."):

                remarks = predict(
                    glucose,
                    haemoglobin,
                    cholesterol
                )

                insert_patient((
                    fullname,
                    str(dob),
                    email,
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

    data = get_patients()

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
            delete_patient(pid)
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

    data = get_patients()

    if data:

        # Select patient ID
        patient_ids = [row[0] for row in data]
        selected_id = st.selectbox("Select Patient ID", patient_ids)

        # Get selected patient
        selected_patient = None
        for row in data:
            if row[0] == selected_id:
                selected_patient = row
                break

        if selected_patient:

            fullname = st.text_input("Full Name", selected_patient[1])
            dob = st.date_input("Date of Birth", value=pd.to_datetime(selected_patient[2]))
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

                        update_patient(
                            selected_id,
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

    else:
        st.warning("No patient records found.")