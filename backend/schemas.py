from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

# ==================== User & Session & Profile ====================
class SessionRegisterRequest(BaseModel):
    session_id: str
    phone: Optional[str] = None
    email: Optional[str] = None
    display_name: Optional[str] = None
    device_info: Optional[Dict[str, Any]] = None

class SessionRegisterResponse(BaseModel):
    user_id: Optional[str] = None
    session_id: str
    is_beta_tester: bool = True
    message: str

class UserRegisterRequest(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    display_name: str
    password: str
    city: Optional[str] = "Bengaluru"

class UserLoginRequest(BaseModel):
    login_id: str # email or phone
    password: str

class UserProfileResponse(BaseModel):
    id: str
    email: Optional[str] = None
    phone: Optional[str] = None
    display_name: str
    city: str = "Bengaluru"
    avatar_url: Optional[str] = None
    is_beta_tester: bool = True
    token: str
    bookings_count: int = 0
    message: str = "Success"

class UserProfileUpdate(BaseModel):
    display_name: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    avatar_url: Optional[str] = None

# ==================== Itinerary ====================
class CustomItineraryCreate(BaseModel):
    session_id: str
    destination: str
    duration_days: int
    vibe: str
    budget_tier: str
    estimated_price: int
    day_plans: List[Dict[str, Any]]

class CustomItineraryResponse(BaseModel):
    id: str
    destination: str
    duration_days: int
    vibe: str
    budget_tier: str
    estimated_price: int
    created_at: datetime

# ==================== Booking ====================
class TravelerDetail(BaseModel):
    name: str
    phone: Optional[str] = ""
    email: Optional[str] = ""
    age: Optional[int] = None

class BookingInitiateRequest(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    trip_id: str
    trip_title: str
    tier: str # LUXURY, MID_TIER, BUDGET
    departure_city: str = "Bengaluru (BLR)"
    travel_date: str
    travelers_count: int = 1
    traveler_details: List[TravelerDetail]
    base_price: float
    discount_amount: float = 0.0
    voucher_code: Optional[str] = None
    gst_tax: float
    total_amount: float
    itinerary_snapshot: Optional[Dict[str, Any]] = None

class BookingResponse(BaseModel):
    booking_id: str
    booking_reference: str
    trip_title: str
    tier: str
    total_amount: float
    status: str
    travel_date: str
    departure_city: str
    travelers_count: int
    user_id: Optional[str] = None
    created_at: datetime

# ==================== Trip Legs & Live Driver Dispatch ====================
class TripLegResponse(BaseModel):
    id: str
    booking_id: str
    leg_index: int
    title: str
    leg_type: str
    status: str
    scheduled_time: Optional[str] = None
    pickup_location: Optional[str] = None
    dropoff_location: Optional[str] = None
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    vehicle_model: Optional[str] = None
    vehicle_number: Optional[str] = None
    otp_code: Optional[str] = None
    notes: Optional[str] = None
    messages_count: int = 0
    updated_at: Optional[datetime] = None

class TripLegUpdate(BaseModel):
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    vehicle_model: Optional[str] = None
    vehicle_number: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    scheduled_time: Optional[str] = None
    pickup_location: Optional[str] = None
    dropoff_location: Optional[str] = None

class DriverMessageCreate(BaseModel):
    sender_name: str
    sender_type: str = "USER" # USER, DRIVER
    message_text: str

class DriverMessageResponse(BaseModel):
    id: str
    leg_id: str
    sender_type: str
    sender_name: str
    message_text: str
    created_at: datetime

# ==================== Payment & Razorpay ====================
class PaymentOrderCreateRequest(BaseModel):
    booking_id: str
    amount_in_rupees: float

class PaymentOrderResponse(BaseModel):
    razorpay_order_id: str
    amount_in_paise: int
    currency: str
    key_id: str
    is_mock: bool
    booking_reference: str

class PaymentVerifyRequest(BaseModel):
    booking_id: str
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    payment_method: Optional[str] = "upi"

class PaymentVerifyResponse(BaseModel):
    success: bool
    booking_reference: str
    payment_id: str
    status: str
    message: str
    voucher_url: Optional[str] = None

# ==================== Beta Testing & Criteria Evaluation ====================
class CriteriaScores(BaseModel):
    pricing_accuracy: int = Field(ge=1, le=5, description="CRIT-01: Tier & pricing calculation clarity")
    audio_guide_experience: int = Field(ge=1, le=5, description="CRIT-02: Audio voice quality, narrative, controls")
    map_waypoint_rendering: int = Field(ge=1, le=5, description="CRIT-03: Route visualizer & GPS responsiveness")
    payment_sandbox_flow: int = Field(ge=1, le=5, description="CRIT-04: Checkout, UPI/Card modal, instant pass generation")
    mobile_responsiveness: int = Field(ge=1, le=5, description="CRIT-05: Mobile viewport, tap targets, animations")
    offline_and_refresh_state: int = Field(ge=1, le=5, description="CRIT-06: Local state retention, cart recovery")

class TestFeedbackCreate(BaseModel):
    session_id: str
    overall_rating: int = Field(ge=1, le=5)
    criteria_scores: CriteriaScores
    comments: Optional[str] = None
    bug_reports: Optional[str] = None
    device_info: Optional[Dict[str, Any]] = None

class TestFeedbackResponse(BaseModel):
    id: str
    message: str
    created_at: datetime

class TelemetryEventCreate(BaseModel):
    session_id: str
    event_name: str
    payload: Optional[Dict[str, Any]] = None

# ==================== Wishlist ====================
class WishlistToggleRequest(BaseModel):
    session_id: str
    trip_id: str

# ==================== HR & Stakeholders ====================
class StakeholderCreate(BaseModel):
    full_name: str
    email: Optional[str] = None
    phone: str
    role_category: str = "CORE_TEAM" # CORE_TEAM, CREATOR, CHAUFFEUR, HOTEL_PARTNER, ACTIVITY_VENDOR, INVESTOR_ADVISOR
    designation: str
    department_or_destination: str = "General"
    status: str = "ACTIVE" # ACTIVE, ONBOARDING, ON_LEAVE, INACTIVE
    employment_type: str = "FULL_TIME" # FULL_TIME, CONTRACTOR, CREATOR_PARTNER, FLEET_PARTNER, ADVISORY
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    payout_details: Optional[str] = None
    compensation_model: Optional[str] = None
    joined_date: Optional[str] = None
    documents_verified: bool = True
    social_handle: Optional[str] = None
    notes: Optional[str] = None

class StakeholderUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    role_category: Optional[str] = None
    designation: Optional[str] = None
    department_or_destination: Optional[str] = None
    status: Optional[str] = None
    employment_type: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    payout_details: Optional[str] = None
    compensation_model: Optional[str] = None
    joined_date: Optional[str] = None
    documents_verified: Optional[bool] = None
    social_handle: Optional[str] = None
    notes: Optional[str] = None

class StakeholderResponse(BaseModel):
    id: str
    full_name: str
    email: Optional[str] = None
    phone: str
    role_category: str
    designation: str
    department_or_destination: str
    status: str
    employment_type: str
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    payout_details: Optional[str] = None
    compensation_model: Optional[str] = None
    joined_date: Optional[str] = None
    documents_verified: bool
    social_handle: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

class HRMetricsResponse(BaseModel):
    total_stakeholders: int
    categories_breakdown: Dict[str, int]
    status_breakdown: Dict[str, int]
    active_drivers_count: int
    verified_creators_count: int
    core_team_count: int

