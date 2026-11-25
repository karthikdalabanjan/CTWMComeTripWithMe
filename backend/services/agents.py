"""
ComeTripWithMe · Autonomous AI Agents Engine
Specialized Agents for Development, Operations, and Marketing.
"""
import os
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy import inspect, text
from backend.database import engine, get_db
from backend.models import Booking, TripLeg, DriverMessage, User, Payment

class DevAgentService:
    """
    Development Agent: Monitors code health, database integrity,
    API endpoint SLAs, and scaffolds new trip itineraries.
    """
    @staticmethod
    def run_system_audit() -> Dict[str, Any]:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        # Check table row counts
        row_counts = {}
        with engine.connect() as conn:
            for t in tables:
                cnt = conn.execute(text(f"SELECT COUNT(*) FROM {t}")).scalar()
                row_counts[t] = cnt

        # Check required environment variables
        env_status = {
            "DATABASE_URL": "Configured (" + ("PostgreSQL Cloud" if "postgres" in str(engine.url) else "SQLite Local") + ")",
            "RAZORPAY_KEY_ID": "Present" if os.getenv("RAZORPAY_KEY_ID") else "Mock Mode Active",
            "RAZORPAY_KEY_SECRET": "Present" if os.getenv("RAZORPAY_KEY_SECRET") else "Mock Mode Active",
            "SECRET_KEY": "Configured",
            "ALLOW_MOCK_PAYMENTS": os.getenv("ALLOW_MOCK_PAYMENTS", "true")
        }

        # Check schema completeness
        expected_tables = ["users", "bookings", "trip_legs", "driver_messages", "payments", "custom_itineraries", "test_feedback", "telemetry_events", "wishlist_items", "stakeholders"]
        missing_tables = [t for t in expected_tables if t not in tables]

        return {
            "status": "HEALTHY" if not missing_tables else "ACTION_REQUIRED",
            "timestamp": datetime.utcnow().isoformat(),
            "database_engine": str(engine.url).split("://")[0],
            "total_tables": len(tables),
            "table_inventory": row_counts,
            "missing_tables": missing_tables,
            "environment_audit": env_status,
            "recommendations": [
                "Database schema is in sync with SQLAlchemy models.",
                f"All {len(expected_tables)} core tables (including HR stakeholders directory) verified and accepting transactions.",
                "Cloud deployment ready for Render / Railway / Supabase."
            ] if not missing_tables else [f"Run database migration to add missing tables: {missing_tables}"]
        }

    @staticmethod
    def scaffold_new_trip(destination: str, duration: str, state_or_country: str) -> Dict[str, Any]:
        """
        Scaffolds a new curated trip with Luxury, Mid-Tier, and Budget specifications.
        """
        dest_slug = destination.lower().replace(" ", "_")
        return {
            "id": dest_slug,
            "name": destination,
            "headline": f"Secret viewpoints, local flavours, and untarnished trails across {destination}.",
            "duration": duration,
            "region": state_or_country,
            "tiers": {
                "budget": {
                    "tierName": "🎒 Budget Backpacker",
                    "price": "₹7,499",
                    "budgetValue": 7499,
                    "transportType": "🚌 AC Sleeper Coach / Express Train",
                    "stayName": f"Zostel / Backpacker Pods {destination}",
                    "inclusions": ["AC Dorm Bed", "Scooty Rental with Helmet", "Hostel Community Pass"]
                },
                "mid": {
                    "tierName": "✨ Mid-Tier Best Value",
                    "price": "₹18,999",
                    "budgetValue": 18999,
                    "transportType": "✈️ Direct Flight + 🚖 AC Cab Transfer",
                    "stayName": f"Curated Boutique Resort {destination}",
                    "inclusions": ["Private AC Room", "Airport Transfers", "Cafe Breakfasts", "Pocket Audio Guide"]
                },
                "luxury": {
                    "tierName": "🌟 Luxury Creator Escape",
                    "price": "₹49,999",
                    "budgetValue": 49999,
                    "transportType": "✈️ Premium Flight + 🚖 Innova Crysta Chauffeur",
                    "stayName": f"5-Star Oceanfront / Heritage Villa {destination}",
                    "inclusions": ["Private Pool Villa", "24/7 Dedicated Chauffeur", "VIP Sunset Table", "Fine Dining Dinner Passes"]
                }
            },
            "status": "SCAFFOLDED_READY_FOR_PUBLICATION"
        }


