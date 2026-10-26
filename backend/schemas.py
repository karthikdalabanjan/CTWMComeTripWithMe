from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

# ==================== User & Session ====================
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
