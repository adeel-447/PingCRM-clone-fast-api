from pydantic import BaseModel, EmailStr
from typing import Optional

# Shared Base Schemas
class OrganizationBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    province_state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    province_state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    organization_id: Optional[int] = None
    organization_name: Optional[str] = None

# CREATE Schemas
class OrganizationCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    province_state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None

class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    province_state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    organization_id: Optional[int] = None

# UPDATE Schemas

class OrganizationUpdate(OrganizationBase):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    province_state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    is_deleted: Optional[bool] = None

class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    province_state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    organization_id: Optional[int] = None
    is_deleted: Optional[bool] = None

# READ Schemas
class Organization(OrganizationBase):
    id: int
    is_deleted: bool

    class Config:
        orm_mode = True
        from_attributes = True

class Contact(ContactBase):
    id: int
    is_deleted: bool

    class Config:
        orm_mode = True
        from_attributes = True

class OrganizationName(BaseModel):
    id: int
    name: str