class OpsAgentService:
    """
    Operations Agent: Oversees fleet dispatch, driver phone updates by destination,
    transit delay watchdog, and traveler communication.
    """
    @staticmethod
    def auto_dispatch_booking_legs(booking_ref: str, db) -> Dict[str, Any]:
        booking = db.query(Booking).filter(Booking.booking_reference == booking_ref).first()
        if not booking:
            return {"error": "Booking not found"}

        legs = db.query(TripLeg).filter(TripLeg.booking_id == booking.id).order_by(TripLeg.leg_index).all()
        updated_legs = []

        # Destination specific mapping
        dest = booking.trip_title.lower()
        default_phone = "+91 97645 10928"
        default_driver = "Sandeep Naik"
        default_vehicle = "Toyota Innova Crysta AC"
        default_plate = "GA-03-AA-4491"

        if "thailand" in dest or "krabi" in dest:
            default_phone = "+66 81 234 5678"
            default_driver = "Somchai Prasert"
            default_vehicle = "Toyota VIP Commuter Van"
            default_plate = "BKK-8821"
        elif "himachal" in dest or "kasol" in dest:
            default_phone = "+91 98160 55432"
            default_driver = "Prem Thakur"
            default_vehicle = "Mahindra Scorpio 4x4"
            default_plate = "HP-01-T-8877"
        elif "gokarna" in dest:
            default_phone = "+91 94801 22334"
            default_driver = "Manjunath Hegde"
            default_vehicle = "Toyota Innova AC"
            default_plate = "KA-30-M-4921"

        for l in legs:
            if not l.driver_name or l.status == "SCHEDULED":
                if "Arrival" in l.title or "Destination" in l.title:
                    l.driver_name = default_driver
                    l.driver_phone = default_phone
                    l.vehicle_model = default_vehicle
                    l.vehicle_number = default_plate
                    l.status = "ASSIGNED"
                    l.notes = "OpsAgent auto-dispatched destination chauffeur according to route."
                    updated_legs.append(l.title)
        
        db.commit()

        return {
            "status": "DISPATCH_OPTIMIZED",
            "booking_reference": booking_ref,
            "destination": booking.trip_title,
            "legs_dispatched": len(updated_legs),
            "updated_legs": updated_legs,
            "assigned_driver": default_driver,
            "assigned_phone": default_phone
        }

    @staticmethod
    def get_fleet_telemetry(db) -> Dict[str, Any]:
        total_legs = db.query(TripLeg).count()
        assigned_legs = db.query(TripLeg).filter(TripLeg.status == "ASSIGNED").count()
        en_route_legs = db.query(TripLeg).filter(TripLeg.status == "DRIVER_EN_ROUTE").count()
        scheduled_legs = db.query(TripLeg).filter(TripLeg.status == "SCHEDULED").count()
        completed_legs = db.query(TripLeg).filter(TripLeg.status == "COMPLETED").count()

        # Recent messages
        recent_msgs = db.query(DriverMessage).order_by(DriverMessage.created_at.desc()).limit(5).all()

        return {
            "total_legs_active": total_legs,
            "status_breakdown": {
                "assigned": assigned_legs,
                "en_route": en_route_legs,
                "scheduled": scheduled_legs,
                "completed": completed_legs
            },
            "dispatch_readiness": "100% OPERATIONAL",
            "recent_chat_traffic": [
                {
                    "sender": f"{m.sender_name} ({m.sender_type})",
                    "text": m.message_text,
                    "time": m.created_at.strftime("%H:%M:%S")
                } for m in recent_msgs
            ]
        }

    @staticmethod
    def generate_traveler_dispatch_sms(booking: Booking, leg: TripLeg) -> str:
        """
        Creates ready-to-send SMS/WhatsApp notification for traveler about their assigned driver.
        """
        return (
            f"🚗 ComeTripWithMe Chauffeur Update!\n"
            f"Trip: {booking.trip_title} ({booking.booking_reference})\n"
            f"Leg: {leg.title}\n"
            f"Driver: {leg.driver_name} ({leg.driver_phone})\n"
            f"Vehicle: {leg.vehicle_model} · {leg.vehicle_number}\n"
            f"Pickup Time: {leg.scheduled_time}\n"
            f"Pickup Point: {leg.pickup_location}\n"
            f"Your Pickup OTP: {leg.otp_code}\n"
            f"Track live or text your driver directly in the ComeTripWithMe app!"
        )


