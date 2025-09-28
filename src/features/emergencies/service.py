# src/features/emergencies/service.py

from typing import List, Optional
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from datetime import datetime

from src.entities.EmergenciesEntity import Emergencies
# --- 1. Importamos la entidad de la unidad ---
from src.entities.EmergencyUnitEntity import EmergencyUnit 
from .model import EmergencyCreate, EmergencyUpdate


# --- FUNCIÓN PARA ASIGNAR UNIDAD (MODIFICADA) ---
def assign_unit_to_emergency(db: Session, emergency_id: int, unit_id: int) -> Optional[Emergencies]:
    emergency = db.get(Emergencies, emergency_id)
    # Buscamos la unidad para poder modificarla
    unit = db.get(EmergencyUnit, unit_id)

    if not emergency or not unit:
        return None
    
    # Asignamos la unidad a la emergencia
    emergency.assigned_unit = unit_id
    emergency.status = 2 # Cambiamos el estado a "asignada"

    # --- LÓGICA AÑADIDA ---
    # Marcamos la unidad como "ocupada" con el ID de esta emergencia
    unit.assigned_emergency_id = emergency_id
    # --- FIN DE LA LÓGICA AÑADIDA ---

    db.add(emergency)
    db.add(unit) # Añadimos la unidad a la sesión para guardar sus cambios
    db.commit()
    db.refresh(emergency)
    return emergency


# --- FUNCIÓN PARA ACTUALIZAR EMERGENCIA (MODIFICADA) ---
def update_emergency(db: Session, emergency_id: int, emergency_in: EmergencyUpdate) -> Optional[Emergencies]:
    emergency = db.get(Emergencies, emergency_id)
    if not emergency:
        return None
    
    # --- LÓGICA AÑADIDA ---
    # Verificamos si el estado está cambiando a 3 (cerrada)
    if emergency_in.status == 3 and emergency.assigned_unit is not None:
        # Si es así, buscamos la unidad que estaba asignada
        unit_to_release = db.get(EmergencyUnit, emergency.assigned_unit)
        if unit_to_release:
            # Y la liberamos poniendo su campo en NULL
            unit_to_release.assigned_emergency_id = None
            db.add(unit_to_release)
    # --- FIN DE LA LÓGICA AÑADIDA ---
    
    if emergency_in.assigned_unit is not None:
        emergency.assigned_unit = emergency_in.assigned_unit
    if emergency_in.status is not None:
        emergency.status = emergency_in.status
    
    db.add(emergency)
    db.commit()
    db.refresh(emergency)
    return emergency


def create_emergency(db: Session, emergency_in: EmergencyCreate) -> Emergencies:
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