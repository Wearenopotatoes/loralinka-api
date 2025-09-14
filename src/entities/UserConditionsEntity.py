# src/entities/user_conditions.py
from sqlalchemy import Column, Integer, ForeignKey
from .BaseEntity import Base

class UserConditions(Base):
    __tablename__ = "user_conditions"

    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    medical_condition_id = Column(
        Integer,
        ForeignKey("medical_conditions.medical_condition_id"),
        primary_key=True,
    )