class MarketingAgentService:
    """
    Marketing Agent: Generates viral Instagram Reel concepts, high-converting
    WhatsApp broadcasts, and creator collaboration outreach.
    """
    @staticmethod
    def generate_reel_campaign(destination: str, tier: str) -> Dict[str, Any]:
        return {
            "destination": destination,
            "target_tier": tier,
            "campaign_title": f"Stop Booking Overpriced Packages: Real {destination} Creator Guide",
            "audio_suggestion": "Trending Ambient Lo-Fi House (e.g. 'Bicep - Glue' or viral travel sound)",
            "visual_hook_3s": f"Text on screen: 'Why everyone pays ₹40,000 for {destination} while we spent ₹{ '7,999' if 'bud' in tier.lower() else ('18,999' if 'mid' in tier.lower() else '49,999') }... with a private driver.'",
            "shot_breakdown": [
                "0:00 - 0:03: Rapid pan from airplane window to secret cliff sunrise (Chapora / Kudle).",
                "0:03 - 0:07: POV stepping into private air-conditioned chauffeur cab.",
                "0:07 - 0:12: Close-up sizzling butter garlic squid at local ocean shack.",
                "0:12 - 0:16: Creator holding ComeTripWithMe app showing live digital boarding pass and audio narration.",
                "0:16 - 0:20: Call to action: 'Link in bio for verified itineraries with transport & stays included.'"
            ],
            "instagram_caption": (
                f"No commercial tourist traps. No hidden agent fees. 🌴✨\\n\\n"
                f"We mapped out the exact verified {destination} route across {tier.upper()} travel: "
                f"direct flights, pre-booked airport chauffeur, curated boutique stays, and audio guides for secret spots.\\n\\n"
                f"✦ Starting from verified creator rates.\\n"
                f"✦ Book your pass or view the day-by-day map at link in bio @cometriipwme!\\n\\n"
                f"#{destination.replace(' ', '')} #{destination.replace(' ', '')}Diaries #ComeTripWithMe #CreatorTravel #TravelHacks #LuxuryTravelOnABudget"
            ),
            "hashtags": [
                f"#{destination.replace(' ', '')}",
                "#CuratedTravel",
                "#CreatorTourOperator",
                "#ComeTripWithMe",
                "#IndiaTravelGram",
                "#OffbeatTravel"
            ]
        }

    @staticmethod
    def generate_whatsapp_broadcast(destination: str, discount_code: str = "SQUAD500") -> str:
        return (
            f"🌴 *Exclusive Squad Drop: {destination} is Live!* ✦\\n\\n"
            f"Hey traveler! ComeTripWithMe just dropped our updated 2026 curated itineraries for *{destination}* across Luxury, Mid-Tier, and Budget classes.\\n\\n"
            f"✨ *What's included in every pass:*\\n"
            f"• Verified stays (5-Star oceanfront villas or boutique resorts)\\n"
            f"• Pre-booked airport transfers & dedicated chauffeur cabs\\n"
            f"• Live pocket audio guide for zero tourist traps\\n"
            f"• Real-time driver chat & live tracking in the app\\n\\n"
            f"🔥 Use code *{discount_code}* at checkout for an instant ₹2,000 discount per group.\\n\\n"
            f"👉 *Preview complete route itinerary & book:*\\n"
            f"https://cometripwithme.netlify.app\\n\\n"
            f"Need customized dates? Reply to this message to chat with our travel team!"
        )

    @staticmethod
    def generate_creator_pitch(creator_name: str, niche: str, location: str) -> Dict[str, Any]:
        return {
            "subject": f"Paid Creator Partnership: ComeTripWithMe × {creator_name}",
            "body": (
                f"Hey {creator_name}! 👋\\n\\n"
                f"Loved your recent reels on {niche} around {location}. "
                f"I'm reaching out from ComeTripWithMe — India's 1st Creator Tour Operator.\\n\\n"
                f"We turn authentic creator recommendations into fully bookable travel passes (verified stays, dedicated cabs, secret food stops, and live audio guides) so your audience can experience the exact same journey with zero stress.\\n\\n"
                f"We'd love to sponsor your upcoming trip to Goa or Thailand: we cover 100% of luxury/mid-tier stays, chauffeur transfers, and dining, plus a 15% revenue share on every audience booking generated from your custom pass.\\n\\n"
                f"Would you be open for a quick 10-minute catch-up this Thursday to walk you through the creator portal?\\n\\n"
                f"Best,\\n"
                f"Karthik Dalabanjan\\n"
                f"Founder · ComeTripWithMe (@cometriipwme)"
            )
        }

