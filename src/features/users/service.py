from __future__ import annotations

import hashlib
from typing import List, Optional

from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select

from src.entities.UsersEntity import Users
from src.entities.EmergencyContactsEntity import EmergencyContacts
from src.entities.UserConditionsEntity import UserConditions
from .model import UserCreate, UserUpdate


def _hash_password(password: str) -> str:
    # Hash simple con SHA-256 (placeholder); reemplazar por un hash fuerte si se requiere.
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_user(db: Session, user_in: UserCreate) -> Users:
    # Crear el usuario
    user = Users(
        name=user_in.name,
        phone=user_in.phone,
        birthday=user_in.birthday,
        password=_hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Crear contactos de emergencia si fueron proporcionados
    if user_in.emergency_contacts:
        for contact_data in user_in.emergency_contacts:
            emergency_contact = EmergencyContacts(
                user_id=user.user_id,
                contact_phone=contact_data.contact_phone,
                kin=contact_data.kin,
                contact_name=contact_data.contact_name,
            )
            db.add(emergency_contact)
    
    # Asociar condiciones médicas si fueron proporcionadas
    if user_in.medical_condition_ids:
        for condition_id in user_in.medical_condition_ids:
            user_condition = UserConditions(
                user_id=user.user_id,
                medical_condition_id=condition_id,
            )
            db.add(user_condition)
    
    db.commit()
    return user


def get_user(db: Session, user_id: int) -> Optional[Users]:
    stmt = select(Users).where(Users.user_id == user_id).options(
        selectinload(Users.emergency_contacts),
        selectinload(Users.conditions)
    )
    return db.execute(stmt).scalar_one_or_none()

def get_user_by_phone(db: Session, phone: str) -> Optional[Users]:
    stmt = select(Users).where(Users.phone == phone)
    return db.execute(stmt).scalar_one_or_none()


def authenticate_user(db: Session, phone: str, password: str) -> Optional[Users]:
    user = get_user_by_phone(db, phone)
    if not user:
        return None
    if user.password != _hash_password(password):
        return None
    return user



def list_users(db: Session, skip: int = 0, limit: int = 100) -> List[Users]:
    stmt = select(Users).options(
        selectinload(Users.emergency_contacts),
        selectinload(Users.conditions)
    ).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def update_user(db: Session, user_id: int, user_in: UserUpdate) -> Optional[Users]:
    user = db.get(Users, user_id)
    if not user:
        return None

    if user_in.name is not None:
        user.name = user_in.name
    if user_in.phone is not None:
        user.phone = user_in.phone
    if user_in.birthday is not None:
        user.birthday = user_in.birthday
    if user_in.password is not None:
        user.password = _hash_password(user_in.password)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:
    user = db.get(Users, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True