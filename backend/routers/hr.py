"""
ComeTripWithMe · HR & Stakeholders Directory Router
Manages all stakeholder records: Core Team, Creators, Chauffeurs, Hotel Partners, and Activity Vendors.
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.database import get_db
from backend.models import Stakeholder
from backend.schemas import (
    StakeholderCreate, StakeholderUpdate, StakeholderResponse, HRMetricsResponse
)

router = APIRouter(prefix="/hr", tags=["HR & Stakeholders Directory"])

DEFAULT_STAKEHOLDERS_SEED = [
    {
        "full_name": "Karthik Dalabanjan",
        "email": "karthik@cometripwithme.com",
        "phone": "+91 97423 11023",
        "role_category": "CORE_TEAM",
        "designation": "Founder & Managing Director",
        "department_or_destination": "Executive Management",
        "status": "ACTIVE",
        "employment_type": "FULL_TIME",
        "emergency_contact_name": "Family Emergency",
        "emergency_contact_phone": "+91 97423 11000",
        "payout_details": "karthik@okhdfcbank",
        "compensation_model": "Executive Equity & Director Remuneration",
        "joined_date": "2024-01-01",
        "documents_verified": True,
        "social_handle": "@cometriipwme",
        "notes": "Oversees corporate strategy, trip scouting, and platform expansion."
    },
]

def seed_stakeholders_if_empty(db: Session):
    count = db.query(Stakeholder).count()
    if count == 0:
        for s in DEFAULT_STAKEHOLDERS_SEED:
            stakeholder = Stakeholder(**s)
            db.add(stakeholder)
        db.commit()

@router.get("/stakeholders", response_model=List[StakeholderResponse])
def get_all_stakeholders(
    category: Optional[str] = Query(None, description="Filter by CORE_TEAM, CREATOR, CHAUFFEUR, HOTEL_PARTNER, ACTIVITY_VENDOR, INVESTOR_ADVISOR"),
    department: Optional[str] = Query(None, description="Filter by department or destination"),
    status: Optional[str] = Query(None, description="Filter by ACTIVE, ONBOARDING, ON_LEAVE, INACTIVE"),
    search: Optional[str] = Query(None, description="Search by name, email, phone, or designation"),
    db: Session = Depends(get_db)
):
    """
    Retrieves all stakeholders with optional filtering and search capabilities.
    """
    seed_stakeholders_if_empty(db)
    query = db.query(Stakeholder)

    if category and category.upper() != "ALL":
        query = query.filter(Stakeholder.role_category == category.upper())
    if department and department.upper() != "ALL":
        query = query.filter(Stakeholder.department_or_destination.ilike(f"%{department}%"))
    if status and status.upper() != "ALL":
        query = query.filter(Stakeholder.status == status.upper())
    if search:
        s = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Stakeholder.full_name.ilike(s),
                Stakeholder.email.ilike(s),
                Stakeholder.phone.ilike(s),
                Stakeholder.designation.ilike(s),
                Stakeholder.department_or_destination.ilike(s)
            )
        )

    return query.order_by(Stakeholder.role_category, Stakeholder.full_name).all()

@router.get("/stakeholders/{stakeholder_id}", response_model=StakeholderResponse)
def get_stakeholder(stakeholder_id: str, db: Session = Depends(get_db)):
    """
    Retrieves full profile details for a specific stakeholder.
    """
    stakeholder = db.query(Stakeholder).filter(Stakeholder.id == stakeholder_id).first()
    if not stakeholder:
        raise HTTPException(status_code=404, detail="Stakeholder record not found")
    return stakeholder

@router.post("/stakeholders", response_model=StakeholderResponse)
def create_stakeholder(req: StakeholderCreate, db: Session = Depends(get_db)):
    """
    Onboards and registers a new stakeholder into the HR directory.
    """
    if req.email:
        existing = db.query(Stakeholder).filter(Stakeholder.email == req.email.strip().lower()).first()
        if existing:
            raise HTTPException(status_code=400, detail="A stakeholder with this email address already exists.")

    stakeholder = Stakeholder(
        full_name=req.full_name.strip(),
        email=req.email.strip().lower() if req.email else None,
        phone=req.phone.strip(),
        role_category=req.role_category.upper(),
        designation=req.designation.strip(),
        department_or_destination=req.department_or_destination.strip(),
        status=req.status.upper(),
        employment_type=req.employment_type.upper(),
        emergency_contact_name=req.emergency_contact_name.strip() if req.emergency_contact_name else None,
        emergency_contact_phone=req.emergency_contact_phone.strip() if req.emergency_contact_phone else None,
        payout_details=req.payout_details.strip() if req.payout_details else None,
        compensation_model=req.compensation_model.strip() if req.compensation_model else None,
        joined_date=req.joined_date or datetime.utcnow().strftime("%Y-%m-%d"),
        documents_verified=req.documents_verified,
        social_handle=req.social_handle.strip() if req.social_handle else None,
        notes=req.notes.strip() if req.notes else None
    )
    db.add(stakeholder)
    db.commit()
    db.refresh(stakeholder)
    return stakeholder

@router.put("/stakeholders/{stakeholder_id}", response_model=StakeholderResponse)
def update_stakeholder(stakeholder_id: str, req: StakeholderUpdate, db: Session = Depends(get_db)):
    """
    Updates stakeholder details, contact, designation, payout, or status.
    """
    stakeholder = db.query(Stakeholder).filter(Stakeholder.id == stakeholder_id).first()
    if not stakeholder:
        raise HTTPException(status_code=404, detail="Stakeholder record not found")

    if req.full_name is not None:
        stakeholder.full_name = req.full_name.strip()
    if req.email is not None:
        stakeholder.email = req.email.strip().lower() if req.email else None
    if req.phone is not None:
        stakeholder.phone = req.phone.strip()
    if req.role_category is not None:
        stakeholder.role_category = req.role_category.upper()
    if req.designation is not None:
        stakeholder.designation = req.designation.strip()
    if req.department_or_destination is not None:
        stakeholder.department_or_destination = req.department_or_destination.strip()
    if req.status is not None:
        stakeholder.status = req.status.upper()
    if req.employment_type is not None:
        stakeholder.employment_type = req.employment_type.upper()
    if req.emergency_contact_name is not None:
        stakeholder.emergency_contact_name = req.emergency_contact_name.strip()
    if req.emergency_contact_phone is not None:
        stakeholder.emergency_contact_phone = req.emergency_contact_phone.strip()
    if req.payout_details is not None:
        stakeholder.payout_details = req.payout_details.strip()
    if req.compensation_model is not None:
        stakeholder.compensation_model = req.compensation_model.strip()
    if req.joined_date is not None:
        stakeholder.joined_date = req.joined_date.strip()
    if req.documents_verified is not None:
        stakeholder.documents_verified = req.documents_verified
    if req.social_handle is not None:
        stakeholder.social_handle = req.social_handle.strip()
    if req.notes is not None:
        stakeholder.notes = req.notes.strip()

    stakeholder.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(stakeholder)
    return stakeholder

@router.delete("/stakeholders/{stakeholder_id}")
def delete_stakeholder(stakeholder_id: str, db: Session = Depends(get_db)):
    """
    Removes a stakeholder record from the directory.
    """
    stakeholder = db.query(Stakeholder).filter(Stakeholder.id == stakeholder_id).first()
    if not stakeholder:
        raise HTTPException(status_code=404, detail="Stakeholder record not found")

    db.delete(stakeholder)
    db.commit()
    return {"success": True, "message": f"Stakeholder '{stakeholder.full_name}' deleted successfully."}

@router.get("/metrics", response_model=HRMetricsResponse)
def get_hr_metrics(db: Session = Depends(get_db)):
    """
    Returns real-time HR directory analytics, headcount by category, and active counts.
    """
    seed_stakeholders_if_empty(db)
    all_s = db.query(Stakeholder).all()

    cat_map = {}
    stat_map = {}
    active_drivers = 0
    verified_creators = 0
    core_team = 0

    for s in all_s:
        cat = s.role_category or "OTHER"
        cat_map[cat] = cat_map.get(cat, 0) + 1

        stat = s.status or "ACTIVE"
        stat_map[stat] = stat_map.get(stat, 0) + 1

        if cat == "CHAUFFEUR" and stat == "ACTIVE":
            active_drivers += 1
        if cat == "CREATOR" and s.documents_verified:
            verified_creators += 1
        if cat == "CORE_TEAM":
            core_team += 1

    return HRMetricsResponse(
        total_stakeholders=len(all_s),
        categories_breakdown=cat_map,
        status_breakdown=stat_map,
        active_drivers_count=active_drivers,
        verified_creators_count=verified_creators,
        core_team_count=core_team
    )

@router.post("/seed")
def seed_hr_directory(force: bool = False, db: Session = Depends(get_db)):
    """
    Manually triggers seeding of default stakeholders.
    """
    if force:
        db.query(Stakeholder).delete()
        db.commit()

    seed_stakeholders_if_empty(db)
    count = db.query(Stakeholder).count()
    return {"success": True, "total_stakeholders": count, "message": "HR Stakeholder directory seeded successfully."}

