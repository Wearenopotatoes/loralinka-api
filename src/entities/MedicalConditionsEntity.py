# src/entities/medical_conditions.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .BaseEntity import Base
from .UserConditionsEntity import UserConditions

class MedicalConditions(Base):
    __tablename__ = "medical_conditions"

    medical_condition_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), nullable=True)

    # Relación many-to-many con Users mediante tabla intermedia user_conditions
    users = relationship(
        "Users",
        secondary=UserConditions.__table__,
        back_populates="conditions",
    )
