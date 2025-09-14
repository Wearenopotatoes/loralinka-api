# src/entities/emergency_contacts.py
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .BaseEntity import Base

class EmergencyContacts(Base):
    __tablename__ = "emergency_contacts"
    # PK compuesta (user_id, contact_phone). contact_id existe pero no es PK.
    __table_args__ = (
        UniqueConstraint("user_id", "contact_phone", name="pk_emergency_contacts"),
    )

    contact_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    contact_phone = Column(String(20), nullable=True)
    kin = Column(Integer, ForeignKey("kin_catalog.kin_id"), nullable=True)
    contact_name = Column(String(255), nullable=True)

    user = relationship("Users", back_populates="emergency_contacts")
