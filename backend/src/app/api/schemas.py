import uuid
from typing import List, AnyStr, Optional, Dict

from fastapi_users import schemas
from pydantic import BaseModel


class CorrelAidUser(BaseModel):
    """
    Base class extension for the user model with additional fields.
    """
    roles: List[str]
    local_chapter: str
    first_name: str
    surname: str
    gender: Optional[str]

class UserRead(schemas.BaseUser[uuid.UUID], CorrelAidUser):
    pass

class UserCreate(schemas.BaseUserCreate, CorrelAidUser):
    pass

class UserUpdate(schemas.BaseUserUpdate, CorrelAidUser):
    pass


class Contact(BaseModel):
    """
    Base class for specifying organizational contacts.
    """
    first_name: str
    surname: str
    email: str
    phone: Optional[str]

    class Config:
        orm_mode = True

class PartnerOrganization(BaseModel):
    """
    Class for the partner organizations collaborating with CorrelAid.
    """
    id: uuid.UUID
    name: str
    general_contact: Contact
    project_contacts: Optional[List[Dict[str, Contact]]]
    legal_form: str
    sector: str
    local_chapter: Optional[str]
    digital_maturity: Optional[str]
    data_culture: Optional[str]

    class Config:
        orm_mode = True