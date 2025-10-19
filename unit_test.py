import unittest
import requests
import time
from datetime import date, timedelta


class TestMedicalSystemAPI(unittest.TestCase):
    BASE_URL = "http://localhost:8000"
    
    def setUp(self):
        self.timestamp = int(time.time())
    

    def test_01_get_patients(self):
        print("Тест 1: Получение списка пациентов")
        response = requests.get(f"{self.BASE_URL}/patients/")
        print(f"   GET /patients/ - статус: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        print("   Успешно получен список пациентов")

    def test_02_create_and_delete_patient(self):
        print("Тест 2: Создание и удаление пациента")

        data = {
            'full_name': f'Иванов Иван Иванович {self.timestamp}',
            'gender': 'М',
            'birth_date': '1990-01-01',
            'phone': f'+7-999-{self.timestamp}',
            'email': f'ivanov{self.timestamp}@mail.ru'
        }
        response = requests.post(f"{self.BASE_URL}/patients/", json=data)
        print(f"   POST /patients/ - статус: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        
        patient_id = response.json().get('id')
        print(f"   Пациент успешно создан с ID: {patient_id}")
        
    
        delete_response = requests.delete(f"{self.BASE_URL}/patients/{patient_id}")
        print(f"   DELETE /patients/{patient_id} - статус: {delete_response.status_code}")
        self.assertEqual(delete_response.status_code, 200)
        print("   Пациент успешно удален")

    def test_03_get_doctors(self):
        print("Тест 3: Получение списка врачей")
        response = requests.get(f"{self.BASE_URL}/doctors/")
        print(f"   GET /doctors/ - статус: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        print("   Успешно получен список врачей")

    def test_04_create_and_delete_doctor(self):
        print("Тест 4: Создание и удаление врача")

        data = {
            'full_name': f'Петров Петр Сергеевич {self.timestamp}',
            'specialty_id': 1,
            'clinic_id': 1,
            'category': 'Терапевт',
            'experience': 5
        }
        response = requests.post(f"{self.BASE_URL}/doctors/", json=data)
        print(f"   POST /doctors/ - статус: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        
        doctor_id = response.json().get('id')
        print(f"   Врач успешно создан с ID: {doctor_id}")
        

        delete_response = requests.delete(f"{self.BASE_URL}/doctors/{doctor_id}")
        print(f"   DELETE /doctors/{doctor_id} - статус: {delete_response.status_code}")
        self.assertEqual(delete_response.status_code, 200)
        print("   Врач успешно удален")

    def test_05_get_appointments(self):
        print("Тест 5: Получение списка записей")
        response = requests.get(f"{self.BASE_URL}/appointments/")
        print(f"   GET /appointments/ - статус: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        print("   Успешно получен список записей")

    def test_06_create_and_delete_appointment(self):
        print("Тест 6: Создание и удаление записи на прием")
    
        patient_data = {
            'full_name': f'Сидорова Анна Михайловна {self.timestamp}',
            'gender': 'Ж',
            'birth_date': '1985-03-15'
        }
        patient_response = requests.post(f"{self.BASE_URL}/patients/", json=patient_data)
        patient_id = patient_response.json().get('id')
        print(f"   Создан пациент с ID: {patient_id}")
        
    
        doctor_data = {
            'full_name': f'Козлова Ольга Владимировна {self.timestamp}',
            'specialty_id': 1,
            'clinic_id': 1
        }
        doctor_response = requests.post(f"{self.BASE_URL}/doctors/", json=doctor_data)
        doctor_id = doctor_response.json().get('id')
        print(f"   Создан врач с ID: {doctor_id}")
        
    
        appointment_data = {
            'patient_id': patient_id,
            'doctor_id': doctor_id,
            'appointment_date': str(date.today() + timedelta(days=1)),
            'appointment_time': '10:00',
            'notes': f'Плановый осмотр {self.timestamp}'
        }
        
        response = requests.post(f"{self.BASE_URL}/appointments/", json=appointment_data)
        print(f"   POST /appointments/ - статус: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        
        appointment_id = response.json().get('id')
        print(f"   Запись на прием успешно создана с ID: {appointment_id}")
        

        delete_response = requests.delete(f"{self.BASE_URL}/appointments/{appointment_id}")
        print(f"   DELETE /appointments/{appointment_id} - статус: {delete_response.status_code}")
        self.assertEqual(delete_response.status_code, 200)
        print("   Запись успешно удалена")
        

        requests.delete(f"{self.BASE_URL}/patients/{patient_id}")
        requests.delete(f"{self.BASE_URL}/doctors/{doctor_id}")
        print("   Пациент и врач также удалены")

    def test_07_get_patient_by_id(self):
        print("Тест 7: Получение пациента по ID")

        patient_data = {
            'full_name': f'Николаев Дмитрий Петрович {self.timestamp}',
            'gender': 'М',
            'birth_date': '1995-05-15'
        }
        create_response = requests.post(f"{self.BASE_URL}/patients/", json=patient_data)
        patient_id = create_response.json().get('id')
        print(f"   Создан пациент с ID: {patient_id}")
        

        response = requests.get(f"{self.BASE_URL}/patients/{patient_id}")
        print(f"   GET /patients/{patient_id} - статус: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        print("   Пациент по ID успешно получен")
        

        requests.delete(f"{self.BASE_URL}/patients/{patient_id}")
        print("   Пациент удален")

    def test_08_get_doctor_by_id(self):
        print("Тест 8: Получение врача по ID")
    
        doctor_data = {
            'full_name': f'Волкова Екатерина Игоревна {self.timestamp}',
            'specialty_id': 1,
            'clinic_id': 1
        }
        create_response = requests.post(f"{self.BASE_URL}/doctors/", json=doctor_data)
        doctor_id = create_response.json().get('id')
        print(f"   Создан врач с ID: {doctor_id}")
        
    
        response = requests.get(f"{self.BASE_URL}/doctors/{doctor_id}")
        print(f"   GET /doctors/{doctor_id} - статус: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        print("   Врач по ID успешно получен")
        
    
        requests.delete(f"{self.BASE_URL}/doctors/{doctor_id}")
        print("   Врач удален")

    def test_09_update_patient(self):
        print("Тест 9: Обновление пациента")
        patient_data = {
            'full_name': f'Алексеев Михаил Викторович {self.timestamp}',
            'gender': 'М',
            'birth_date': '1990-01-01'
        }
        create_response = requests.post(f"{self.BASE_URL}/patients/", json=patient_data)
        patient_id = create_response.json().get('id')
        print(f"   Создан пациент с ID: {patient_id}")
        

        update_data = {
            'full_name': f'Алексеев Михаил Викторович (обновлено) {self.timestamp}',
            'phone': '+7-888-888-88-88'
        }
        response = requests.put(f"{self.BASE_URL}/patients/{patient_id}", json=update_data)
        print(f"   PUT /patients/{patient_id} - статус: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        print("   Пациент успешно обновлен")
        

        requests.delete(f"{self.BASE_URL}/patients/{patient_id}")
        print("   Пациент удален")

    def test_10_update_doctor(self):
        print("Тест 10: Обновление врача")

        doctor_data = {
            'full_name': f'Орлов Сергей Александрович {self.timestamp}',
            'specialty_id': 1,
            'clinic_id': 1
        }
        create_response = requests.post(f"{self.BASE_URL}/doctors/", json=doctor_data)
        doctor_id = create_response.json().get('id')
        print(f"   Создан врач с ID: {doctor_id}")
        

        update_data = {
            'category': 'Высшая категория',
            'experience': 10
        }
        response = requests.put(f"{self.BASE_URL}/doctors/{doctor_id}", json=update_data)
        print(f"   PUT /doctors/{doctor_id} - статус: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        print("   Врач успешно обновлен")
        

        requests.delete(f"{self.BASE_URL}/doctors/{doctor_id}")
        print("   Врач удален")


if __name__ == '__main__':
    print("ЗАПУСК ТЕСТОВ СИСТЕМЫ ЗАПИСИ К ВРАЧУ")
    print("=" * 50)
    unittest.main(verbosity=2)