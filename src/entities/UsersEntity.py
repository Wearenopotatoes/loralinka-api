# src/entities/users.py
from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, func
from sqlalchemy.orm import relationship
from .BaseEntity import Base
from .UserConditionsEntity import UserConditions
from .MedicalConditionsEntity import MedicalConditions  # Ensure class is registered

class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    birthday = Column(Date, nullable=True)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    # Relaciones
    conditions = relationship(
        "MedicalConditions",
        secondary=UserConditions.__table__,
        back_populates="users",
        cascade="save-update",
    )
    emergency_contacts = relationship(
        "EmergencyContacts",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    emergencies = relationship(
        "Emergencies",
        back_populates="user",
        cascade="save-update",
    )
