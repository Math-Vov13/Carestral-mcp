"""SQLAlchemy ORM models for NeonDB database."""

from datetime import datetime

from sqlalchemy import (
    ARRAY,
    Column,
    DateTime,
    Double,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    """User model."""

    __tablename__ = "User"
    __table_args__ = {'extend_existing': True}

    id = Column(Text, primary_key=True)
    email = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    firstname = Column(Text)
    surname = Column(Text)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    age = Column(Integer)
    phoneNumber = Column(Text)
    reservationCount = Column(Integer, default=0)
    sex = Column(Text)
    profileCompletedAt = Column(DateTime)

    # Relationships
    appointments = relationship("Appointment", back_populates="user")
    bookings = relationship("Booking", back_populates="user")
    mcps = relationship("MCP", back_populates="user")
    temp_tokens = relationship("TempToken", back_populates="user")


class Hospital(Base):
    """Hospital model."""

    __tablename__ = "Hospital"
    __table_args__ = {'extend_existing': True}

    id = Column(Text, primary_key=True)
    name = Column(Text, nullable=False)
    city = Column(Text)
    distanceKm = Column(Double)
    address = Column(Text)
    phoneNumber = Column(Text)
    email = Column(Text)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    appointments = relationship("Appointment", back_populates="hospital")
    hospital_statuses = relationship("HospitalStatus", back_populates="hospital")


class Appointment(Base):
    """Appointment model."""

    __tablename__ = "Appointment"
    __table_args__ = {'extend_existing': True}

    id = Column(Text, primary_key=True)
    userId = Column(Text, ForeignKey("User.id"), nullable=False)
    hospitalId = Column(Text, ForeignKey("Hospital.id"), nullable=False)
    patientId = Column(Text)
    description = Column(Text)
    date = Column(Text)
    time = Column(Text)
    status = Column(Text)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="appointments")
    hospital = relationship("Hospital", back_populates="appointments")


class Booking(Base):
    """Booking model."""

    __tablename__ = "Booking"
    __table_args__ = {'extend_existing': True}

    id = Column(Text, primary_key=True)
    userId = Column(Text, ForeignKey("User.id"), nullable=False)
    description = Column(Text)
    hospital = Column(Text)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="bookings")


class HospitalStatus(Base):
    """HospitalStatus model."""

    __tablename__ = "HospitalStatus"
    __table_args__ = {'extend_existing': True}

    id = Column(Text, primary_key=True)
    hospitalId = Column(Text, ForeignKey("Hospital.id"), nullable=False)
    availableBeds = Column(Integer)
    icuBeds = Column(Integer)
    ventilators = Column(Integer)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    hospital = relationship("Hospital", back_populates="hospital_statuses")


class MCP(Base):
    """MCP model."""

    __tablename__ = "MCP"
    __table_args__ = {'extend_existing': True}

    id = Column(Text, primary_key=True)
    userId = Column(Text, ForeignKey("User.id"), nullable=False)
    tokenMcp = Column(Text)
    createdAt = Column(DateTime, default=datetime.utcnow)
    expiresAt = Column(DateTime)
    name = Column(Text)
    scopes = Column(ARRAY(Text))

    # Relationships
    user = relationship("User", back_populates="mcps")


class TempToken(Base):
    """TempToken model."""

    __tablename__ = "TempToken"
    __table_args__ = {'extend_existing': True}

    id = Column(Text, primary_key=True)
    token = Column(Text, nullable=False)
    userId = Column(Text, ForeignKey("User.id"), nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    expiresAt = Column(DateTime)

    # Relationships
    user = relationship("User", back_populates="temp_tokens")
