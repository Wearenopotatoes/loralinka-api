from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class AccidentTypeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    accident_type_id: int
    description: Optional[str] = None


class EmergencyUnitOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    emergency_unit_id: int
    name: str
    latitud: float
    longitud: float


class UserBasicOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    user_id: int
    name: str
    phone: str


class EmergencyCreate(BaseModel):
    timestamp: Optional[datetime] = None
    tipo_accidente: Optional[int] = Field(None, description="ID del tipo de accidente")
    assigned_unit: Optional[int] = Field(None, description="ID de la unidad de emergencia asignada")
    latitud: float = Field(..., description="Latitud de la emergencia")
    longitud: float = Field(..., description="Longitud de la emergencia")
    user_id: Optional[int] = Field(None, description="ID del usuario que reporta")
    status: int = Field(default=1, ge=1, le=3, description="Estado: 1=pendiente, 2=en curso, 3=cerrada")


class EmergencyUpdate(BaseModel):
    assigned_unit: Optional[int] = None
    status: Optional[int] = Field(None, ge=1, le=3)


class EmergencyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    emergency_id: int
    timestamp: datetime
    tipo_accidente: Optional[int] = None
    assigned_unit: Optional[int] = None
    latitud: float
    longitud: float
    user_id: Optional[int] = None
    status: int
    
    # Relaciones opcionales con modelos específicos
    accident_type: Optional[AccidentTypeOut] = None
    assigned_unit_rel: Optional[EmergencyUnitOut] = None
    user: Optional[UserBasicOut] = None