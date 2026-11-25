import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, Text, DateTime, ForeignKey, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
import enum
from backend.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class BookingStatus(str, enum.Enum):
    INITIATED = "INITIATED"
    PENDING_PAYMENT = "PENDING_PAYMENT"
    CONFIRMED = "CONFIRMED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"

class PaymentStatus(str, enum.Enum):
    CREATED = "CREATED"
    AUTHORIZED = "AUTHORIZED"
    CAPTURED = "CAPTURED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"

class TierEnum(str, enum.Enum):
    LUXURY = "LUXURY"
    MID_TIER = "MID_TIER"
    BUDGET = "BUDGET"

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    phone = Column(String(20), unique=True, nullable=True, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    display_name = Column(String(100), nullable=True)
    password_hash = Column(String(255), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    city = Column(String(100), default="Bengaluru")
    is_beta_tester = Column(Boolean, default=True)
    tester_group = Column(String(50), default="public_beta")
    device_info = Column(Text, nullable=True) # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    bookings = relationship("Booking", back_populates="user")
    feedbacks = relationship("TestFeedback", back_populates="user")

class CustomItinerary(Base):
    __tablename__ = "custom_itineraries"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    session_id = Column(String(100), index=True, nullable=False)
    destination = Column(String(100), nullable=False)
    duration_days = Column(Integer, nullable=False)
    vibe = Column(String(50), nullable=False)
    budget_tier = Column(String(20), nullable=False)
    estimated_price = Column(Integer, nullable=False)
    day_plans_json = Column(Text, nullable=False) # JSON
    created_at = Column(DateTime, default=datetime.utcnow)

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    booking_reference = Column(String(30), unique=True, nullable=False, index=True) # e.g. CTWM-2026-X79K
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    session_id = Column(String(100), index=True, nullable=False)
    trip_id = Column(String(50), nullable=False)
    trip_title = Column(String(255), nullable=False)
    tier = Column(String(20), nullable=False) # LUXURY, MID_TIER, BUDGET
    departure_city = Column(String(100), default="Bengaluru (BLR)")
    travel_date = Column(String(50), nullable=False)
    travelers_count = Column(Integer, default=1)
    traveler_details_json = Column(Text, nullable=False) # JSON: [{name, phone, email}]
    base_price = Column(Float, nullable=False)
    discount_amount = Column(Float, default=0.0)
    voucher_code = Column(String(50), nullable=True)
    gst_tax = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String(30), default=BookingStatus.INITIATED.value, index=True)
    itinerary_snapshot_json = Column(Text, nullable=True) # Full snapshot of day-by-day plan at booking
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="bookings")
    payments = relationship("Payment", back_populates="booking", cascade="all, delete-orphan")
    legs = relationship("TripLeg", back_populates="booking", cascade="all, delete-orphan", order_by="TripLeg.leg_index")

