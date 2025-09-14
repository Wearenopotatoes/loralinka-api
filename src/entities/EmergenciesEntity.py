# src/entities/emergencies.py
from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, Numeric, CheckConstraint, func
from sqlalchemy.orm import relationship
from .BaseEntity import Base

class Emergencies(Base):
    __tablename__ = "emergencies"
    __table_args__ = (
        CheckConstraint("status IN (1, 2, 3)", name="chk_emergencies_status"),
    )

    emergency_id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(TIMESTAMP, nullable=False, server_default=func.now())
    tipo_accidente = Column(Integer, ForeignKey("accident_types.accident_type_id"), nullable=True)
    assigned_unit = Column(Integer, ForeignKey("emergency_unit.emergency_unit_id"), nullable=True)
    latitud = Column(Numeric(8, 6), nullable=False)
    longitud = Column(Numeric(9, 6), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    status = Column(Integer, nullable=False, server_default="1")

    accident_type = relationship("AccidentTypes", back_populates="emergencies")
    assigned_unit_rel = relationship("EmergencyUnit", back_populates="emergencies")
    user = relationship("Users", back_populates="emergencies")
