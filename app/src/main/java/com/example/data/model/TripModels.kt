package com.example.data.model

data class Trip(
    val id: String,
    val name: String,
    val headline: String,
    val description: String,
    val vibe: TripVibe,
    val duration: String,
    val price: String,
    val budgetValue: Int,
    val imageUrl: String,
    val heroTags: List<String>,
    val totalEstimateDetails: String,
    val creatorNote: String,
    val youtubeVideoId: String = "",
    val days: List<DayPlan>
)

enum class TripVibe(val label: String, val emoji: String, val badgeColorHex: Long) {
    PARTY("Party", "🎉", 0xFFDC503C),
    BACKPACKING("Backpacking", "🎒", 0xFF354259),
    CHILL("Chill & Slow", "🏔️", 0xFF3CA082),
    LUXURY("Luxury Escapes", "✨", 0xFFE8C97A),
    HERITAGE("Ancient Heritage", "🏛️", 0xFFB37D4E)
}

data class DayPlan(
    val dayNumber: Int,
    val title: String,
    val summary: String,
    val stops: List<StopLocation>,
    val foodSpots: List<FoodSpot>,
    val creatorSecretTip: String
)

data class StopLocation(
    val id: String,
    val name: String,
    val timing: String,
    val category: String,
    val description: String,
    val insiderTip: String,
    val photoUrl: String,
    val lat: Double = 0.0,
    val lng: Double = 0.0,
    val audioStory: AudioStory? = null
)

data class AudioStory(
    val title: String,
    val narrator: String = "ComeTripWithMe Creator",
    val durationSeconds: Int,
    val scriptText: String
)

data class FoodSpot(
    val name: String,
    val specialty: String,
    val recommendedBy: String = "@beyondbengalurufoods",
    val mustTryDish: String,
    val approxCostForTwo: String,
    val reelThumbnailUrl: String = "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600&q=80",
    val reelUrl: String = "https://www.instagram.com/beyondbengalurufoods/",
    val reelCaption: String = "Watch the full food review & vibe reel on Instagram",
    val reelViews: String = "Reel 🎬"
)

data class VideoProof(
    val id: String,
    val title: String,
    val destination: String,
    val duration: String,
    val views: String,
    val thumbnailUrl: String,
    val videoUrl: String,
    val highlights: List<String>
)

data class InstagramPost(
    val id: String,
    val handle: String, // @cometriipwme or @beyondbenaglurufoods
    val channelType: ChannelType,
    val caption: String,
    val location: String,
    val imageUrl: String,
    val likesCount: String
)

enum class ChannelType {
    TRAVEL, FOOD
}

data class TravelerReview(
    val id: String,
    val authorHandle: String,
    val city: String,
    val tripTag: String,
    val rating: Int = 5,
    val reviewQuote: String,
    val verified: Boolean = true
)

data class DestinationSpotlight(
    val id: String,
    val title: String,
    val subtitle: String,
    val region: String,
    val documentedSpotsCount: String,
    val imageUrl: String,
    val tags: List<String>
)
