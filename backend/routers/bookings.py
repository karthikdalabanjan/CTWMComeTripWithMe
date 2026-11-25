import json
import random
import string
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Booking, BookingStatus, User, TripLeg, DriverMessage
from backend.schemas import (
    BookingInitiateRequest, BookingResponse,
    TripLegResponse, TripLegUpdate,
    DriverMessageCreate, DriverMessageResponse
)

router = APIRouter(prefix="/bookings", tags=["Bookings, Legs & Driver Dispatch"])

def generate_booking_ref() -> str:
    chars = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"CTWM-2026-{chars}"

def seed_default_trip_legs(booking: Booking, db: Session) -> List[TripLeg]:
    """
    Creates comprehensive sequential legs (instances of the trip) with assigned drivers,
    destinations, vehicle info, and phone numbers that can be updated according to destination.
    """
    dest = booking.trip_title.split()[0]
    org = booking.departure_city.split()[0]
    is_luxury = "LUX" in booking.tier.upper()

    # Destination-specific contact data
    dest_phone = "+91 97645 10928"
    dest_driver = "Sandeep Naik"
    dest_vehicle = "Toyota Innova Crysta (Pearl White)" if is_luxury else "Maruti Suzuki Ertiga AC"
    dest_plate = "GA-03-AA-4491"

    if "thailand" in booking.trip_id.lower() or "krabi" in booking.trip_id.lower():
        dest_phone = "+66 81 234 5678"
        dest_driver = "Somchai Prasert (Bangkok & Krabi Transport)"
        dest_vehicle = "VIP Commuter Luxury Van" if is_luxury else "Air-Conditioned Sedan"
        dest_plate = "BKK-8821"
    elif "himachal" in booking.trip_id.lower():
        dest_phone = "+91 98160 55432"
        dest_driver = "Prem Thakur (Mountain Chauffeur)"
        dest_vehicle = "Mahindra Scorpio 4x4" if is_luxury else "Swift Dzire Mountain AC"
        dest_plate = "HP-01-T-8877"
    elif "gokarna" in booking.trip_id.lower():
        dest_phone = "+91 94801 22334"
        dest_driver = "Manjunath Hegde (Coastline Transfers)"
        dest_vehicle = "Toyota Innova AC" if is_luxury else "Dzire AC"
        dest_plate = "KA-30-M-4921"
    elif "pon" in booking.trip_id.lower() or "puducherry" in booking.trip_id.lower():
        dest_phone = "+91 98401 55667"
        dest_driver = "Murugan Selvam (ECR Coastal Driver)"
        dest_vehicle = "Innova Crysta" if is_luxury else "Etios AC"
        dest_plate = "TN-07-BZ-9021"

    legs_specs = [
        {
            "leg_index": 1,
            "title": f"Leg 1: Pickup Cab from Home/Hub ({org})",
            "leg_type": "CAB_PICKUP",
            "status": "ASSIGNED",
            "scheduled_time": f"{booking.travel_date} · 05:45 AM",
            "pickup_location": f"Traveler Home / Koramangala Hub, {org}",
            "dropoff_location": f"{booking.departure_city} - Departure Gate 2",
            "driver_name": "Ramesh Gowda" if "BLR" in org else ("Virender Sharma" if "DEL" in org else "Sachin Kadam"),
            "driver_phone": "+91 98451 22910" if "BLR" in org else ("+91 98112 34567" if "DEL" in org else "+91 98201 98765"),
            "vehicle_model": "Innova Crysta AC (White)" if is_luxury else "Maruti Dzire AC (Silver)",
            "vehicle_number": "KA-01-MJ-8821" if "BLR" in org else ("DL-01-CA-4491" if "DEL" in org else "MH-02-BT-3329"),
            "otp_code": "4821",
            "notes": "Chauffeur assigned. Waiting with name placard. Direct text and call available."
        },
        {
            "leg_index": 2,
            "title": f"Leg 2: Primary Transit ({org} ➔ {dest})",
            "leg_type": "FLIGHT" if "LUX" in booking.tier.upper() or "MID" in booking.tier.upper() else "BUS",
            "status": "SCHEDULED",
            "scheduled_time": f"{booking.travel_date} · 08:30 AM",
            "pickup_location": f"{booking.departure_city} - Gate 4",
            "dropoff_location": f"{dest} Terminal 1 Arrivals",
            "driver_name": "IndiGo 6E-241" if not is_luxury else "Air India AI-512 VIP",
            "driver_phone": "1800 180 1407",
            "vehicle_model": "Airbus A321neo" if not is_luxury else "Boeing 787 Dreamliner",
            "vehicle_number": f"PNR: {booking.booking_reference[-6:]}",
            "otp_code": "BOARDING",
            "notes": "Web check-in completed. Priority boarding pass unlocked."
        },
        {
            "leg_index": 3,
            "title": f"Leg 3: Destination Arrival Pickup Cab ({dest})",
            "leg_type": "CAB_TRANSFER",
            "status": "ASSIGNED",
            "scheduled_time": f"{booking.travel_date} · 11:15 AM",
            "pickup_location": f"{dest} Airport Arrival Exit (Pillar 6)",
            "dropoff_location": f"Boutique Resort / Villa ({dest})",
            "driver_name": dest_driver,
            "driver_phone": dest_phone,
            "vehicle_model": dest_vehicle,
            "vehicle_number": dest_plate,
            "otp_code": "7719",
            "notes": "Dedicated arrival chauffeur assigned according to destination. Number updated by operator."
        },
        {
            "leg_index": 4,
            "title": f"Leg 4: Resort Check-In & Room Allocation ({dest})",
            "leg_type": "HOTEL_CHECKIN",
            "status": "SCHEDULED",
            "scheduled_time": f"{booking.travel_date} · 12:30 PM",
            "pickup_location": "Resort Front Desk & Concierge",
            "dropoff_location": "Deluxe Balcony Suite / Ocean Villa",
            "driver_name": "Resort Concierge Team",
            "driver_phone": "+91 98450 88200",
            "vehicle_model": "Room Key Card & Welcome Drink Pass",
            "vehicle_number": f"Voucher: {booking.booking_reference}",
            "otp_code": "PASS-2026",
            "notes": "Early check-in prioritized. Welcome drinks and resort audio guide unlocked."
        },
        {
            "leg_index": 5,
            "title": f"Leg 5: Curated Sightseeing & Day Tour ({dest})",
            "leg_type": "ACTIVITY_TRANSFER",
            "status": "SCHEDULED",
            "scheduled_time": "Day 2 · 09:00 AM",
            "pickup_location": "Resort Courtyard Lobby",
            "dropoff_location": "Curated Secret Viewpoints & Cliff Trails",
            "driver_name": "Mahesh Patil (Tour Captain)",
            "driver_phone": "+91 94220 77312",
            "vehicle_model": "Dedicated AC Tour Cab / Scooty Handover",
            "vehicle_number": "GA-03-BB-1029",
            "otp_code": "3310",
            "notes": "Dedicated local captain for all curated stops, secret bakeries, and audio guide spots."
        },
        {
            "leg_index": 6,
            "title": f"Leg 6: Return Airport / Station Transfer Cab ({dest})",
            "leg_type": "RETURN_CAB",
            "status": "SCHEDULED",
            "scheduled_time": "Final Day · 04:00 PM",
            "pickup_location": "Resort Lobby",
            "dropoff_location": f"{dest} Airport Terminal Departure Gate",
            "driver_name": "Santosh Velingkar",
            "driver_phone": "+91 98221 44091",
            "vehicle_model": "Toyota Innova Crysta / Sedan",
            "vehicle_number": "GA-03-AC-7782",
            "otp_code": "9023",
            "notes": "Scheduled for on-time return flight departure."
        }
    ]

    created_legs = []
    for spec in legs_specs:
        leg = TripLeg(
            booking_id=booking.id,
            leg_index=spec["leg_index"],
            title=spec["title"],
            leg_type=spec["leg_type"],
            status=spec["status"],
            scheduled_time=spec["scheduled_time"],
            pickup_location=spec["pickup_location"],
            dropoff_location=spec["dropoff_location"],
            driver_name=spec["driver_name"],
            driver_phone=spec["driver_phone"],
            vehicle_model=spec["vehicle_model"],
            vehicle_number=spec["vehicle_number"],
            otp_code=spec["otp_code"],
            notes=spec["notes"]
        )
        db.add(leg)
        created_legs.append(leg)

    db.commit()
    return created_legs

