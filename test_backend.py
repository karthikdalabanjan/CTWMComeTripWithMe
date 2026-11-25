#!/usr/bin/env python3
"""
ComeTripWithMe Backend Integration & Criteria Test Suite
Tests all endpoints: Auth, Itineraries, Bookings, Razorpay Payments, Telemetry, and Testing Metrics.
"""
import requests
import sys

BASE_URL = "http://localhost:8000"

def run_tests():
    print("======================================================")
    print("🧪 Running Full E2E Test Suite against FastAPI Backend")
    print("======================================================\n")

    # 1. Healthcheck
    try:
        r = requests.get(f"{BASE_URL}/")
    except requests.exceptions.ConnectionError:
        print("❌ Error: FastAPI server is not running on http://localhost:8000")
        print("   Start it first using: python3 run_backend.py")
        sys.exit(1)

    assert r.status_code == 200, f"Root check failed: {r.status_code}"
    data = r.json()
    print(f"1. [PASS] Health Check: Status={data['status']}, Service={data['service']}")
    print(f"   Payment Provider: {data['payment_gateway']['provider']} ({data['payment_gateway']['mode']})")

    # 2. Auth Registration & User Login
    reg_payload = {
        "email": "tester.ksd@example.com",
        "phone": "+91 97423 11023",
        "display_name": "Karthik Beta Tester",
        "password": "testerpassword2026",
        "city": "Bengaluru"
    }
    r = requests.post(f"{BASE_URL}/api/v1/auth/register", json=reg_payload)
    if r.status_code == 400 and "already exists" in r.text:
        r = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
            "login_id": "tester.ksd@example.com",
            "password": "testerpassword2026"
        })
    assert r.status_code == 200, f"User auth failed: {r.text}"
    user_data = r.json()
    user_id = user_data["id"]
    print(f"2. [PASS] User Account & Auth: User ID={user_id}, Name={user_data['display_name']}, City={user_data['city']}")

    # 2b. Session registration for telemetry
    session_id = "tester_session_beta_8821"
    r = requests.post(f"{BASE_URL}/api/v1/auth/session", json={
        "session_id": session_id,
        "email": "tester.ksd@example.com",
        "display_name": "Karthik Beta Tester",
        "device_info": {"device": "MacBook Pro", "os": "macOS 15", "browser": "Chrome 122"}
    })
    assert r.status_code == 200

    # 3. Custom Itinerary
    r = requests.post(f"{BASE_URL}/api/v1/trips/custom", json={
        "session_id": session_id,
        "destination": "Gokarna Beaches & Cliffside Trek",
        "duration_days": 3,
        "vibe": "CHILL",
        "budget_tier": "MID_TIER",
        "estimated_price": 11500,
        "day_plans": [
            {"day": 1, "title": "Kudle Beach Sunset & Cliff Cafe", "stops": ["Kudle Beach", "Namaste Cafe"]},
            {"day": 2, "title": "Om Beach Trek & Dolphin View", "stops": ["Om Beach", "Half Moon Beach"]},
            {"day": 3, "title": "Mirjan Fort & Coastal Drive", "stops": ["Mirjan Fort"]}
        ]
    })
    assert r.status_code == 200, f"Custom itinerary failed: {r.text}"
    itinerary = r.json()
    print(f"3. [PASS] Custom Itinerary Saved: Destination={itinerary['destination']}, Budget=₹{itinerary['estimated_price']}")

    # 4. Wishlist Toggle
    r = requests.post(f"{BASE_URL}/api/v1/trips/wishlist/toggle", json={
        "session_id": session_id,
        "trip_id": "gokarna_escape"
    })
    assert r.status_code == 200 and r.json()["saved"] is True
    print("4. [PASS] Wishlist Persistence: Added trip to saved wishlist")

    # 5. Booking Initiation
    booking_payload = {
        "session_id": session_id,
        "trip_id": "gokarna_escape",
        "trip_title": "Gokarna Beach & Cliffside Trek",
        "tier": "MID_TIER",
        "departure_city": "Bengaluru (BLR)",
        "travel_date": "2026-11-20",
        "travelers_count": 2,
        "traveler_details": [
            {"name": "Karthik", "phone": "9876543210", "email": "tester.ksd@example.com", "age": 26},
            {"name": "Companion", "phone": "9876543211", "email": "companion@example.com", "age": 25}
        ],
        "base_price": 23000.0,
        "discount_amount": 2000.0,
        "voucher_code": "EARLYBIRD",
        "gst_tax": 1050.0,
        "total_amount": 22050.0
    }
    r = requests.post(f"{BASE_URL}/api/v1/bookings/initiate", json=booking_payload)
    assert r.status_code == 200, f"Booking initiation failed: {r.text}"
    booking = r.json()
    booking_ref = booking["booking_reference"]
    booking_id = booking["booking_id"]
    print(f"5. [PASS] Booking Initiated: Ref={booking_ref}, Tier={booking['tier']}, Total=₹{booking['total_amount']}")

    # 6. Razorpay Payment Gateway Order Creation
    r = requests.post(f"{BASE_URL}/api/v1/payments/create-order", json={
        "booking_id": booking_id,
        "amount_in_rupees": 22050.0
    })
    assert r.status_code == 200, f"Payment order creation failed: {r.text}"
    order_data = r.json()
    print(f"6. [PASS] Razorpay Order Generated: Order ID={order_data['razorpay_order_id']}, Amount={order_data['amount_in_paise']} paise")

    # 7. Payment Signature Verification & Confirmation
    r = requests.post(f"{BASE_URL}/api/v1/payments/verify", json={
        "booking_id": booking_id,
        "razorpay_order_id": order_data["razorpay_order_id"],
        "razorpay_payment_id": "pay_test_live_77192",
        "razorpay_signature": "mock_signature_success",
        "payment_method": "upi"
    })
    assert r.status_code == 200, f"Payment verification failed: {r.text}"
    verify_data = r.json()
    print(f"7. [PASS] Payment Verification: Status={verify_data['status']}, Booking Confirmed!")

    # 8. Booking Travel Pass & QR Generation
    r = requests.get(f"{BASE_URL}/api/v1/bookings/{booking_ref}")
    assert r.status_code == 200, f"Pass fetch failed: {r.text}"
    pass_data = r.json()
    assert pass_data["is_confirmed"] is True
    print(f"8. [PASS] Digital Travel Pass: Status={pass_data['status']}, Confirmed={pass_data['is_confirmed']}")
    print(f"   Pass QR URL: {pass_data['digital_pass_qr']}")

    # 8b. Trip Legs & Live Driver Dispatch
    r = requests.get(f"{BASE_URL}/api/v1/bookings/{booking_ref}/legs")
    assert r.status_code == 200, f"Fetch legs failed: {r.text}"
    legs = r.json()
    assert len(legs) >= 6, f"Expected at least 6 trip legs, got {len(legs)}"
    leg1 = legs[0]
    print(f"8b. [PASS] Live Trip Tracker: {len(legs)} instances verified!")
    print(f"    Leg 1: {leg1['title']} | Driver: {leg1['driver_name']} ({leg1['driver_phone']})")

    # 8c. Update Driver Phone Number according to destination
    leg3 = [l for l in legs if l["leg_index"] == 3][0]
    r = requests.put(f"{BASE_URL}/api/v1/bookings/legs/{leg3['id']}", json={
        "driver_name": "Sandeep Naik (Gokarna Operator)",
        "driver_phone": "+91 94801 99887",
        "vehicle_number": "KA-30-M-7711",
        "notes": "Driver phone updated for destination pickup by operator"
    })
    assert r.status_code == 200
    print(f"8c. [PASS] Operator Update: Driver phone updated to {r.json()['leg']['driver_phone']}!")

    # 8d. Traveler Texts the Driver & Receives Driver Reply
    r = requests.post(f"{BASE_URL}/api/v1/bookings/legs/{leg3['id']}/messages", json={
        "sender_name": "Karthik",
        "sender_type": "USER",
        "message_text": "Hi Sandeep, where are you parked at the station?"
    })
    assert r.status_code == 200
    chat_thread = r.json()
    assert len(chat_thread) >= 2
    print(f"8d. [PASS] Driver Text Chat: Received reply from driver:")
    print(f"    Driver: {chat_thread[-1]['message_text']}")

    # 9. Telemetry Event Logging
    r = requests.post(f"{BASE_URL}/api/v1/testing/event", json={
        "session_id": session_id,
        "event_name": "AUDIO_PLAYED",
        "payload": {"story_id": "gokarna_story_1", "duration_seconds": 45, "playback_speed": 1.0}
    })
    assert r.status_code == 200
    print("9. [PASS] Telemetry Event Stream: Recorded AUDIO_PLAYED event")

    # 10. Beta Tester Feedback on all 6 Criteria
    feedback_payload = {
        "session_id": session_id,
        "overall_rating": 5,
        "criteria_scores": {
            "pricing_accuracy": 5,
            "audio_guide_experience": 5,
            "map_waypoint_rendering": 4,
            "payment_sandbox_flow": 5,
            "mobile_responsiveness": 5,
            "offline_and_refresh_state": 4
        },
        "comments": "Razorpay payment flow was instantaneous. Gokarna audio guide and tier breakdown are excellent.",
        "bug_reports": None,
        "device_info": {"device": "MacBook Pro", "resolution": "1920x1080", "browser": "Chrome"}
    }
    r = requests.post(f"{BASE_URL}/api/v1/testing/feedback", json=feedback_payload)
    assert r.status_code == 200
    print("10. [PASS] Tester 6-Criteria Evaluation: Feedback and ratings recorded")

    # 11. Tester Metrics Dashboard API
    r = requests.get(f"{BASE_URL}/api/v1/testing/metrics")
    assert r.status_code == 200
    metrics = r.json()
    print("\n======================================================")
    print("📊 Live Metrics Dashboard Summary")
    print("======================================================")
    print(f"Total Tester Submissions: {metrics['testing_program']['total_feedback_submissions']}")
    print(f"Average Overall Rating:   {metrics['testing_program']['average_overall_rating']} / 5.0")
    print("Criteria Benchmarks:")
    for k, v in metrics["testing_program"]["criteria_benchmarks"].items():
        print(f"  • {k}: {v} / 5.0")
    print(f"Funnel Conversion Rate:   {metrics['funnel_analytics']['checkout_conversion_rate']}")
    print(f"Confirmed Bookings:       {metrics['funnel_analytics']['confirmed_bookings']}")
    print("\n✅ All 11 E2E Integration Tests Passed Successfully!")

if __name__ == "__main__":
    run_tests()
