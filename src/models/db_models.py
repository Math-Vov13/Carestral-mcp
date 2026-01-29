from pydantic import BaseModel


class Patient(BaseModel):
    id: str
    name: str
    age: int
    city: str
    medical_history: list[str]

class Hospital(BaseModel):
    id: str
    name: str
    city: str
    distance_km: float

class AppointmentRequest(BaseModel):
    patient_id: str
    hospital_id: str
    date: str
    time: str

class HospitalStatus(BaseModel):
    hospital_id: str
    available_beds: int
    icu_beds: int
    ventilators: int
