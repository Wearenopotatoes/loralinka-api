from typing import List

from fastapi import APIRouter, HTTPException, status
from src.database.db import DbSession

from .model import MedicalConditionOut, KinCatalogOut, AccidentTypeOut, EmergencyUnitOut
from . import service

router = APIRouter(prefix="/catalogs", tags=["catalogs"])


@router.get(
    "/medical-conditions",
    response_model=List[MedicalConditionOut],
    summary="Get all medical conditions"
)
def get_medical_conditions(db: DbSession) -> List[MedicalConditionOut]:
    conditions = service.get_all_medical_conditions(db)
    return [MedicalConditionOut.model_validate(condition) for condition in conditions]


@router.get(
    "/medical-conditions/{condition_id}",
    response_model=MedicalConditionOut,
    summary="Get medical condition by ID"
)
def get_medical_condition(condition_id: int, db: DbSession) -> MedicalConditionOut:
    condition = service.get_medical_condition(db, condition_id)
    if not condition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Medical condition not found"
        )
    return MedicalConditionOut.model_validate(condition)


@router.get(
    "/kin-catalog",
    response_model=List[KinCatalogOut],
    summary="Get all kin/relationship types"
)
def get_kin_catalog(db: DbSession) -> List[KinCatalogOut]:
    kin_types = service.get_all_kin_catalog(db)
    return [KinCatalogOut.model_validate(kin) for kin in kin_types]


@router.get(
    "/kin-catalog/{kin_id}",
    response_model=KinCatalogOut,
    summary="Get kin/relationship type by ID"
)
def get_kin_catalog_item(kin_id: int, db: DbSession) -> KinCatalogOut:
    kin = service.get_kin_catalog(db, kin_id)
    if not kin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kin catalog item not found"
        )
    return KinCatalogOut.model_validate(kin)


@router.get(
    "/accident-types",
    response_model=List[AccidentTypeOut],
    summary="Get all accident types"
)
def get_accident_types(db: DbSession) -> List[AccidentTypeOut]:
    accident_types = service.get_all_accident_types(db)
    return [AccidentTypeOut.model_validate(accident) for accident in accident_types]


@router.get(
    "/accident-types/{accident_type_id}",
    response_model=AccidentTypeOut,
    summary="Get accident type by ID"
)
def get_accident_type(accident_type_id: int, db: DbSession) -> AccidentTypeOut:
    accident = service.get_accident_type(db, accident_type_id)
    if not accident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accident type not found"
        )
    return AccidentTypeOut.model_validate(accident)


@router.get(
    "/emergency-units",
    response_model=List[EmergencyUnitOut],
    summary="Get all emergency units"
)
def get_emergency_units(db: DbSession) -> List[EmergencyUnitOut]:
    units = service.get_all_emergency_units(db)
    return [EmergencyUnitOut.model_validate(unit) for unit in units]


@router.get(
    "/emergency-units/{unit_id}",
    response_model=EmergencyUnitOut,
    summary="Get emergency unit by ID"
)
def get_emergency_unit(unit_id: int, db: DbSession) -> EmergencyUnitOut:
    unit = service.get_emergency_unit(db, unit_id)
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency unit not found"
        )
    return EmergencyUnitOut.model_validate(unit)