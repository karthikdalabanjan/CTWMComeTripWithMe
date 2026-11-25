"""
ComeTripWithMe · Autonomous AI Agents API Router
Endpoints for Development, Operations, and Marketing Agents.
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Booking, TripLeg
from backend.services.agents import DevAgentService, OpsAgentService, MarketingAgentService

router = APIRouter(prefix="/agents", tags=["Autonomous AI Agents (Dev, Ops, Marketing)"])

# Request Schemas
class ScaffoldTripRequest(BaseModel):
    destination: str
    duration: str = "4D · 3N"
    state_or_country: str = "India"

class AutoDispatchRequest(BaseModel):
    booking_reference: str

class ReelCampaignRequest(BaseModel):
    destination: str = "Goa"
    tier: str = "MID_TIER"

class WhatsAppCampaignRequest(BaseModel):
    destination: str = "Goa"
    discount_code: str = "SQUAD2026"

class CreatorPitchRequest(BaseModel):
    creator_name: str = "Rohini"
    niche: str = "Luxury Beach Stays & Cafes"
    location: str = "Bengaluru"

# Endpoints
@router.get("/status")
def get_agents_status(db: Session = Depends(get_db)):
    """
    Returns live operating status, tasks, and telemetry for all 3 agents.
    """
    fleet = OpsAgentService.get_fleet_telemetry(db)
    audit = DevAgentService.run_system_audit()

    return {
        "status": "ALL_SYSTEMS_OPERATIONAL",
        "timestamp": audit["timestamp"],
        "agents": {
            "dev_agent": {
                "name": "DevAgent",
                "role": "Cloud Architect & Codebase Reliability",
                "state": "ACTIVE",
                "system_health": audit["status"],
                "database_engine": audit["database_engine"],
                "total_tables": audit["total_tables"]
            },
            "ops_agent": {
                "name": "OpsAgent",
                "role": "24/7 Driver Dispatch & Transit Operations",
                "state": "ACTIVE",
                "active_trip_legs": fleet["total_legs_active"],
                "fleet_status": fleet["dispatch_readiness"]
            },
            "marketing_agent": {
                "name": "MarketingAgent",
                "role": "Creator Viral Growth & WhatsApp Campaigns",
                "state": "ACTIVE",
                "campaigns_ready": 7,
                "supported_channels": ["Instagram Reels", "WhatsApp Broadcast", "Creator Pitch"]
            }
        }
    }

# ==================== Dev Agent ====================
@router.post("/dev/audit")
def run_dev_agent_audit():
    """
    DevAgent: Runs automated system diagnostic, database check, and SLA verification.
    """
    return DevAgentService.run_system_audit()

@router.post("/dev/scaffold-trip")
def scaffold_trip(req: ScaffoldTripRequest):
    """
    DevAgent: Generates full code and tier structure for a new travel destination.
    """
    return DevAgentService.scaffold_new_trip(req.destination, req.duration, req.state_or_country)

# ==================== Ops Agent ====================
@router.post("/ops/dispatch")
def auto_dispatch_booking(req: AutoDispatchRequest, db: Session = Depends(get_db)):
    """
    OpsAgent: Automatically assigns chauffeurs and updates destination phone numbers.
    """
    res = OpsAgentService.auto_dispatch_booking_legs(req.booking_reference, db)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res

@router.get("/ops/fleet")
def get_fleet_telemetry(db: Session = Depends(get_db)):
    """
    OpsAgent: Returns real-time fleet overview, active leg counts, and chauffeur communication.
    """
    return OpsAgentService.get_fleet_telemetry(db)

@router.get("/ops/notify/{booking_ref}")
def generate_traveler_notification(booking_ref: str, db: Session = Depends(get_db)):
    """
    OpsAgent: Generates personalized traveler dispatch SMS/WhatsApp notification.
    """
    booking = db.query(Booking).filter(Booking.booking_reference == booking_ref).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    leg = db.query(TripLeg).filter(TripLeg.booking_id == booking.id).first()
    if not leg:
        raise HTTPException(status_code=404, detail="Trip leg not found")

    sms = OpsAgentService.generate_traveler_dispatch_sms(booking, leg)
    return {
        "booking_reference": booking_ref,
        "recipient": booking.traveler_details_json,
        "notification_text": sms
    }

# ==================== Marketing Agent ====================
@router.post("/marketing/reel")
def generate_reel_campaign(req: ReelCampaignRequest):
    """
    MarketingAgent: Generates viral Instagram Reel hook, shot list, caption, and hashtags.
    """
    return MarketingAgentService.generate_reel_campaign(req.destination, req.tier)

@router.post("/marketing/whatsapp")
def generate_whatsapp_campaign(req: WhatsAppCampaignRequest):
    """
    MarketingAgent: Generates high-converting WhatsApp broadcast message with squad discount.
    """
    return {
        "destination": req.destination,
        "discount_code": req.discount_code,
        "broadcast_message": MarketingAgentService.generate_whatsapp_broadcast(req.destination, req.discount_code)
    }

@router.post("/marketing/creator-pitch")
def generate_creator_pitch(req: CreatorPitchRequest):
    """
    MarketingAgent: Generates personalized creator sponsorship pitch email.
    """
    return MarketingAgentService.generate_creator_pitch(req.creator_name, req.niche, req.location)