@router.post("/initiate", response_model=BookingResponse)
def initiate_booking(req: BookingInitiateRequest, db: Session = Depends(get_db)):
    """
    Initiates a new booking. Requires user account or associates with authenticated profile.
    Saves snapshot of the complete itinerary and generates sequential trip legs with driver assignments.
    """
    ref = generate_booking_ref()

    # Find or link user
    user = None
    if req.user_id:
        user = db.query(User).filter(User.id == req.user_id).first()

    if not user and req.traveler_details:
        t0 = req.traveler_details[0]
        if t0.email:
            user = db.query(User).filter(User.email == t0.email).first()
        elif t0.phone:
            user = db.query(User).filter(User.phone == t0.phone).first()

    if not user:
        # Create an account automatically so user has a profile
        name = req.traveler_details[0].name if req.traveler_details else "Traveler"
        email = req.traveler_details[0].email if req.traveler_details else None
        phone = req.traveler_details[0].phone if req.traveler_details else None
        user = User(
            display_name=name,
            email=email,
            phone=phone,
            city=req.departure_city.split()[0] if req.departure_city else "Bengaluru",
            is_beta_tester=True,
            tester_group="verified_member"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    booking = Booking(
        booking_reference=ref,
        user_id=user.id,
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
        status=BookingStatus.INITIATED.value,
        itinerary_snapshot_json=json.dumps(req.itinerary_snapshot) if req.itinerary_snapshot else None
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    # Automatically seed the 6 trip legs with driver contact details
    seed_default_trip_legs(booking, db)

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
        user_id=booking.user_id,
        created_at=booking.created_at
    )

@router.get("/{booking_ref}")
def get_booking_pass(booking_ref: str, db: Session = Depends(get_db)):
    """
    Retrieves full booking pass, travelers, inclusions, complete itinerary snapshot, and digital voucher.
    """
    booking = db.query(Booking).filter(Booking.booking_reference == booking_ref).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking reference not found")

    travelers = []
    try:
        travelers = json.loads(booking.traveler_details_json) if booking.traveler_details_json else []
    except:
        pass

    itinerary_snapshot = None
    if booking.itinerary_snapshot_json:
        try:
            itinerary_snapshot = json.loads(booking.itinerary_snapshot_json)
        except:
            pass

    # Ensure legs exist
    legs = db.query(TripLeg).filter(TripLeg.booking_id == booking.id).order_by(TripLeg.leg_index).all()
    if not legs:
        legs = seed_default_trip_legs(booking, db)

    legs_data = []
    for l in legs:
        msg_count = db.query(DriverMessage).filter(DriverMessage.leg_id == l.id).count()
        legs_data.append({
            "id": l.id,
            "leg_index": l.leg_index,
            "title": l.title,
            "leg_type": l.leg_type,
            "status": l.status,
            "scheduled_time": l.scheduled_time,
            "pickup_location": l.pickup_location,
            "dropoff_location": l.dropoff_location,
            "driver_name": l.driver_name,
            "driver_phone": l.driver_phone,
            "vehicle_model": l.vehicle_model,
            "vehicle_number": l.vehicle_number,
            "otp_code": l.otp_code,
            "notes": l.notes,
            "messages_count": msg_count,
            "updated_at": l.updated_at.isoformat() if l.updated_at else None
        })

    return {
        "booking_id": booking.id,
        "booking_reference": booking.booking_reference,
        "user_id": booking.user_id,
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
        "itinerary_snapshot": itinerary_snapshot,
        "legs": legs_data,
        "digital_pass_qr": f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={booking.booking_reference}",
        "created_at": booking.created_at.isoformat()
    }

# ==================== Trip Legs & Live Driver Dispatch ====================

@router.get("/{booking_ref}/legs", response_model=List[TripLegResponse])
def get_booking_legs(booking_ref: str, db: Session = Depends(get_db)):
    """
    Returns all sequential legs/instances of the trip for real-time tracking,
    driver information, contact numbers, and messaging status.
    """
    booking = db.query(Booking).filter(Booking.booking_reference == booking_ref).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    legs = db.query(TripLeg).filter(TripLeg.booking_id == booking.id).order_by(TripLeg.leg_index).all()
    if not legs:
        legs = seed_default_trip_legs(booking, db)

    resp = []
    for l in legs:
        msg_count = db.query(DriverMessage).filter(DriverMessage.leg_id == l.id).count()
        resp.append(TripLegResponse(
            id=l.id,
            booking_id=l.booking_id,
            leg_index=l.leg_index,
            title=l.title,
            leg_type=l.leg_type,
            status=l.status,
            scheduled_time=l.scheduled_time,
            pickup_location=l.pickup_location,
            dropoff_location=l.dropoff_location,
            driver_name=l.driver_name,
            driver_phone=l.driver_phone,
            vehicle_model=l.vehicle_model,
            vehicle_number=l.vehicle_number,
            otp_code=l.otp_code,
            notes=l.notes,
            messages_count=msg_count,
            updated_at=l.updated_at
        ))
    return resp

@router.put("/legs/{leg_id}")
def update_trip_leg(leg_id: str, req: TripLegUpdate, db: Session = Depends(get_db)):
    """
    Updates driver information, driver phone number, vehicle details, or status for any instance of the trip.
    Enables operator/host to dynamically update the driver's phone number according to destination.
    """
    leg = db.query(TripLeg).filter(TripLeg.id == leg_id).first()
    if not leg:
        raise HTTPException(status_code=404, detail="Trip leg not found")

    if req.driver_name is not None:
        leg.driver_name = req.driver_name.strip()
    if req.driver_phone is not None:
        leg.driver_phone = req.driver_phone.strip()
    if req.vehicle_model is not None:
        leg.vehicle_model = req.vehicle_model.strip()
    if req.vehicle_number is not None:
        leg.vehicle_number = req.vehicle_number.strip()
    if req.status is not None:
        leg.status = req.status.strip().upper()
    if req.notes is not None:
        leg.notes = req.notes.strip()
    if req.scheduled_time is not None:
        leg.scheduled_time = req.scheduled_time.strip()
    if req.pickup_location is not None:
        leg.pickup_location = req.pickup_location.strip()
    if req.dropoff_location is not None:
        leg.dropoff_location = req.dropoff_location.strip()

    leg.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(leg)

    return {
        "success": True,
        "message": f"Trip leg '{leg.title}' driver & dispatch details updated successfully!",
        "leg": {
            "id": leg.id,
            "title": leg.title,
            "driver_name": leg.driver_name,
            "driver_phone": leg.driver_phone,
            "vehicle_model": leg.vehicle_model,
            "vehicle_number": leg.vehicle_number,
            "status": leg.status,
            "notes": leg.notes,
            "updated_at": leg.updated_at.isoformat()
        }
    }

# ==================== Traveler & Driver Text Messaging ====================

@router.get("/legs/{leg_id}/messages", response_model=List[DriverMessageResponse])
def get_leg_driver_messages(leg_id: str, db: Session = Depends(get_db)):
    """
    Retrieves full chat history between traveler and the driver for this trip leg.
    """
    leg = db.query(TripLeg).filter(TripLeg.id == leg_id).first()
    if not leg:
        raise HTTPException(status_code=404, detail="Trip leg not found")

    msgs = db.query(DriverMessage).filter(DriverMessage.leg_id == leg_id).order_by(DriverMessage.created_at).all()
    return [
        DriverMessageResponse(
            id=m.id,
            leg_id=m.leg_id,
            sender_type=m.sender_type,
            sender_name=m.sender_name,
            message_text=m.message_text,
            created_at=m.created_at
        )
        for m in msgs
    ]

@router.post("/legs/{leg_id}/messages", response_model=List[DriverMessageResponse])
def send_driver_message(leg_id: str, req: DriverMessageCreate, db: Session = Depends(get_db)):
    """
    Enables traveler to text the driver for this leg of the trip.
    Saves message and immediately returns driver's contextual reply so the user can communicate in real time!
    """
    leg = db.query(TripLeg).filter(TripLeg.id == leg_id).first()
    if not leg:
        raise HTTPException(status_code=404, detail="Trip leg not found")

    # 1. Save traveler message
    user_msg = DriverMessage(
        leg_id=leg.id,
        sender_type=req.sender_type.upper(),
        sender_name=req.sender_name or "Traveler",
        message_text=req.message_text
    )
    db.add(user_msg)
    db.commit()

    # 2. Generate simulated driver reply based on context and message
    driver_name = leg.driver_name or "Driver"
    text_lower = req.message_text.lower()

    if "where" in text_lower or "parked" in text_lower or "spot" in text_lower:
        reply = f"Hello! I am parked right near {leg.pickup_location.split('-')[0].strip()} with hazard lights on. Vehicle: {leg.vehicle_model} ({leg.vehicle_number})."
    elif "land" in text_lower or "arrived" in text_lower or "gate" in text_lower:
        reply = f"Welcome! I am waiting outside Pillar 4 with your name placard. Please take your time with luggage."
    elif "ac" in text_lower or "air" in text_lower or "temp" in text_lower:
        reply = f"Done! AC is already running and set to 22°C. Cold water bottles are kept in the rear seat."
    elif "late" in text_lower or "delay" in text_lower or "min" in text_lower:
        reply = f"No problem at all! Take your time, I am stationed right at the pickup zone waiting for you."
    elif "otp" in text_lower:
        reply = f"Got it, OTP will be verified upon boarding: {leg.otp_code}."
    else:
        reply = f"Received! I am {driver_name}, your assigned chauffeur for this leg ({leg.title}). Looking forward to hosting you!"

    driver_msg = DriverMessage(
        leg_id=leg.id,
        sender_type="DRIVER",
        sender_name=driver_name,
        message_text=reply
    )
    db.add(driver_msg)
    db.commit()

    # Return full message history
    all_msgs = db.query(DriverMessage).filter(DriverMessage.leg_id == leg.id).order_by(DriverMessage.created_at).all()
    return [
        DriverMessageResponse(
            id=m.id,
            leg_id=m.leg_id,
            sender_type=m.sender_type,
            sender_name=m.sender_name,
            message_text=m.message_text,
            created_at=m.created_at
        )
        for m in all_msgs
    ]
