import requests

BASE_URL = "http://127.0.0.1:8000" 


def test_get_patients():
    response = requests.get(f"{BASE_URL}/patients/")
    print("GET /patients:")
    print("Status Code:", response.status_code)
    print("Response Body:", response.json())

def test_get_patient(patient_id):
    response = requests.get(f"{BASE_URL}/patients/{patient_id}")
    print(f"GET /patients/{patient_id}:")
    print("Status Code:", response.status_code)
    print("Response Body:", response.json())

def test_create_patient(patient_data):
    response = requests.post(f"{BASE_URL}/patients/", json=patient_data)
    print("POST /patients:")
    print("Status Code:", response.status_code)
    print("Response Body:", response.json())
    return response.json()

def test_update_patient(patient_id, patient_data):
    response = requests.put(f"{BASE_URL}/patients/{patient_id}", json=patient_data)
    print(f"PUT /patients/{patient_id}:")
    print("Status Code:", response.status_code)
    print("Response Body:", response.json())

def test_delete_patient(patient_id):
    response = requests.delete(f"{BASE_URL}/patients/{patient_id}")
    print(f"DELETE /patients/{patient_id}:")
    print("Status Code:", response.status_code)
    print("Response Body:", response.json())



def test_get_doctors():
    response = requests.get(f"{BASE_URL}/doctors/")
    print("GET /doctors:")
    print("Status Code:", response.status_code)
    print("Response Body:", response.json())

def test_get_doctor(doctor_id):
    response = requests.get(f"{BASE_URL}/doctors/{doctor_id}")
    print(f"GET /doctors/{doctor_id}:")
    print("Status Code:", response.status_code)
    print("Response Body:", response.json())

def test_create_doctor(doctor_data):
    response = requests.post(f"{BASE_URL}/doctors/", json=doctor_data)
    print("POST /doctors:")
    print("Status Code:", response.status_code)
    print("Response Body:", response.json())
    return response.json()

def test_update_doctor(doctor_id, doctor_data):
    response = requests.put(f"{BASE_URL}/doctors/{doctor_id}", json=doctor_data)
    print(f"PUT /doctors/{doctor_id}:")
    print("Status Code:", response.status_code)
    print("Response Body:", response.json())

def test_delete_doctor(doctor_id):
    response = requests.delete(f"{BASE_URL}/doctors/{doctor_id}")
    print(f"DELETE /doctors/{doctor_id}:")
    print("Status Code:", response.status_code)
    print("Response Body:", response.json())



def test_get_appointments():
    response = requests.get(f"{BASE_URL}/appointments/")
    print("GET /appointments:")
    print("Status Code:", response.status_code)
    print("Response Body:", response.json())

def test_get_appointment(appointment_id):
    response = requests.get(f"{BASE_URL}/appointments/{appointment_id}")
    print(f"GET /appointments/{appointment_id}:")
    print("Status Code:", response.status_code)
    print("Response Body:", response.json())

def test_create_appointment(appointment_data):
    response = requests.post(f"{BASE_URL}/appointments/", json=appointment_data)
    print("POST /appointments:")
    print("Status Code:", response.status_code)
    print("Response Body:", response.json())
    return response.json()

def test_update_appointment(appointment_id, appointment_data):
    response = requests.put(f"{BASE_URL}/appointments/{appointment_id}", json=appointment_data)
    print(f"PUT /appointments/{appointment_id}:")
    print("Status Code:", response.status_code)
    print("Response Body:", response.json())

def test_delete_appointment(appointment_id):
    response = requests.delete(f"{BASE_URL}/appointments/{appointment_id}")
    print(f"DELETE /appointments/{appointment_id}:")
    print("Status Code:", response.status_code)
    print("Response Body:", response.json())


if __name__ == "__main__":
    new_patient = {
        "full_name": "Иванова Мария Алексеевна",
        "gender": "Ж",
        "birth_date": "1990-12-01",
        "phone": "+7-996-555-78-98",
        "email": "maria@example.com"
    }


    new_doctor = {
        "full_name": "Петров Михаил Владимирович",
        "specialty_id": 1,
        "clinic_id": 1,
        "category": "Высшая",
        "experience": 11
    }

    
    new_appointment = {
        "patient_id": 2,
        "doctor_id": 4,
        "appointment_date": "2025-10-01",
        "appointment_time": "09:00",
        "notes": "Проверка давления"
    }


    print("\n--- Testing Patients API ---")
    test_get_patients()
    created_patient_response = test_create_patient(new_patient)
    
    if created_patient_response is not None:
        patient_id = created_patient_response['id']
        test_get_patient(patient_id)
        update_patient_data = {
            "full_name": "Иванова Екатерина Алексеевна",
            "gender": None,
            "birth_date": None,
            "phone": None,
            "email": None
        }
        test_update_patient(patient_id, update_patient_data)
        test_delete_patient(patient_id)



    print("\n--- Testing Doctors API ---")
    test_get_doctors()
    created_doctor_response = test_create_doctor(new_doctor)
    
    if created_doctor_response is not None:
        doctor_id = created_doctor_response['id']
        test_get_doctor(doctor_id)
        update_doctor_data = {
            "full_name": "Петров Алексей Владимирович",
            "specialty_id": None,
            "clinic_id": None,
            "category": None,
            "experience": None
        }
        test_update_doctor(doctor_id, update_doctor_data)
        test_delete_doctor(doctor_id)


    
    print("\n--- Testing Appointments API ---")
    test_get_appointments()
    created_appointment_response = test_create_appointment(new_appointment)
    
    if created_appointment_response is not None:
        appointment_id = created_appointment_response['id']
        test_get_appointment(appointment_id)
        update_appointment_data = {
            "status": "completed",
            "notes": "Прием завершен, пациент здоров"
        }
        test_update_appointment(appointment_id, update_appointment_data)
        test_delete_appointment(appointment_id)
