package com.example.data.model

data class AiChatMessage(
    val id: String,
    val text: String,
    val isFromUser: Boolean,
    val timestamp: Long = System.currentTimeMillis(),
    val customItinerary: CustomItineraryResult? = null,
    val isLoading: Boolean = false
)

data class CustomItineraryResult(
    val id: String,
    val destinationName: String,
    val title: String,
    val tagline: String,
    val duration: String,
    val vibe: TripVibe,
    val basePerPersonBudget: Int,
    val travelerPricingTable: Map<TravelerType, Int>,
    val offbeatSecretSpots: List<String>,
    val foodHighlights: List<String>,
    val dayWisePlans: List<CustomDayPlan>,
    val creatorVerdict: String,
    val isSavedToRoom: Boolean = false
)

data class CustomDayPlan(
    val dayNumber: Int,
    val title: String,
    val morningActivity: String,
    val afternoonActivity: String,
    val eveningActivity: String,
    val offbeatSecretSpot: String,
    val mustTryFoodSpot: String,
    val creatorTip: String
)
