import json
import random
import string
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Booking, BookingStatus, User
from backend.schemas import BookingInitiateRequest, BookingResponse

router = APIRouter(prefix="/bookings", tags=["Bookings & Passes"])

def generate_booking_ref() -> str:
    chars = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"CTWM-2026-{chars}"

@router.post("/initiate", response_model=BookingResponse)
def initiate_booking(req: BookingInitiateRequest, db: Session = Depends(get_db)):
    """
    Initiates a new booking in pending state prior to payment.
    """
    ref = generate_booking_ref()
    
    # Check if user exists for session
    user = db.query(User).filter(User.phone == req.traveler_details[0].phone).first() if req.traveler_details else None

    booking = Booking(
        booking_reference=ref,
        user_id=user.id if user else None,
        session_id=req.session_id,
        trip_id=req.trip_id,
        trip_title=req.trip_title,
        tier=req.tier.upper(),
        departure_city=req.departure_city,
        travel_date=req.travel_date,
        travelers_count=req.travelers_count,
        traveler_details_json=json.dumps([t.dict() for t in req.traveler_details]),
        base_price=req.base_price,
        discount_amount=req.discount_amount,
        voucher_code=req.voucher_code,
        gst_tax=req.gst_tax,
        total_amount=req.total_amount,
        status=BookingStatus.INITIATED.value
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    return BookingResponse(
        booking_id=booking.id,
        booking_reference=booking.booking_reference,
        trip_title=booking.trip_title,
        tier=booking.tier,
        total_amount=booking.total_amount,
        status=booking.status,
        travel_date=booking.travel_date,
        departure_city=booking.departure_city,
        travelers_count=booking.travelers_count,
        created_at=booking.created_at
    )

@router.get("/{booking_ref}")
def get_booking_pass(booking_ref: str, db: Session = Depends(get_db)):
    """
    Retrieves full booking pass, travelers, inclusions, and digital voucher.
    """
    booking = db.query(Booking).filter(Booking.booking_reference == booking_ref).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking reference not found")

    travelers = json.loads(booking.traveler_details_json)
    
    return {
        "booking_id": booking.id,
        "booking_reference": booking.booking_reference,
        "trip_id": booking.trip_id,
        "trip_title": booking.trip_title,
        "tier": booking.tier,
        "departure_city": booking.departure_city,
        "travel_date": booking.travel_date,
        "travelers_count": booking.travelers_count,
        "travelers": travelers,
        "base_price": booking.base_price,
        "discount_amount": booking.discount_amount,
        "gst_tax": booking.gst_tax,
        "total_amount": booking.total_amount,
        "status": booking.status,
        "is_confirmed": booking.status == BookingStatus.CONFIRMED.value,
        "digital_pass_qr": f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={booking.booking_reference}",
        "created_at": booking.created_at.isoformat()
    }
