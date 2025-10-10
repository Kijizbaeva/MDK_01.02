from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import pyodbc

app = FastAPI()


def get_db():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-PJMJ60V\SQLEXPRESS;'
        'DATABASE=MedicalBooking;'
        'Trusted_Connection=yes;'
    )
    return conn


class Patient(BaseModel):
    id: int
    full_name: str
    gender: str
    birth_date: str
    phone: Optional[str] = None
    email: Optional[str] = None

class PatientCreate(BaseModel):
    full_name: str
    gender: str
    birth_date: str
    phone: Optional[str] = None
    email: Optional[str] = None

class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class Doctor(BaseModel):
    id: int
    full_name: str
    specialty_id: int
    clinic_id: int
    category: Optional[str] = None
    experience: Optional[int] = None

class DoctorCreate(BaseModel):
    full_name: str
    specialty_id: int
    clinic_id: int
    category: Optional[str] = None
    experience: Optional[int] = None

class DoctorUpdate(BaseModel):
    full_name: Optional[str] = None
    specialty_id: Optional[int] = None
    clinic_id: Optional[int] = None
    category: Optional[str] = None
    experience: Optional[int] = None

class Appointment(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_date: str
    appointment_time: str
    status: str

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: str
    appointment_time: str
    notes: Optional[str] = None

class AppointmentUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None


@app.get("/patients/", response_model=List[Patient])
def get_patients():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, gender, birth_date, phone, email FROM patients")
    patients = []
    for row in cursor.fetchall():
        patients.append(Patient(
            id=row.id,
            full_name=row.full_name,
            gender=row.gender,
            birth_date=str(row.birth_date),
            phone=row.phone,
            email=row.email
        ))
    conn.close()
    return patients

@app.get("/patients/{patient_id}", response_model=Patient)
def get_patient(patient_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, gender, birth_date, phone, email FROM patients WHERE id = ?", patient_id)
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return Patient(
        id=row.id,
        full_name=row.full_name,
        gender=row.gender,
        birth_date=str(row.birth_date),
        phone=row.phone,
        email=row.email
    )

@app.post("/patients/", response_model=Patient)
def create_patient(patient: PatientCreate):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO patients (full_name, gender, birth_date, phone, email) OUTPUT INSERTED.id VALUES (?, ?, ?, ?, ?)",
        patient.full_name, patient.gender, patient.birth_date, patient.phone, patient.email
    )
    
    patient_id = cursor.fetchone()[0]
    conn.commit()
    
    
    cursor.execute("SELECT id, full_name, gender, birth_date, phone, email FROM patients WHERE id = ?", patient_id)
    row = cursor.fetchone()
    conn.close()
    
    return Patient(
        id=row.id,
        full_name=row.full_name,
        gender=row.gender,
        birth_date=str(row.birth_date),
        phone=row.phone,
        email=row.email
    )

@app.put("/patients/{patient_id}", response_model=Patient)
def update_patient(patient_id: int, patient: PatientUpdate):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM patients WHERE id = ?", patient_id)
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Patient not found")
    
    
    update_fields = []
    params = []
    
    if patient.full_name is not None:
        update_fields.append("full_name = ?")
        params.append(patient.full_name)
    if patient.gender is not None:
        update_fields.append("gender = ?")
        params.append(patient.gender)
    if patient.birth_date is not None:
        update_fields.append("birth_date = ?")
        params.append(patient.birth_date)
    if patient.phone is not None:
        update_fields.append("phone = ?")
        params.append(patient.phone)
    if patient.email is not None:
        update_fields.append("email = ?")
        params.append(patient.email)
    
    if update_fields:
        params.append(patient_id)
        query = f"UPDATE patients SET {', '.join(update_fields)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
    

    cursor.execute("SELECT id, full_name, gender, birth_date, phone, email FROM patients WHERE id = ?", patient_id)
    row = cursor.fetchone()
    conn.close()
    
    return Patient(
        id=row.id,
        full_name=row.full_name,
        gender=row.gender,
        birth_date=str(row.birth_date),
        phone=row.phone,
        email=row.email
    )

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    conn = get_db()
    cursor = conn.cursor()
    

    cursor.execute("SELECT id FROM appointments WHERE patient_id = ?", patient_id)
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Cannot delete patient with existing appointments")
    
    cursor.execute("DELETE FROM patients WHERE id = ?", patient_id)
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Patient not found")
    
    conn.close()
    return {"message": "Patient deleted successfully"}


@app.get("/doctors/", response_model=List[Doctor])
def get_doctors():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, specialty_id, clinic_id, category, experience FROM doctors")
    doctors = []
    for row in cursor.fetchall():
        doctors.append(Doctor(
            id=row.id,
            full_name=row.full_name,
            specialty_id=row.specialty_id,
            clinic_id=row.clinic_id,
            category=row.category,
            experience=row.experience 
        ))
    conn.close()
    return doctors

@app.get("/doctors/{doctor_id}", response_model=Doctor)
def get_doctor(doctor_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, specialty_id, clinic_id, category, experience FROM doctors WHERE id = ?", doctor_id)
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    return Doctor(
        id=row.id,
        full_name=row.full_name,
        specialty_id=row.specialty_id,
        clinic_id=row.clinic_id,
        category=row.category,
        experience=row.experience
    )

@app.post("/doctors/", response_model=Doctor)
def create_doctor(doctor: DoctorCreate):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO doctors (full_name, specialty_id, clinic_id, category, experience) OUTPUT INSERTED.id VALUES (?, ?, ?, ?, ?)",
        doctor.full_name, doctor.specialty_id, doctor.clinic_id, doctor.category, doctor.experience 
    )
    
    doctor_id = cursor.fetchone()[0]
    conn.commit()
    
    cursor.execute("SELECT id, full_name, specialty_id, clinic_id, category, experience FROM doctors WHERE id = ?", doctor_id)
    row = cursor.fetchone()
    conn.close()
    
    return Doctor(
        id=row.id,
        full_name=row.full_name,
        specialty_id=row.specialty_id,
        clinic_id=row.clinic_id,
        category=row.category,
        experience=row.experience
    )


@app.put("/doctors/{doctor_id}", response_model=Doctor)
def update_doctor(doctor_id: int, doctor: DoctorUpdate):
    conn = get_db()
    cursor = conn.cursor()
    
    
    cursor.execute("SELECT id FROM doctors WHERE id = ?", doctor_id)
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    
    update_fields = []
    params = []
    
    if doctor.full_name is not None:
        update_fields.append("full_name = ?")
        params.append(doctor.full_name)
    if doctor.specialty_id is not None:
        update_fields.append("specialty_id = ?")
        params.append(doctor.specialty_id)
    if doctor.clinic_id is not None:
        update_fields.append("clinic_id = ?")
        params.append(doctor.clinic_id)
    if doctor.category is not None:
        update_fields.append("category = ?")
        params.append(doctor.category)
    if doctor.experience is not None:
        update_fields.append("experience = ?")
        params.append(doctor.experience)
    
    if update_fields:
        params.append(doctor_id)
        query = f"UPDATE doctors SET {', '.join(update_fields)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
    

    cursor.execute("SELECT id, full_name, specialty_id, clinic_id, category, experience FROM doctors WHERE id = ?", doctor_id)
    row = cursor.fetchone()
    conn.close()
    
    return Doctor(
        id=row.id,
        full_name=row.full_name,
        specialty_id=row.specialty_id,
        clinic_id=row.clinic_id,
        category=row.category,
        experience=row.experience
    )

@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int):
    conn = get_db()
    cursor = conn.cursor()
    
    
    cursor.execute("SELECT id FROM appointments WHERE doctor_id = ?", doctor_id)
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Cannot delete doctor with existing appointments")
    
    
    cursor.execute("DELETE FROM work_schedules WHERE doctor_id = ?", doctor_id)
    cursor.execute("DELETE FROM doctors WHERE id = ?", doctor_id)
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    conn.close()
    return {"message": "Doctor deleted successfully"}


