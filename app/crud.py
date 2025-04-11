from sqlalchemy.orm import Session
from app import schemas
from app.models import Organization, Contact
from sqlalchemy import func

# ----------------------
# Organizations
# ----------------------

def get_organizations(db: Session, page: int = 1, search: str = "", per_page: int = 10, deleted: str = "false"):
    query = db.query(Organization)

    if deleted == "false":
        query = query.filter(Organization.is_deleted == False)
    elif deleted == "true":
        query = query.filter(Organization.is_deleted == True)

    if search:
        query = query.filter(Organization.name.ilike(f"%{search}%"))
        organizations = query.all()
        return [schemas.Organization.model_validate(org) for org in organizations], 1

    total_items = query.count()
    total_pages = (total_items + per_page - 1) // per_page
    organizations = query.offset((page - 1) * per_page).limit(per_page).all()
    return [schemas.Organization.model_validate(org) for org in organizations], total_pages

def get_organization(db: Session, organization_id: int):
    return db.query(Organization).filter(Organization.id == organization_id).first()

def create_organization(db: Session, organization: schemas.OrganizationCreate):
    db_organization = Organization(
        name=organization.name,
        email=organization.email,
        phone=organization.phone,
        address=organization.address,
        city=organization.city,
        province_state=organization.province_state,
        country=organization.country,
        postal_code=organization.postal_code,
        is_deleted=False
    )
    db.add(db_organization)
    db.commit()
    db.refresh(db_organization)
    return db_organization


def update_organization(db: Session, organization_id: int, updates: schemas.OrganizationUpdate):
    db_organization = get_organization(db, organization_id)
    if db_organization:
        for key, value in updates.dict(exclude_unset=True).items():
            setattr(db_organization, key, value)
        db.commit()
        db.refresh(db_organization)
    return db_organization

def get_all_organization_names(db: Session):
    return db.query(Organization.id, Organization.name).all()

def delete_organization(db: Session, organization_id: int):
    organization = get_organization(db, organization_id)
    if organization:
        organization.is_deleted = True
        for contact in organization.contacts:
            contact.is_deleted = True
        db.commit()
        db.refresh(organization)
    return organization

def get_contacts_by_organization(db: Session, organization_id: int):
    contacts = db.query(Contact).filter(
        Contact.organization_id == organization_id
    ).all()

    for contact in contacts:
        contact.organization_name = contact.organization.name if contact.organization else None

    return [schemas.Contact.model_validate(contact) for contact in contacts]


# ----------------------
# Contacts
# ----------------------

def get_contacts(db: Session, page: int = 1, search: str = "", per_page: int = 10, deleted: str = "false"):
    query = db.query(Contact)

    if deleted == "false":
        query = query.filter(Contact.is_deleted == False)
    elif deleted == "true":
        query = query.filter(Contact.is_deleted == True)

    if search:
        query = query.filter((Contact.first_name + ' ' + Contact.last_name).ilike(f"%{search}%"))

    total_items = query.count()
    total_pages = (total_items + per_page - 1) // per_page
    contacts = query.offset((page - 1) * per_page).limit(per_page).all()

    # Check for None values and replace them with empty strings if necessary
    for contact in contacts:
        if contact.first_name is None:
            contact.first_name = ""
        if contact.last_name is None:
            contact.last_name = ""

        contact.organization_name = contact.organization.name if contact.organization else None

    return [schemas.Contact.model_validate(contact) for contact in contacts], total_pages

def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = Contact(
        first_name=contact.first_name,
        last_name=contact.last_name,
        email=contact.email,
        phone=contact.phone,
        address=contact.address,
        city=contact.city,
        province_state=contact.province_state,
        country=contact.country,
        postal_code=contact.postal_code,
        organization_id=contact.organization_id,
        is_deleted=False
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, updates: schemas.ContactUpdate):
    db_contact = get_contact(db, contact_id)
    if db_contact:
        for key, value in updates.dict(exclude_unset=True).items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    contact = get_contact(db, contact_id)
    if contact:
        contact.is_deleted = True
        db.commit()
        db.refresh(contact)
    return contact
