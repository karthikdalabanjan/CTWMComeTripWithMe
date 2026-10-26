import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.database import get_db
from backend.models import TestFeedback, TelemetryEvent, Booking, Payment, User
from backend.schemas import (
    TestFeedbackCreate, TestFeedbackResponse, TelemetryEventCreate
)

router = APIRouter(prefix="/testing", tags=["Beta Testing & Criteria Telemetry"])

@router.post("/feedback", response_model=TestFeedbackResponse)
def submit_test_feedback(req: TestFeedbackCreate, db: Session = Depends(get_db)):
    """
    Submits tester feedback scoring all 6 evaluation criteria.
    """
    feedback = TestFeedback(
        session_id=req.session_id,
        overall_rating=req.overall_rating,
        criteria_scores_json=json.dumps(req.criteria_scores.dict()),
        comments=req.comments,
        bug_reports=req.bug_reports,
        device_info_json=json.dumps(req.device_info or {})
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return TestFeedbackResponse(
        id=feedback.id,
        message="Criteria feedback recorded successfully! Thank you for testing.",
        created_at=feedback.created_at
    )

@router.post("/event")
def log_telemetry_event(req: TelemetryEventCreate, db: Session = Depends(get_db)):
    """
    Logs frontend telemetry events (e.g. audio latency, tier switches, map loads).
    """
    event = TelemetryEvent(
        session_id=req.session_id,
        event_name=req.event_name,
        event_payload_json=json.dumps(req.payload or {})
    )
    db.add(event)
    db.commit()
    return {"status": "recorded", "event": req.event_name}

@router.get("/metrics")
def get_testing_dashboard_metrics(db: Session = Depends(get_db)):
    """
    Aggregates criteria scores, tester count, funnel conversion, and feedback comments.
    """
    total_feedbacks = db.query(TestFeedback).count()
    all_feedbacks = db.query(TestFeedback).all()

    # Aggregate criteria scores
    criteria_totals = {
        "CRIT-01_pricing_accuracy": 0.0,
        "CRIT-02_audio_guide_experience": 0.0,
        "CRIT-03_map_waypoint_rendering": 0.0,
        "CRIT-04_payment_sandbox_flow": 0.0,
        "CRIT-05_mobile_responsiveness": 0.0,
        "CRIT-06_offline_and_refresh_state": 0.0
    }
    
    recent_comments = []
    bug_reports = []

    for f in all_feedbacks:
        if f.comments:
            recent_comments.append({"rating": f.overall_rating, "comment": f.comments, "date": f.created_at.strftime("%Y-%m-%d %H:%M")})
        if f.bug_reports:
            bug_reports.append({"bug": f.bug_reports, "date": f.created_at.strftime("%Y-%m-%d %H:%M")})
        try:
            scores = json.loads(f.criteria_scores_json)
            criteria_totals["CRIT-01_pricing_accuracy"] += scores.get("pricing_accuracy", 0)
            criteria_totals["CRIT-02_audio_guide_experience"] += scores.get("audio_guide_experience", 0)
            criteria_totals["CRIT-03_map_waypoint_rendering"] += scores.get("map_waypoint_rendering", 0)
            criteria_totals["CRIT-04_payment_sandbox_flow"] += scores.get("payment_sandbox_flow", 0)
            criteria_totals["CRIT-05_mobile_responsiveness"] += scores.get("mobile_responsiveness", 0)
            criteria_totals["CRIT-06_offline_and_refresh_state"] += scores.get("offline_and_refresh_state", 0)
        except Exception:
            pass

    criteria_averages = {}
    if total_feedbacks > 0:
        for k, v in criteria_totals.items():
            criteria_averages[k] = round(v / total_feedbacks, 2)

    # Conversion Funnel
    total_bookings = db.query(Booking).count()
    confirmed_bookings = db.query(Booking).filter(Booking.status == "CONFIRMED").count()
    total_payments = db.query(Payment).count()
    captured_payments = db.query(Payment).filter(Payment.status == "CAPTURED").count()

    conversion_rate = round((confirmed_bookings / total_bookings * 100), 1) if total_bookings > 0 else 0.0

    return {
        "testing_program": {
            "total_feedback_submissions": total_feedbacks,
            "average_overall_rating": round(
                sum(f.overall_rating for f in all_feedbacks) / total_feedbacks, 2
            ) if total_feedbacks > 0 else 0.0,
            "criteria_benchmarks": criteria_averages,
            "recent_feedback": recent_comments[-10:],
            "active_bug_reports": bug_reports[-10:]
        },
        "funnel_analytics": {
            "total_bookings_initiated": total_bookings,
            "confirmed_bookings": confirmed_bookings,
            "checkout_conversion_rate": f"{conversion_rate}%",
            "payments_initiated": total_payments,
            "payments_captured": captured_payments
        }
    }
