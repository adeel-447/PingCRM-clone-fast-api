"""Routers"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/contacts", tags=["Contacts"])

@router.get("/", response_model=dict)
def list_contacts(
    page: int = 1, 
    search: str = "",
    per_page: int = 10,
    deleted: str = "false",
    db: Session = Depends(get_db)
):
    contacts, total_pages = crud.get_contacts(db, page, search, per_page, deleted)
    return {"items": contacts, "totalPages": total_pages}

@router.post("/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db
    , contact)

@router.patch("/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, updates: schemas.ContactUpdate, db: Session = Depends(get_db)):
    return crud.update_contact(db, contact_id, updates)

@router.delete("/{contact_id}", response_model=schemas.Contact)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    return crud.delete_contact(db, contact_id)

@router.patch("/{contact_id}/restore", response_model=schemas.Contact)
def restore_contact(contact_id: int, db: Session = Depends(get_db)):
    updates = schemas.ContactUpdate(is_deleted=False)
    return crud.update_contact(db, contact_id, updates)
