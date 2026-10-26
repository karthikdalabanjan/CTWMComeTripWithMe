package com.example.data.model

data class BookingRequest(
    val bookingId: String,
    val tripId: String,
    val tripName: String,
    val travelerType: TravelerType,
    val groupSize: Int,
    val travelDate: String,
    val season: TravelSeason,
    val selectedAddOns: Set<String>,
    val contactName: String,
    val contactPhone: String,
    val contactEmail: String,
    val specialNotes: String,
    val pricingCalculation: PricingCalculation,
    val bookedAtTimestamp: Long = System.currentTimeMillis(),
    val status: BookingStatus = BookingStatus.CONFIRMED
)

enum class BookingStatus(val label: String, val badgeHex: Long) {
    CONFIRMED("Confirmed 🚀", 0xFF3CA082),
    PENDING_COORDINATION("Coordinator Connecting...", 0xFFE8C97A),
    COMPLETED("Completed ✨", 0xFF888888)
}

data class TravelVoucher(
    val voucherId: String,
    val tripTitle: String,
    val destination: String,
    val travelerName: String,
    val contactPhone: String,
    val travelerTier: String,
    val groupCount: Int,
    val travelDate: String,
    val durationText: String,
    val totalAmountPaid: String,
    val perPersonRate: String,
    val includedAddOns: List<String>,
    val emergencyCoordinator: String = "+91 98765 43210 (24/7 Creator Support)",
    val qrCodePayload: String
)
