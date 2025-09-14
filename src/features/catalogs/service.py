from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.entities.MedicalConditionsEntity import MedicalConditions
from src.entities.KinCatalogModel import KinCatalog
from src.entities.AccidentTypesEntity import AccidentTypes
from src.entities.EmergencyUnitEntity import EmergencyUnit


def get_all_medical_conditions(db: Session) -> List[MedicalConditions]:
    stmt = select(MedicalConditions).order_by(MedicalConditions.medical_condition_id)
    return list(db.execute(stmt).scalars().all())


def get_medical_condition(db: Session, condition_id: int) -> MedicalConditions | None:
    return db.get(MedicalConditions, condition_id)


def get_all_kin_catalog(db: Session) -> List[KinCatalog]:
    stmt = select(KinCatalog).order_by(KinCatalog.kin_id)
    return list(db.execute(stmt).scalars().all())


def get_kin_catalog(db: Session, kin_id: int) -> KinCatalog | None:
    return db.get(KinCatalog, kin_id)


def get_all_accident_types(db: Session) -> List[AccidentTypes]:
    stmt = select(AccidentTypes).order_by(AccidentTypes.accident_type_id)
    return list(db.execute(stmt).scalars().all())


def get_accident_type(db: Session, accident_type_id: int) -> AccidentTypes | None:
    return db.get(AccidentTypes, accident_type_id)


def get_all_emergency_units(db: Session) -> List[EmergencyUnit]:
    stmt = select(EmergencyUnit).order_by(EmergencyUnit.emergency_unit_id)
    return list(db.execute(stmt).scalars().all())


def get_emergency_unit(db: Session, unit_id: int) -> EmergencyUnit | None:
    return db.get(EmergencyUnit, unit_id)
