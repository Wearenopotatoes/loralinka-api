from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class EmergencyUnitCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Nombre de la unidad de emergencia")
    latitud: float = Field(..., ge=-90, le=90, description="Latitud de la ubicación de la unidad")
    longitud: float = Field(..., ge=-180, le=180, description="Longitud de la ubicación de la unidad")


class EmergencyUnitUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Nombre de la unidad de emergencia")
    latitud: Optional[float] = Field(None, ge=-90, le=90, description="Latitud de la ubicación de la unidad")
    longitud: Optional[float] = Field(None, ge=-180, le=180, description="Longitud de la ubicación de la unidad")


class EmergencyUnitOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    emergency_unit_id: int
    name: str
    latitud: float
    longitud: float
    
    assigned_emergency_id: Optional[int] = None


class EmergencyUnitWithStats(EmergencyUnitOut):
    """Emergency unit with additional statistics"""
    active_emergencies: int = Field(default=0, description="Número de emergencias activas asignadas")
    total_emergencies: int = Field(default=0, description="Total de emergencias atendidas")