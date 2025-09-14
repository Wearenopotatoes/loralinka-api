from typing import List

from fastapi import APIRouter, HTTPException, status, Query
from src.database.db import DbSession

from .model import EmergencyCreate, EmergencyUpdate, EmergencyOut
from . import service

router = APIRouter(prefix="/emergencies", tags=["emergencies"])


@router.post(
    "",
    response_model=EmergencyOut,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva emergencia"
)
def create_emergency(emergency: EmergencyCreate, db: DbSession) -> EmergencyOut:
    """Crea una nueva emergencia con los datos del usuario y la emergencia."""
    new_emergency = service.create_emergency(db, emergency)
    return EmergencyOut.model_validate(new_emergency)


@router.get(
    "/{emergency_id}",
    response_model=EmergencyOut,
    summary="Obtener datos de una emergencia"
)
def get_emergency(emergency_id: int, db: DbSession) -> EmergencyOut:
    """Obtiene todos los datos de una emergencia espec�fica."""
    emergency = service.get_emergency(db, emergency_id)
    if not emergency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency not found"
        )
    return EmergencyOut.model_validate(emergency)


@router.get(
    "",
    response_model=List[EmergencyOut],
    summary="Listar emergencias"
)
def list_emergencies(
    db: DbSession,
    skip: int = Query(0, ge=0, description="N�mero de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="N�mero m�ximo de registros"),
    status_filter: int = Query(None, ge=1, le=3, description="Filtrar por estado")
) -> List[EmergencyOut]:
    """Lista todas las emergencias con paginaci�n y filtros opcionales."""
    if status_filter is not None:
        emergencies = service.get_emergencies_by_status(db, status_filter)
    else:
        emergencies = service.list_emergencies(db, skip=skip, limit=limit)
    
    return [EmergencyOut.model_validate(emergency) for emergency in emergencies]


@router.put(
    "/{emergency_id}/assign-unit",
    response_model=EmergencyOut,
    summary="Asignar unidad de emergencia"
)
def assign_unit_to_emergency(
    emergency_id: int,
    unit_id: int,
    db: DbSession
) -> EmergencyOut:
    """Asigna una unidad de emergencia espec�fica a una emergencia."""
    emergency = service.assign_unit_to_emergency(db, emergency_id, unit_id)
    if not emergency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency not found"
        )
    return EmergencyOut.model_validate(emergency)


@router.put(
    "/{emergency_id}",
    response_model=EmergencyOut,
    summary="Actualizar emergencia"
)
def update_emergency(
    emergency_id: int,
    emergency_update: EmergencyUpdate,
    db: DbSession
) -> EmergencyOut:
    """Actualiza los datos de una emergencia (unidad asignada y/o estado)."""
    emergency = service.update_emergency(db, emergency_id, emergency_update)
    if not emergency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency not found"
        )
    return EmergencyOut.model_validate(emergency)


@router.get(
    "/user/{user_id}",
    response_model=List[EmergencyOut],
    summary="Obtener emergencias de un usuario"
)
def get_emergencies_by_user(user_id: int, db: DbSession) -> List[EmergencyOut]:
    """Obtiene todas las emergencias reportadas por un usuario espec�fico."""
    emergencies = service.get_emergencies_by_user(db, user_id)
    return [EmergencyOut.model_validate(emergency) for emergency in emergencies]