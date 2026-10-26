import json
from fastapi import APIRouter, Depends, HTTPException, Request, Header
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Booking, BookingStatus, Payment, PaymentStatus
from backend.schemas import (
    PaymentOrderCreateRequest, PaymentOrderResponse,
    PaymentVerifyRequest, PaymentVerifyResponse
)
from backend.services.payment import payment_service
from backend.config import settings

router = APIRouter(prefix="/payments", tags=["Payment Gateway (Razorpay)"])

@router.post("/create-order", response_model=PaymentOrderResponse)
def create_payment_order(req: PaymentOrderCreateRequest, db: Session = Depends(get_db)):
    """
    Creates a Razorpay Payment Gateway order for a booking.
    """
    booking = db.query(Booking).filter(Booking.id == req.booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    order_id, amount_paise, is_mock = payment_service.create_order(
        booking_ref=booking.booking_reference,
        amount_in_rupees=req.amount_in_rupees
    )

    # Save payment record in DB
    payment = Payment(
        booking_id=booking.id,
        razorpay_order_id=order_id,
        amount_in_paise=amount_paise,
        currency="INR",
        status=PaymentStatus.CREATED.value,
        is_sandbox=is_mock or not payment_service.is_live
    )
    db.add(payment)
    db.commit()

    return PaymentOrderResponse(
        razorpay_order_id=order_id,
        amount_in_paise=amount_paise,
        currency="INR",
        key_id=settings.RAZORPAY_KEY_ID or "rzp_test_mock_cometrip",
        is_mock=is_mock,
        booking_reference=booking.booking_reference
    )

@router.post("/verify", response_model=PaymentVerifyResponse)
def verify_payment(req: PaymentVerifyRequest, db: Session = Depends(get_db)):
    """
    Verifies payment signature from Razorpay checkout modal.
    Confirms booking and unlocks digital travel pass upon success.
    """
    booking = db.query(Booking).filter(Booking.id == req.booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    payment = db.query(Payment).filter(Payment.razorpay_order_id == req.razorpay_order_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment record not found")

    is_valid = payment_service.verify_payment_signature(
        razorpay_order_id=req.razorpay_order_id,
        razorpay_payment_id=req.razorpay_payment_id,
        razorpay_signature=req.razorpay_signature
    )

    if not is_valid:
        payment.status = PaymentStatus.FAILED.value
        payment.error_description = "HMAC signature verification failed"
        db.commit()
        raise HTTPException(status_code=400, detail="Invalid payment signature")

    # Update payment & booking status
    payment.razorpay_payment_id = req.razorpay_payment_id
    payment.razorpay_signature = req.razorpay_signature
    payment.payment_method = req.payment_method or "upi"
    payment.status = PaymentStatus.CAPTURED.value

    booking.status = BookingStatus.CONFIRMED.value
    db.commit()

    return PaymentVerifyResponse(
        success=True,
        booking_reference=booking.booking_reference,
        payment_id=req.razorpay_payment_id,
        status="CONFIRMED",
        message="Payment verified successfully! Travel pass confirmed.",
        voucher_url=f"/api/v1/bookings/{booking.booking_reference}"
    )

@router.post("/webhook")
async def razorpay_webhook(
    request: Request,
    x_razorpay_signature: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    Asynchronous Webhook endpoint for Razorpay payment notifications.
    """
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8")

    if x_razorpay_signature and not payment_service.verify_webhook_signature(body_str, x_razorpay_signature):
        raise HTTPException(status_code=400, detail="Invalid webhook signature")

    try:
        data = json.loads(body_str)
        event = data.get("event")

        if event == "payment.captured":
            payment_entity = data.get("payload", {}).get("payment", {}).get("entity", {})
            order_id = payment_entity.get("order_id")
            payment_id = payment_entity.get("id")

            if order_id:
                payment = db.query(Payment).filter(Payment.razorpay_order_id == order_id).first()
                if payment:
                    payment.status = PaymentStatus.CAPTURED.value
                    payment.razorpay_payment_id = payment_id
                    if payment.booking:
                        payment.booking.status = BookingStatus.CONFIRMED.value
                    db.commit()

        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
