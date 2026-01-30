from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    """User model - matches database schema"""
    id: str
    email: str
    firstname: Optional[str] = None
    surname: Optional[str] = None
    age: Optional[int] = None
    phoneNumber: Optional[str] = None
    reservationCount: Optional[int] = 0
    sex: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None


class Hospital(BaseModel):
    """Hospital model - matches database schema"""
    id: str
    name: str
    city: Optional[str] = None
    distanceKm: Optional[float] = None
    address: Optional[str] = None
    phoneNumber: Optional[str] = None
    email: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None


class AppointmentRequest(BaseModel):
    """Request model for creating appointments"""
    hospital_name: str
    date: str
    time: str


class Appointment(BaseModel):
    """Appointment model - matches database schema"""
    id: str
    userId: str
    hospitalId: str
    patientId: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    status: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None


class HospitalStatus(BaseModel):
    """Hospital status model - matches database schema"""
    id: Optional[str] = None
    hospitalId: str
    availableBeds: Optional[int] = None
    icuBeds: Optional[int] = None
    ventilators: Optional[int] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
