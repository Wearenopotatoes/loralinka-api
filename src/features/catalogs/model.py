from typing import List
from pydantic import BaseModel, ConfigDict


class MedicalConditionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    medical_condition_id: int
    description: str | None = None


class KinCatalogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    kin_id: int
    kin_name: str | None = None


class AccidentTypeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    accident_type_id: int
    description: str | None = None


class EmergencyUnitOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    emergency_unit_id: int
    name: str
    latitud: float
    longitud: float