# Import side-effects to register all ORM mappings on app startup
from .BaseEntity import Base  # noqa: F401
from .UsersEntity import Users  # noqa: F401
from .MedicalConditionsEntity import MedicalConditions  # noqa: F401
from .UserConditionsEntity import UserConditions  # noqa: F401
from .KinCatalogModel import KinCatalog  # noqa: F401
from .EmergencyContactsEntity import EmergencyContacts  # noqa: F401
from .AccidentTypesEntity import AccidentTypes  # noqa: F401
from .EmergencyUnitEntity import EmergencyUnit  # noqa: F401
from .EmergenciesEntity import Emergencies  # noqa: F401

__all__ = [
    "Base",
    "Users",
    "MedicalConditions",
    "UserConditions",
    "KinCatalog",
    "EmergencyContacts",
    "AccidentTypes",
    "EmergencyUnit",
    "Emergencies",
]
# Import side-effects to register all ORM mappings on app startup
from .BaseEntity import Base  # noqa: F401
from .UsersEntity import Users  # noqa: F401
from .MedicalConditionsEntity import MedicalConditions  # noqa: F401
from .UserConditionsEntity import UserConditions  # noqa: F401
from .KinCatalogModel import KinCatalog  # noqa: F401
from .EmergencyContactsEntity import EmergencyContacts  # noqa: F401
from .AccidentTypesEntity import AccidentTypes  # noqa: F401
from .EmergencyUnitEntity import EmergencyUnit  # noqa: F401
from .EmergenciesEntity import Emergencies  # noqa: F401

__all__ = [
    "Base",
    "Users",
    "MedicalConditions",
    "UserConditions",
    "KinCatalog",
    "EmergencyContacts",
    "AccidentTypes",
    "EmergencyUnit",
    "Emergencies",
]