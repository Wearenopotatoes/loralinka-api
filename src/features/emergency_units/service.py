from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from src.entities.EmergencyUnitEntity import EmergencyUnit
from src.entities.EmergenciesEntity import Emergencies
from .model import EmergencyUnitCreate, EmergencyUnitUpdate


def create_emergency_unit(db: Session, unit_in: EmergencyUnitCreate) -> EmergencyUnit:
    """Create a new emergency unit."""
    unit = EmergencyUnit(
        name=unit_in.name,
        latitud=unit_in.latitud,
        longitud=unit_in.longitud
    )
    db.add(unit)
    db.commit()
    db.refresh(unit)
    return unit


def get_emergency_unit(db: Session, unit_id: int) -> Optional[EmergencyUnit]:
    """Get an emergency unit by ID."""
    return db.get(EmergencyUnit, unit_id)


def get_emergency_unit_by_name(db: Session, name: str) -> Optional[EmergencyUnit]:
    """Get an emergency unit by name."""
    stmt = select(EmergencyUnit).where(EmergencyUnit.name == name)
    return db.execute(stmt).scalar_one_or_none()


def list_emergency_units(db: Session, skip: int = 0, limit: int = 100) -> List[EmergencyUnit]:
    """List all emergency units with pagination."""
    stmt = select(EmergencyUnit).offset(skip).limit(limit).order_by(EmergencyUnit.name)
    return list(db.execute(stmt).scalars().all())


def update_emergency_unit(db: Session, unit_id: int, unit_in: EmergencyUnitUpdate) -> Optional[EmergencyUnit]:
    """Update an emergency unit."""
    unit = db.get(EmergencyUnit, unit_id)
    if not unit:
        return None

    if unit_in.name is not None:
        unit.name = unit_in.name
    if unit_in.latitud is not None:
        unit.latitud = unit_in.latitud
    if unit_in.longitud is not None:
        unit.longitud = unit_in.longitud

    db.add(unit)
    db.commit()
    db.refresh(unit)
    return unit


def delete_emergency_unit(db: Session, unit_id: int) -> bool:
    """Delete an emergency unit."""
    unit = db.get(EmergencyUnit, unit_id)
    if not unit:
        return False

    db.delete(unit)
    db.commit()
    return True


def get_emergency_unit_stats(db: Session, unit_id: int) -> dict:
    """Get statistics for an emergency unit."""
    # Count active emergencies (status 1 or 2)
    active_emergencies_stmt = select(func.count(Emergencies.emergency_id)).where(
        Emergencies.assigned_unit == unit_id,
        Emergencies.status.in_([1, 2])
    )
    active_count = db.execute(active_emergencies_stmt).scalar() or 0

    # Count total emergencies
    total_emergencies_stmt = select(func.count(Emergencies.emergency_id)).where(
        Emergencies.assigned_unit == unit_id
    )
    total_count = db.execute(total_emergencies_stmt).scalar() or 0

    return {
        "active_emergencies": active_count,
        "total_emergencies": total_count
    }


def search_emergency_units_by_location(db: Session, latitude: float, longitude: float, radius_km: float = 10.0) -> List[EmergencyUnit]:
    """Find emergency units within a specified radius from a location."""
    # Simple distance calculation (this could be improved with PostGIS)
    # For now, using a basic bounding box approach
    lat_delta = radius_km / 111.0  # Roughly 111 km per degree of latitude
    lon_delta = radius_km / (111.0 * abs(latitude))  # Adjust longitude for latitude

    stmt = select(EmergencyUnit).where(
        EmergencyUnit.latitud.between(latitude - lat_delta, latitude + lat_delta),
        EmergencyUnit.longitud.between(longitude - lon_delta, longitude + lon_delta)
    ).order_by(EmergencyUnit.name)

    return list(db.execute(stmt).scalars().all())