# src/entities/emergency_unit.py
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from .BaseEntity import Base

class EmergencyUnit(Base):
    __tablename__ = "emergency_unit"

    emergency_unit_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    latitud = Column(Numeric(8, 6), nullable=False)
    longitud = Column(Numeric(9, 6), nullable=False)

    emergencies = relationship("Emergencies", back_populates="assigned_unit_rel")
