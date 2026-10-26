import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User
from backend.schemas import SessionRegisterRequest, SessionRegisterResponse

router = APIRouter(prefix="/auth", tags=["Authentication & Testers"])

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
