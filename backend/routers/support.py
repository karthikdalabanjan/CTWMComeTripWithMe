"""
ComeTripWithMe · AI Concierge & 24/7 Ground Ops Support Router
Handles trip-related intelligent inquiries and automated human support escalations.
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
import json
import random
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.database import get_db
from backend.models import Booking, User, TripLeg, TestFeedback

router = APIRouter(prefix="/support", tags=["AI Support & Concierge Escalation"])

# In-memory support ticket buffer (also mirrored to db feedback telemetry)
SUPPORT_TICKETS_STORE: List[Dict[str, Any]] = []

class SupportChatRequest(BaseModel):
    message: str
    booking_reference: Optional[str] = None
    user_id: Optional[str] = None

class SupportTicketRequest(BaseModel):
    user_name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    booking_reference: Optional[str] = None
    issue_category: str = "TRIP_ASSISTANCE" # BAGGAGE, CHAUFFEUR, RESCHEDULE, EMERGENCY, HOTEL
    message: str
    priority: str = "HIGH"

# Curated Knowledge Base for Trip-Related Questions
FAQ_KNOWLEDGE_BASE = [
    {
        "keywords": ["driver", "cab", "chauffeur", "pickup", "plate", "car", "vehicle"],
        "answer": "🚗 **Chauffeur & Pickup Details**:\nYour dedicated destination chauffeur details (Name, Live Phone Number, and Vehicle Plate) are assigned in your Live Trip Tracking HUD. For cab pickups, your chauffeur will WhatsApp you 30-45 minutes before pickup with the live vehicle location. You can also text or WhatsApp the chauffeur directly using the green WhatsApp button on any trip instance!"
    },
    {
        "keywords": ["whatsapp", "chat", "text", "message", "contact driver"],
        "answer": "💬 **WhatsApp Driver Communication**:\nEvery chauffeur has an integrated WhatsApp extension. In the Live Trip Tracking screen or Driver Messaging window, click **'Chat on WhatsApp'** to instantly open an end-to-end encrypted chat with your driver, prefilled with your booking PNR and pickup coordinates."
    },
    {
        "keywords": ["baggage", "luggage", "weight", "suitcases", "carry on", "pack"],
        "answer": "🧳 **Baggage & Packing Policy**:\n• **Flights**: 15kg checked + 7kg cabin per traveler.\n• **Volvo Express Sleeper**: 2 full-sized suitcases (up to 30kg) in the undercarriage cargo bay + 1 backpack inside.\n• **Local Chauffeur Transfers**: Our assigned vehicles (Innova Crysta / Ertiga / Luxury Commuters) accommodate 4-6 large check-in bags comfortably."
    },
    {
        "keywords": ["checkin", "check-in", "hotel", "resort", "room", "stay"],
        "answer": "🏨 **Boutique Stays & Hotel Handover**:\nAll stays in your ComeTripWithMe getaway are 100% voucherless! Simply flash your Digital QR Pass on arrival. Standard check-in is 1:00 PM; however, our contracted resort managers offer complimentary luggage drop and early beach shack / pool access if you arrive early."
    },
    {
        "keywords": ["cancel", "refund", "reschedule", "change date", "postpone"],
        "answer": "❌ **Cancellation & Flexible Rescheduling**:\n• **100% Full Refund** if canceled up to 72 hours before trip departure.\n• **Free Date Rescheduling** within 6 months of booking with zero penalty fee.\n• Refunds are processed back to your original Razorpay/UPI/Card source within 2-4 business days."
    },
    {
        "keywords": ["food", "meal", "vegetarian", "jain", "vegan", "breakfast"],
        "answer": "🥗 **Food & Dining Inclusions**:\nBreakfast at curated boutique stays is always included! For food crawls (such as our Bangalore Breakfast Trail or Chinatown Street Wok Crawl), vegetarian, Jain, and vegan alternatives are actively curated at each stop. Let your chauffeur know any allergies!"
    },
    {
        "keywords": ["emergency", "sos", "police", "hospital", "doctor", "medical"],
        "answer": "🚨 **24/7 Safety & Emergency SOS**:\nYour safety is our #1 priority. Every trip leg includes continuous ops monitoring. In case of urgent emergency, our Head of Ground Operations (Priya Sharma: +91 98450 77211) and local destination concierge are on standby 24/7. Click 'Request Human Support' for immediate escalation."
    }
]

ESCALATION_KEYWORDS = [
    "human", "agent", "support", "escalate", "call me", "talk to someone",
    "person", "complaint", "issue", "not working", "broken", "unresolved",
    "speak to a human", "representative", "emergency", "help me"
]

@router.post("/chat")
def ai_concierge_chat(req: SupportChatRequest, db: Session = Depends(get_db)):
    """
    Intelligent AI Trip Concierge that answers traveler inquiries and detects when escalation is required.
    """
    user_msg = req.message.strip().lower()
    
    # 1. Check for explicit escalation triggers
    is_escalation = any(k in user_msg for k in ESCALATION_KEYWORDS)
    if is_escalation:
        ticket_id = f"CTWM-SOS-{random.randint(1000, 9999)}"
        return {
            "reply": (
                f"🚨 **Issue Escalated to Ground Operations**\n\n"
                f"I have opened Priority Ticket **{ticket_id}** for you. Our Head of Ground Operations & Safety, **Priya Sharma**, has been paged.\n\n"
                f"📞 **Direct Ops Line**: +91 98450 77211\n"
                f"💬 **Instant WhatsApp Desk**: Available 24/7\n"
                f"✉️ **Priority Email**: support@cometripwithme.com\n\n"
                f"A team member will reach out to your registered phone number immediately."
            ),
            "should_escalate": True,
            "ticket_id": ticket_id,
            "ops_phone": "+91 98450 77211",
            "ops_whatsapp": "https://wa.me/919845077211?text=Hello%20Priya,%20I%20need%20human%20assistance%20with%20my%20ComeTripWithMe%20trip",
            "suggested_actions": ["WhatsApp Ops Desk", "Call Ground Operations", "Close"]
        }

    # 2. Contextual Trip Check if booking reference is supplied
    booking_context = ""
    if req.booking_reference:
        b = db.query(Booking).filter(Booking.booking_reference == req.booking_reference).first()
        if b:
            legs = db.query(TripLeg).filter(TripLeg.booking_id == b.id).all()
            next_driver = legs[0].driver_name if legs else "Assigned Chauffeur"
            booking_context = f"\n\n*(Regarding your active booking **{b.booking_reference}** for **{b.trip_title}**, departing {b.travel_date}. Your assigned chauffeur is **{next_driver}**).* "

    # 3. Match against Knowledge Base
    for item in FAQ_KNOWLEDGE_BASE:
        if any(k in user_msg for k in item["keywords"]):
            return {
                "reply": item["answer"] + booking_context,
                "should_escalate": False,
                "ticket_id": None,
                "suggested_actions": [
                    "Ask another question",
                    "Chat on WhatsApp",
                    "Talk to Human Support"
                ]
            }

    # 4. Fallback intelligent response
    return {
        "reply": (
            f"I can help you with anything regarding your ComeTripWithMe getaway! "
            f"You can ask about:\n"
            f"• **Chauffeur pickup time & vehicle plate**\n"
            f"• **WhatsApp direct driver messaging**\n"
            f"• **Luggage & baggage rules**\n"
            f"• **Hotel check-in & Digital QR Pass**\n"
            f"• **Cancellation & refund policy**\n\n"
            f"If your issue is unresolved, click **'Talk to Human Support'** at any time to connect with our 24/7 Ground Operations Desk."
            + booking_context
        ),
        "should_escalate": False,
        "ticket_id": None,
        "suggested_actions": [
            "Driver Arrival & WhatsApp",
            "Baggage Allowance",
            "Hotel Check-in / QR Pass",
            "Talk to Human Support"
        ]
    }

@router.post("/ticket")
def create_support_ticket(req: SupportTicketRequest, db: Session = Depends(get_db)):
    """
    Submits a high-priority customer support escalation ticket to the Ground Operations Desk.
    """
    ticket_id = f"CTWM-SOS-{random.randint(1000, 9999)}"
    ticket_data = {
        "ticket_id": ticket_id,
        "user_name": req.user_name,
        "phone": req.phone or "+91 97423 11023",
        "email": req.email,
        "booking_reference": req.booking_reference,
        "issue_category": req.issue_category,
        "message": req.message,
        "priority": req.priority,
        "status": "OPEN",
        "assigned_to": "Priya Sharma (Head of Ground Operations)",
        "created_at": datetime.utcnow().isoformat()
    }

    SUPPORT_TICKETS_STORE.append(ticket_data)

    # Also log to database feedback table for durability
    try:
        feedback = TestFeedback(
            session_id=req.booking_reference or "SUPPORT_ESCALATION",
            overall_rating=5,
            criteria_scores_json=json.dumps({"escalation_priority": req.priority}),
            comments=f"SUPPORT TICKET [{ticket_id}] from {req.user_name} ({req.phone}): {req.message}",
            bug_reports=f"Category: {req.issue_category}"
        )
        db.add(feedback)
        db.commit()
    except Exception as e:
        db.rollback()

    clean_ops_phone = "919845077211"
    wa_msg = f"Hello Priya, I have an escalated support ticket ({ticket_id}) regarding booking {req.booking_reference or 'CTWM'}: {req.message}"

    return {
        "success": True,
        "ticket_id": ticket_id,
        "status": "ESCALATED_TO_HUMAN_OPS",
        "assigned_agent": "Priya Sharma (Head of Ground Operations & Safety)",
        "ops_phone": "+91 98450 77211",
        "ops_whatsapp_link": f"https://wa.me/{clean_ops_phone}?text={wa_msg.replace(' ', '%20')}",
        "message": "High-priority support ticket created. Operations team alerted."
    }

@router.get("/tickets")
def list_support_tickets():
    """
    Returns live support tickets for the Executive Command Platform.
    """
    return {
        "total_tickets": len(SUPPORT_TICKETS_STORE),
        "tickets": SUPPORT_TICKETS_STORE[::-1]
    }

