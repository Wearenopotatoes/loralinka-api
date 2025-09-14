# src/entities/accident_types.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .BaseEntity import Base

class AccidentTypes(Base):
    __tablename__ = "accident_types"

    accident_type_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), nullable=True)

    emergencies = relationship("Emergencies", back_populates="accident_type")
