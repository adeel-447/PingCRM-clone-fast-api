import random
from sqlalchemy.orm import Session # type: ignore
from app.models import Organization, Contact

ORG_NAMES = ["TechNova", "GreenEdge", "BlueSky Inc", "DataWorld", "FutureSoft"]
CITIES = ["Toronto", "Vancouver", "New York", "San Francisco", "Chicago"]
PROVINCES = ["ON", "BC", "NY", "CA", "IL"]
COUNTRIES = ["Canada", "USA"]

def seed_data(db: Session):
    if db.query(Organization).first():
        print("Data already seeded.")
        return

    for i, org_name in enumerate(ORG_NAMES):
        org = Organization(
            name=org_name,
            email=f"contact@{org_name.lower().replace(' ', '')}.com",
            phone=f"555-100{i}",
            address=f"{i+1} Main Street",
            city=random.choice(CITIES),
            province_state=random.choice(PROVINCES),
            country=random.choice(COUNTRIES),
            postal_code=f"A1B{i}C{i}",
        )

        db.add(org)

        num_contacts = random.randint(4, 5)
        for j in range(num_contacts):
            contact = Contact(
                first_name=f"User{j+1}",
                last_name=f"Org{i+1}",
                email=f"user{j+1}@{org.name.lower().replace(' ', '')}.com",
                phone=f"555-200{i}{j}",
                address=f"{j+10} Contact St",
                city=random.choice(CITIES),
                province_state=random.choice(PROVINCES),
                country=random.choice(COUNTRIES),
                postal_code=f"Z{i}{j}Y{j}",
                organization=org,
            )
            db.add(contact)

    db.commit()
    print("Data successfully seeded.")
