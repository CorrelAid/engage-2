from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import DeclarativeBase, relationship
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTableUUID


class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTableUUID, Base):
    """
    Basic Userclass used for fast-api users extended with
    Correlaid attribute field to have all user data in one place.
    """
    roles = Column(ARRAY(String))
    local_chapter = Column(String, nullable=True)
    first_name = Column(String)
    surname = Column(String)
    gender = Column(String, nullable=True)


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    pass


class PartnerOrganization(Base):
    __tablename__ = "organizations_partner"

    id = Column(UUID, primary_key=True)
    name = Column(String)
    general_contact_id = Column(UUID, ForeignKey("contacts.id"), unique=True)
    general_contact = relationship("Contacts", back_populates="organization")
    #project_contact = relationship("Contacts")
    local_chapter = Column(String)
    digital_maturity = Column(String, nullable=True)
    data_culture = Column(String, nullable=True)


class Contacts(Base):
    __tablename__ = "contacts"

    id = Column(UUID, primary_key=True)
    first_name = Column(String)
    surname = Column(String)
    email = Column(String)
    phone = Column(String, nullable=True)
    organization = relationship("PartnerOrganization")
    #projects = relationship("")
