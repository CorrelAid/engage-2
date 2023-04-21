from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship

from app.database.connection import Base

class PartnerOrganization(Base):
    __tablename__ = "organizations_partner"

    id = Column(UUID, primary_key=True)
    name = Column(String)
    general_contact_id = Column(UUID, ForeignKey("contacts.id"), unique=True)
    general_contact = relationship("contacts")
    project_contact_id = Column(UUID, ForeignKey("contacts.id"), nullable=True)
    project_contact = relationship("contacts", back_populates="organization")
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
    organization_ids = Column(UUID, ForeignKey("organizations_partner.id"), nullable=True)
    organization = relationship("organizations_partner")