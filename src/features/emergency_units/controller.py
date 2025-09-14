from typing import List

from fastapi import APIRouter, HTTPException, status, Query
from src.database.db import DbSession

from .model import EmergencyUnitCreate, EmergencyUnitUpdate, EmergencyUnitOut, EmergencyUnitWithStats
from . import service

router = APIRouter(prefix="/emergency-units", tags=["emergency-units"])


@router.post(
    "",
    response_model=EmergencyUnitOut,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nueva unidad de emergencia"
)
def create_emergency_unit(unit: EmergencyUnitCreate, db: DbSession) -> EmergencyUnitOut:
    """Registra una nueva unidad de emergencia con su ubicación."""
    # Check if unit name already exists
    existing_unit = service.get_emergency_unit_by_name(db, unit.name)
    if existing_unit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Emergency unit with name '{unit.name}' already exists"
        )

    new_unit = service.create_emergency_unit(db, unit)
    return EmergencyUnitOut.model_validate(new_unit)


@router.get(
    "/{unit_id}",
    response_model=EmergencyUnitOut,
    summary="Obtener datos de una unidad de emergencia"
)
def get_emergency_unit(unit_id: int, db: DbSession) -> EmergencyUnitOut:
    """Obtiene los datos de una unidad de emergencia específica."""
    unit = service.get_emergency_unit(db, unit_id)
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency unit not found"
        )
    return EmergencyUnitOut.model_validate(unit)


@router.get(
    "/{unit_id}/stats",
    response_model=EmergencyUnitWithStats,
    summary="Obtener unidad de emergencia con estadísticas"
)
def get_emergency_unit_with_stats(unit_id: int, db: DbSession) -> EmergencyUnitWithStats:
    """Obtiene los datos de una unidad de emergencia con estadísticas de emergencias."""
    unit = service.get_emergency_unit(db, unit_id)
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency unit not found"
        )

    stats = service.get_emergency_unit_stats(db, unit_id)
    unit_data = EmergencyUnitOut.model_validate(unit).model_dump()
    unit_data.update(stats)

    return EmergencyUnitWithStats.model_validate(unit_data)


@router.get(
    "",
    response_model=List[EmergencyUnitOut],
    summary="Listar unidades de emergencia"
)
def list_emergency_units(
    db: DbSession,
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros")
) -> List[EmergencyUnitOut]:
    """Lista todas las unidades de emergencia con paginación."""
    units = service.list_emergency_units(db, skip=skip, limit=limit)
    return [EmergencyUnitOut.model_validate(unit) for unit in units]


@router.get(
    "/search/nearby",
    response_model=List[EmergencyUnitOut],
    summary="Buscar unidades de emergencia cercanas"
)
def search_nearby_emergency_units(
    latitude: float = Query(..., ge=-90, le=90, description="Latitud de referencia"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitud de referencia"),
    radius_km: float = Query(10.0, ge=0.1, le=100, description="Radio de búsqueda en kilómetros"),
    db: DbSession = None
) -> List[EmergencyUnitOut]:
    """Busca unidades de emergencia dentro de un radio específico desde una ubicación."""
    units = service.search_emergency_units_by_location(db, latitude, longitude, radius_km)
    return [EmergencyUnitOut.model_validate(unit) for unit in units]


@router.put(
    "/{unit_id}",
    response_model=EmergencyUnitOut,
    summary="Actualizar unidad de emergencia"
)
def update_emergency_unit(
    unit_id: int,
    unit_update: EmergencyUnitUpdate,
    db: DbSession
) -> EmergencyUnitOut:
    """Actualiza los datos de una unidad de emergencia."""
    # Check if new name already exists (if name is being updated)
    if unit_update.name:
        existing_unit = service.get_emergency_unit_by_name(db, unit_update.name)
        if existing_unit and existing_unit.emergency_unit_id != unit_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Emergency unit with name '{unit_update.name}' already exists"
            )

    unit = service.update_emergency_unit(db, unit_id, unit_update)
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency unit not found"
        )
    return EmergencyUnitOut.model_validate(unit)


@router.delete(
    "/{unit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar unidad de emergencia"
)
def delete_emergency_unit(unit_id: int, db: DbSession):
    """Elimina una unidad de emergencia."""
    success = service.delete_emergency_unit(db, unit_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency unit not found"
        )