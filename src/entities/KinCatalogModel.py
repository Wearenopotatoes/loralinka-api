# src/entities/kin_catalog.py
from sqlalchemy import Column, Integer, String
from .BaseEntity import Base

class KinCatalog(Base):
    __tablename__ = "kin_catalog"

    kin_id = Column(Integer, primary_key=True, autoincrement=True)
    kin_name = Column(String(255), nullable=True)
