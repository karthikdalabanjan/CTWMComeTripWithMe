import json
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import CustomItinerary, WishlistItem
from backend.schemas import (
    CustomItineraryCreate, CustomItineraryResponse, WishlistToggleRequest
)

router = APIRouter(prefix="/trips", tags=["Trips & Itineraries"])

@router.post("/custom", response_model=CustomItineraryResponse)
def save_custom_itinerary(req: CustomItineraryCreate, db: Session = Depends(get_db)):
    """
    Saves a custom AI-generated or user-planned itinerary to the database.
    """
    itinerary = CustomItinerary(
        session_id=req.session_id,
        destination=req.destination,
        duration_days=req.duration_days,
        vibe=req.vibe,
        budget_tier=req.budget_tier,
        estimated_price=req.estimated_price,
        day_plans_json=json.dumps(req.day_plans)
    )
    db.add(itinerary)
    db.commit()
    db.refresh(itinerary)

    return CustomItineraryResponse(
        id=itinerary.id,
        destination=itinerary.destination,
        duration_days=itinerary.duration_days,
        vibe=itinerary.vibe,
        budget_tier=itinerary.budget_tier,
        estimated_price=itinerary.estimated_price,
        created_at=itinerary.created_at
    )

@router.get("/custom/{session_id}")
def get_custom_itineraries(session_id: str, db: Session = Depends(get_db)):
    """
    Fetches all custom itineraries created during a tester session.
    """
    items = db.query(CustomItinerary).filter(CustomItinerary.session_id == session_id).all()
    results = []
    for item in items:
        results.append({
            "id": item.id,
            "destination": item.destination,
            "duration_days": item.duration_days,
            "vibe": item.vibe,
            "budget_tier": item.budget_tier,
            "estimated_price": item.estimated_price,
            "day_plans": json.loads(item.day_plans_json),
            "created_at": item.created_at.isoformat()
        })
    return results

@router.post("/wishlist/toggle")
def toggle_wishlist(req: WishlistToggleRequest, db: Session = Depends(get_db)):
    """
    Toggles a trip in the user's saved wishlist.
    """
    existing = db.query(WishlistItem).filter(
        WishlistItem.session_id == req.session_id,
        WishlistItem.trip_id == req.trip_id
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        return {"saved": False, "trip_id": req.trip_id}
    else:
        item = WishlistItem(session_id=req.session_id, trip_id=req.trip_id)
        db.add(item)
        db.commit()
        return {"saved": True, "trip_id": req.trip_id}
