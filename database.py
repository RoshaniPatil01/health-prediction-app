import sqlite3

DB_NAME = "patients.db"


def connect():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = connect()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        dob TEXT,
        email TEXT,
        glucose REAL,
        haemoglobin REAL,
        cholesterol REAL,
        remarks TEXT
    )
    """)
    conn.commit()
    conn.close()


def insert_patient(data):
    conn = connect()
    conn.execute("""
    INSERT INTO patients
    (fullname, dob, email, glucose, haemoglobin, cholesterol, remarks)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()


def get_patients():
    conn = connect()
    rows = conn.execute("SELECT * FROM patients").fetchall()
    conn.close()
    return rows


def delete_patient(pid):
    conn = connect()
    conn.execute("DELETE FROM patients WHERE id=?", (pid,))
    conn.commit()
    conn.close()


def update_patient(pid, data):
    conn = connect()

    conn.execute("""
    UPDATE patients
    SET fullname=?,
        dob=?,
        email=?,
        glucose=?,
        haemoglobin=?,
        cholesterol=?,
        remarks=?
    WHERE id=?
    """,
    (
        data[0],
        data[1],
        data[2],
        data[3],
        data[4],
        data[5],
        data[6],
        pid
    ))

    conn.commit()
    conn.close()