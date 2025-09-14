from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class EmergencyContactCreate(BaseModel):
    contact_phone: Optional[str] = Field(None, max_length=20)
    kin: Optional[int] = None
    contact_name: Optional[str] = Field(None, max_length=255)


class UserBase(BaseModel):
    name: str = Field(..., max_length=255)
    phone: str = Field(..., max_length=20)
    birthday: Optional[date] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=1, max_length=255)
    emergency_contacts: Optional[List[EmergencyContactCreate]] = Field(default_factory=list)
    medical_condition_ids: Optional[List[int]] = Field(default_factory=list)


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    birthday: Optional[date] = None
    password: Optional[str] = Field(None, min_length=1, max_length=255)


class EmergencyContactOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    contact_id: int
    contact_phone: Optional[str] = None
    kin: Optional[int] = None
    contact_name: Optional[str] = None


class MedicalConditionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    medical_condition_id: int
    description: Optional[str] = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    name: str
    phone: str
    birthday: Optional[date] = None
    created_at: datetime
    emergency_contacts: List[EmergencyContactOut] = []
    conditions: List[MedicalConditionOut] = []


class LoginRequest(BaseModel):
    phone: str = Field(..., max_length=20)
    password: str = Field(..., min_length=1, max_length=255)