@app.get("/appointments/", response_model=List[Appointment])
def get_appointments():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, patient_id, doctor_id, appointment_date, appointment_time, status FROM appointments")
    appointments = []
    for row in cursor.fetchall():
        appointments.append(Appointment(
            id=row.id,
            patient_id=row.patient_id,
            doctor_id=row.doctor_id,
            appointment_date=str(row.appointment_date),
            appointment_time=str(row.appointment_time),
            status=row.status
        ))
    conn.close()
    return appointments

@app.get("/appointments/{appointment_id}", response_model=Appointment)
def get_appointment(appointment_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, patient_id, doctor_id, appointment_date, appointment_time, status FROM appointments WHERE id = ?", appointment_id)
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    return Appointment(
        id=row.id,
        patient_id=row.patient_id,
        doctor_id=row.doctor_id,
        appointment_date=str(row.appointment_date),
        appointment_time=str(row.appointment_time),
        status=row.status
    )

@app.post("/appointments/", response_model=Appointment)
def create_appointment(appointment: AppointmentCreate):
    conn = get_db()
    cursor = conn.cursor()
    
    
    cursor.execute("SELECT id FROM patients WHERE id = ?", appointment.patient_id)
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Patient not found")
    
    cursor.execute("SELECT id FROM doctors WHERE id = ?", appointment.doctor_id)
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    
    cursor.execute(
        "SELECT id FROM appointments WHERE doctor_id = ? AND appointment_date = ? AND appointment_time = ? AND status != 'cancelled'",
        appointment.doctor_id, appointment.appointment_date, appointment.appointment_time
    )
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="This time slot is already booked")
    
    cursor.execute(
        "INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, notes) OUTPUT INSERTED.id VALUES (?, ?, ?, ?, ?)",
        appointment.patient_id, appointment.doctor_id, appointment.appointment_date, appointment.appointment_time, appointment.notes
    )
    
    appointment_id = cursor.fetchone()[0]
    conn.commit()
    
    cursor.execute("SELECT id, patient_id, doctor_id, appointment_date, appointment_time, status FROM appointments WHERE id = ?", appointment_id)
    row = cursor.fetchone()
    conn.close()
    
    return Appointment(
        id=row.id,
        patient_id=row.patient_id,
        doctor_id=row.doctor_id,
        appointment_date=str(row.appointment_date),
        appointment_time=str(row.appointment_time),
        status=row.status
    )

@app.put("/appointments/{appointment_id}", response_model=Appointment)
def update_appointment(appointment_id: int, appointment: AppointmentUpdate):
    conn = get_db()
    cursor = conn.cursor()
    
    
    cursor.execute("SELECT id FROM appointments WHERE id = ?", appointment_id)
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    
    update_fields = []
    params = []
    
    if appointment.status is not None:
        update_fields.append("status = ?")
        params.append(appointment.status)
    if appointment.notes is not None:
        update_fields.append("notes = ?")
        params.append(appointment.notes)
    
    if update_fields:
        params.append(appointment_id)
        query = f"UPDATE appointments SET {', '.join(update_fields)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
    

    cursor.execute("SELECT id, patient_id, doctor_id, appointment_date, appointment_time, status FROM appointments WHERE id = ?", appointment_id)
    row = cursor.fetchone()
    conn.close()
    
    return Appointment(
        id=row.id,
        patient_id=row.patient_id,
        doctor_id=row.doctor_id,
        appointment_date=str(row.appointment_date),
        appointment_time=str(row.appointment_time),
        status=row.status
    )

@app.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM appointments WHERE id = ?", appointment_id)
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    conn.close()
    return {"message": "Appointment deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)