import json
import hashlib
import uuid
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User, Booking
from backend.schemas import (
    SessionRegisterRequest, SessionRegisterResponse,
    UserRegisterRequest, UserLoginRequest, UserProfileResponse, UserProfileUpdate
)

router = APIRouter(prefix="/auth", tags=["Authentication & Profiles"])

def hash_password(password: str) -> str:
    salt = "ctwm_salt_2026"
    return hashlib.sha256(f"{salt}{password}".encode("utf-8")).hexdigest()

def verify_password(plain_password: str, hashed: Optional[str]) -> bool:
    if not hashed:
        return True # Support for beta users without password
    return hash_password(plain_password) == hashed

@router.post("/register", response_model=UserProfileResponse)
def register_user(req: UserRegisterRequest, db: Session = Depends(get_db)):
    """
    Registers a new traveler account with profile details and password.
    """
    if not req.email and not req.phone:
        raise HTTPException(status_code=400, detail="Either email or phone number is required to register.")

    # Check for existing user
    if req.email:
        existing = db.query(User).filter(User.email == req.email.strip().lower()).first()
        if existing:
            raise HTTPException(status_code=400, detail="An account with this email already exists. Please log in.")
    if req.phone:
        existing = db.query(User).filter(User.phone == req.phone.strip()).first()
        if existing:
            raise HTTPException(status_code=400, detail="An account with this phone number already exists. Please log in.")

    user = User(
        email=req.email.strip().lower() if req.email else None,
        phone=req.phone.strip() if req.phone else None,
        display_name=req.display_name.strip() or "Traveler",
        password_hash=hash_password(req.password),
        city=req.city or "Bengaluru",
        is_beta_tester=True,
        tester_group="verified_member"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = f"ctwm_token_{user.id}_{uuid.uuid4().hex[:12]}"
    return UserProfileResponse(
        id=user.id,
        email=user.email,
        phone=user.phone,
        display_name=user.display_name,
        city=user.city or "Bengaluru",
        avatar_url=user.avatar_url,
        is_beta_tester=user.is_beta_tester,
        token=token,
        bookings_count=0,
        message="Account created successfully! Welcome to ComeTripWithMe."
    )

@router.post("/login", response_model=UserProfileResponse)
def login_user(req: UserLoginRequest, db: Session = Depends(get_db)):
    """
    Authenticates a user via email or phone and password.
    """
    login_id = req.login_id.strip()
    user = None
    if "@" in login_id:
        user = db.query(User).filter(User.email == login_id.lower()).first()
    else:
        user = db.query(User).filter(User.phone == login_id).first()

    # If user doesn't exist, create on the fly if demo/beta testing credentials or return 401
    if not user:
        # Check if login_id matches by phone or email regardless
        user = db.query(User).filter((User.email == login_id.lower()) | (User.phone == login_id)).first()

    if not user:
        # If user doesn't exist and password provided, automatically register for seamless demo/testing
        user = User(
            email=login_id.lower() if "@" in login_id else None,
            phone=login_id if "@" not in login_id else None,
            display_name=login_id.split("@")[0].capitalize() if "@" in login_id else f"Traveler_{login_id[-4:]}",
            password_hash=hash_password(req.password),
            city="Bengaluru",
            is_beta_tester=True,
            tester_group="verified_member"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # Check password if set
        if user.password_hash and not verify_password(req.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid password. Please check your credentials.")

    bookings_count = db.query(Booking).filter(Booking.user_id == user.id).count()
    token = f"ctwm_token_{user.id}_{uuid.uuid4().hex[:12]}"

    return UserProfileResponse(
        id=user.id,
        email=user.email,
        phone=user.phone,
        display_name=user.display_name or "Traveler",
        city=user.city or "Bengaluru",
        avatar_url=user.avatar_url,
        is_beta_tester=user.is_beta_tester,
        token=token,
        bookings_count=bookings_count,
        message="Login successful! Ready to explore and book trips."
    )

@router.get("/me")
def get_current_user_profile(
    user_id: Optional[str] = Query(None),
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Returns authenticated user profile along with all booked trips and digital passes.
    """
    uid = user_id
    if not uid and authorization and authorization.startswith("Bearer ctwm_token_"):
        parts = authorization.replace("Bearer ctwm_token_", "").split("_")
        if parts:
            uid = parts[0]

    if not uid:
        # Return fallback demo user if no user_id passed
        user = db.query(User).first()
        if not user:
            raise HTTPException(status_code=404, detail="No authenticated user found")
    else:
        user = db.query(User).filter(User.id == uid).first()
        if not user:
            raise HTTPException(status_code=404, detail="User account not found")

    bookings = db.query(Booking).filter(Booking.user_id == user.id).order_by(Booking.created_at.desc()).all()
    bookings_data = []
    for b in bookings:
        travelers = []
        try:
            travelers = json.loads(b.traveler_details_json) if b.traveler_details_json else []
        except:
            pass
        bookings_data.append({
            "booking_id": b.id,
            "booking_reference": b.booking_reference,
            "trip_id": b.trip_id,
            "trip_title": b.trip_title,
            "tier": b.tier,
            "departure_city": b.departure_city,
            "travel_date": b.travel_date,
            "travelers_count": b.travelers_count,
            "travelers": travelers,
            "total_amount": b.total_amount,
            "status": b.status,
            "created_at": b.created_at.isoformat()
        })

    return {
        "id": user.id,
        "email": user.email,
        "phone": user.phone,
        "display_name": user.display_name,
        "city": user.city or "Bengaluru",
        "avatar_url": user.avatar_url,
        "is_beta_tester": user.is_beta_tester,
        "tester_group": user.tester_group,
        "bookings_count": len(bookings_data),
        "bookings": bookings_data
    }

@router.put("/profile")
def update_profile(
    req: UserProfileUpdate,
    user_id: str = Query(...),
    db: Session = Depends(get_db)
):
    """
    Updates user display name, phone, city, or avatar URL.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if req.display_name:
        user.display_name = req.display_name.strip()
    if req.phone:
        user.phone = req.phone.strip()
    if req.city:
        user.city = req.city.strip()
    if req.avatar_url:
        user.avatar_url = req.avatar_url.strip()

    db.commit()
    db.refresh(user)
    return {
        "success": True,
        "message": "Profile updated successfully!",
        "user": {
            "id": user.id,
            "display_name": user.display_name,
            "email": user.email,
            "phone": user.phone,
            "city": user.city,
            "avatar_url": user.avatar_url
        }
    }

@router.post("/session", response_model=SessionRegisterResponse)
def register_session(req: SessionRegisterRequest, db: Session = Depends(get_db)):
    """
    Registers or restores an anonymous or named beta tester session.
    """
    user = None
    if req.email:
        user = db.query(User).filter(User.email == req.email).first()
    elif req.phone:
        user = db.query(User).filter(User.phone == req.phone).first()

    if not user:
        user = User(
            phone=req.phone,
            email=req.email,
            display_name=req.display_name or f"Tester_{req.session_id[:6]}",
            is_beta_tester=True,
            tester_group="public_beta",
            device_info=json.dumps(req.device_info or {})
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return SessionRegisterResponse(
        user_id=user.id,
        session_id=req.session_id,
        is_beta_tester=user.is_beta_tester,
        message="Session active and ready for testing."
    )
