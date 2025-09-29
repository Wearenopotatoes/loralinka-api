from typing import List, Optional
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, func
from datetime import datetime

from src.entities.EmergenciesEntity import Emergencies
from .model import EmergencyCreate, EmergencyUpdate


def create_emergency(db: Session, emergency_in: EmergencyCreate) -> Emergencies:
    # Usar timestamp proporcionado o datetime.now() si es None
    timestamp = emergency_in.timestamp or datetime.now()
    
    emergency = Emergencies(
        timestamp=timestamp,
        tipo_accidente=emergency_in.tipo_accidente,
        assigned_unit=emergency_in.assigned_unit,
        latitud=emergency_in.latitud,
        longitud=emergency_in.longitud,
        user_id=emergency_in.user_id,
        status=emergency_in.status,
    )
    db.add(emergency)
    db.commit()
    db.refresh(emergency)
    return emergency


def get_emergency(db: Session, emergency_id: int) -> Optional[Emergencies]:
    stmt = select(Emergencies).where(Emergencies.emergency_id == emergency_id).options(
        selectinload(Emergencies.accident_type),
        selectinload(Emergencies.assigned_unit_rel),
        selectinload(Emergencies.user)
    )
    return db.execute(stmt).scalar_one_or_none()


def list_emergencies(db: Session, skip: int = 0, limit: int = 100) -> List[Emergencies]:
    stmt = select(Emergencies).options(
        selectinload(Emergencies.accident_type),
        selectinload(Emergencies.assigned_unit_rel),
        selectinload(Emergencies.user)
    ).offset(skip).limit(limit).order_by(Emergencies.timestamp.desc())
    return list(db.execute(stmt).scalars().all())


def update_emergency(db: Session, emergency_id: int, emergency_in: EmergencyUpdate) -> Optional[Emergencies]:
    emergency = db.get(Emergencies, emergency_id)
    if not emergency:
        return None
    
    if emergency_in.assigned_unit is not None:
        emergency.assigned_unit = emergency_in.assigned_unit
    if emergency_in.status is not None:
        emergency.status = emergency_in.status
    
    db.add(emergency)
    db.commit()
    db.refresh(emergency)
    return emergency


def assign_unit_to_emergency(db: Session, emergency_id: int, unit_id: int) -> Optional[Emergencies]:
    emergency = db.get(Emergencies, emergency_id)
    if not emergency:
        return None
    
    emergency.assigned_unit = unit_id
    db.add(emergency)
    db.commit()
    db.refresh(emergency)
    return emergency


def get_emergencies_by_user(db: Session, user_id: int) -> List[Emergencies]:
    stmt = select(Emergencies).where(Emergencies.user_id == user_id).options(
        selectinload(Emergencies.accident_type),
        selectinload(Emergencies.assigned_unit_rel),
        selectinload(Emergencies.user)
    ).order_by(Emergencies.timestamp.desc())
    return list(db.execute(stmt).scalars().all())


def get_emergencies_by_status(db: Session, status: int) -> List[Emergencies]:
    stmt = select(Emergencies).where(Emergencies.status == status).options(
        selectinload(Emergencies.accident_type),
        selectinload(Emergencies.assigned_unit_rel),
        selectinload(Emergencies.user)
    ).order_by(Emergencies.timestamp.desc())
    return list(db.execute(stmt).scalars().all())