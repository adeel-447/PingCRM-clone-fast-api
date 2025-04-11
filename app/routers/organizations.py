from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/organizations", tags=["Organizations"])

@router.get("/", response_model=dict)
def list_organizations(
    page: int = 1,
    search: str = "",
    per_page: int = 10,
    deleted: str = "false",
    db: Session = Depends(get_db)
):
    organizations, total_pages = crud.get_organizations(db, page, search, per_page, deleted)
    return {"items": organizations, "totalPages": total_pages}

@router.post("/", response_model=schemas.Organization)
def create_organization(organization: schemas.OrganizationCreate, db: Session = Depends(get_db)):
    print('fbeahkfbejfq')
    return crud.create_organization(db, organization)

@router.get("/names", response_model=list[schemas.OrganizationName])
def get_organization_names(db: Session = Depends(get_db)):
    return crud.get_all_organization_names(db)

@router.patch("/{organization_id}", response_model=schemas.Organization)
def update_organization(organization_id: int, updates: schemas.OrganizationUpdate, db: Session = Depends(get_db)):
    return crud.update_organization(db, organization_id, updates)

@router.delete("/{organization_id}", response_model=schemas.Organization)
def delete_organization(organization_id: int, db: Session = Depends(get_db)):
    return crud.delete_organization(db, organization_id)

@router.get("/{organization_id}/contacts", response_model=list[schemas.Contact])
def get_contacts_for_organization(organization_id: int, db: Session = Depends(get_db)):
    return crud.get_contacts_by_organization(db, organization_id)

@router.patch("/{organization_id}/restore", response_model=schemas.Organization)
def restore_organization(organization_id: int, db: Session = Depends(get_db)):
    updates = schemas.OrganizationUpdate(is_deleted=False)
    return crud.update_organization(db, organization_id, updates)