class TripLeg(Base):
    __tablename__ = "trip_legs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    booking_id = Column(String(36), ForeignKey("bookings.id"), nullable=False, index=True)
    leg_index = Column(Integer, nullable=False) # 1, 2, 3...
    title = Column(String(255), nullable=False) # e.g. "Airport Pickup Cab"
    leg_type = Column(String(50), nullable=False) # CAB_PICKUP, FLIGHT, TRAIN, BUS, CAB_TRANSFER, HOTEL_CHECKIN, ACTIVITY_TRANSFER, RETURN_CAB
    status = Column(String(50), default="ASSIGNED") # SCHEDULED, ASSIGNED, DRIVER_EN_ROUTE, ARRIVED, IN_PROGRESS, COMPLETED
    scheduled_time = Column(String(100), nullable=True)
    pickup_location = Column(String(255), nullable=True)
    dropoff_location = Column(String(255), nullable=True)
    driver_name = Column(String(100), nullable=True)
    driver_phone = Column(String(50), nullable=True)
    vehicle_model = Column(String(100), nullable=True)
    vehicle_number = Column(String(50), nullable=True)
    otp_code = Column(String(20), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    booking = relationship("Booking", back_populates="legs")
    messages = relationship("DriverMessage", back_populates="leg", cascade="all, delete-orphan", order_by="DriverMessage.created_at")

class DriverMessage(Base):
    __tablename__ = "driver_messages"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    leg_id = Column(String(36), ForeignKey("trip_legs.id"), nullable=False, index=True)
    sender_type = Column(String(20), nullable=False) # "USER", "DRIVER", "SYSTEM"
    sender_name = Column(String(100), nullable=False)
    message_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    leg = relationship("TripLeg", back_populates="messages")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    booking_id = Column(String(36), ForeignKey("bookings.id"), nullable=False)
    razorpay_order_id = Column(String(100), unique=True, nullable=False, index=True)
    razorpay_payment_id = Column(String(100), unique=True, nullable=True, index=True)
    razorpay_signature = Column(String(255), nullable=True)
    amount_in_paise = Column(Integer, nullable=False)
    currency = Column(String(10), default="INR")
    payment_method = Column(String(50), nullable=True) # upi, card, netbanking, mock
    status = Column(String(30), default=PaymentStatus.CREATED.value)
    is_sandbox = Column(Boolean, default=True)
    error_code = Column(String(100), nullable=True)
    error_description = Column(Text, nullable=True)
    raw_payload_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    booking = relationship("Booking", back_populates="payments")

class TestFeedback(Base):
    __tablename__ = "test_feedback"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tester_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    session_id = Column(String(100), nullable=False, index=True)
    overall_rating = Column(Integer, nullable=False) # 1 - 5
    criteria_scores_json = Column(Text, nullable=False) # JSON: {pricing: 5, audio: 4, map: 5...}
    comments = Column(Text, nullable=True)
    bug_reports = Column(Text, nullable=True)
    device_info_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="feedbacks")

class TelemetryEvent(Base):
    __tablename__ = "telemetry_events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    session_id = Column(String(100), index=True, nullable=False)
    event_name = Column(String(100), index=True, nullable=False) # e.g. 'AUDIO_PLAYED', 'TIER_SWITCHED'
    event_payload_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class WishlistItem(Base):
    __tablename__ = "wishlist_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    session_id = Column(String(100), index=True, nullable=False)
    user_id = Column(String(36), nullable=True)
    trip_id = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Stakeholder(Base):
    """
    HR & Stakeholders Directory: Stores all stakeholder details across
    Core Team, Travel Creators, Chauffeurs/Fleet, Hotel Partners, Activity Vendors, and Investors.
    """
    __tablename__ = "stakeholders"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    full_name = Column(String(150), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    phone = Column(String(50), nullable=False, index=True)
    role_category = Column(String(50), default="CORE_TEAM", index=True) # CORE_TEAM, CREATOR, CHAUFFEUR, HOTEL_PARTNER, ACTIVITY_VENDOR, INVESTOR_ADVISOR
    designation = Column(String(100), nullable=False) # e.g. "Founder & CEO", "Lead Goa Chauffeur"
    department_or_destination = Column(String(100), default="General", index=True) # e.g. "Operations", "Goa", "Thailand", "Marketing"
    status = Column(String(30), default="ACTIVE", index=True) # ACTIVE, ONBOARDING, ON_LEAVE, INACTIVE
    employment_type = Column(String(50), default="FULL_TIME") # FULL_TIME, CONTRACTOR, CREATOR_PARTNER, FLEET_PARTNER, ADVISORY
    emergency_contact_name = Column(String(150), nullable=True)
    emergency_contact_phone = Column(String(50), nullable=True)
    payout_details = Column(String(255), nullable=True) # UPI ID, Bank IFSC, or PayPal
    compensation_model = Column(String(255), nullable=True) # e.g. "₹1,20,000 / month", "15% Booking Rev Share", "₹2,200 per airport transfer"
    joined_date = Column(String(50), nullable=True)
    documents_verified = Column(Boolean, default=True)
    social_handle = Column(String(100), nullable=True) # e.g. "@cometriipwme", "@rohini.explores"
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

