package com.example.data.local

import androidx.room.Embedded
import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.Index
import androidx.room.PrimaryKey
import androidx.room.Relation

/**
 * Room Entity representing a curated travel itinerary.
 * Stores destination name, creator profile info, reel link, Google Maps link, and overview metadata.
 */
@Entity(
    tableName = "travel_itineraries",
    indices = [
        Index(value = ["destinationName"]),
        Index(value = ["creatorHandle"])
    ]
)
data class TravelItineraryEntity(
    @PrimaryKey
    val itineraryId: String,
    val destinationName: String,
    val title: String,
    val tagline: String = "",
    val creatorName: String = "ComeTripWithMe",
    val creatorHandle: String = "@beyondbengalurufoods",
    val creatorBio: String = "Bengaluru food & travel creator sharing real verified routes.",
    val creatorAvatarUrl: String = "",
    val creatorVerified: Boolean = true,
    val duration: String = "3 Days / 2 Nights",
    val durationDays: Int = 3,
    val estimatedBudget: String = "₹8,999",
    val budgetValue: Int = 8999,
    val vibe: String = "BEACH",
    val reelUrl: String = "https://www.instagram.com/beyondbengalurufoods/",
    val mapLink: String = "https://maps.google.com/?q=Goa",
    val coverImageUrl: String = "",
    val summary: String = "",
    val bestSeason: String = "Oct - Mar",
    val tagsCsv: String = "Food,Beaches,Culture,Nightlife",
    val isSaved: Boolean = false,
    val createdAtTimestamp: Long = System.currentTimeMillis()
)

/**
 * Room Entity representing an individual spot recommendation within an itinerary.
 * Contains spot details, food/drink must-tries, Instagram Reel links with thumbnails, and Google Maps coordinates/links.
 */
@Entity(
    tableName = "spot_recommendations",
    foreignKeys = [
        ForeignKey(
            entity = TravelItineraryEntity::class,
            parentColumns = ["itineraryId"],
            childColumns = ["itineraryId"],
            onDelete = ForeignKey.CASCADE
        )
    ],
    indices = [
        Index(value = ["itineraryId"]),
        Index(value = ["category"])
    ]
)
data class SpotRecommendationEntity(
    @PrimaryKey
    val spotId: String,
    val itineraryId: String,
    val spotName: String,
    val category: String = "FOOD", // FOOD, CAFE, VIEWPOINT, SUNSET_POINT, HIDDEN_GEM, CULTURE, ACTIVITY
    val description: String = "",
    val mustTryItem: String = "",
    val approxCost: String = "₹500 for two",
    val reelUrl: String = "https://www.instagram.com/beyondbengalurufoods/",
    val reelThumbnailUrl: String = "",
    val reelCaption: String = "",
    val reelViews: String = "Reel 🎬",
    val mapLink: String = "https://maps.google.com/",
    val latitude: Double = 0.0,
    val longitude: Double = 0.0,
    val bestTimeToVisit: String = "Evening",
    val creatorTip: String = "",
    val dayNumber: Int = 1,
    val orderIndex: Int = 0,
    val isVerifiedByCreator: Boolean = true
)

/**
 * One-to-Many relational data model pairing a Travel Itinerary with all its recommended spots.
 */
data class ItineraryWithSpots(
    @Embedded
    val itinerary: TravelItineraryEntity,

    @Relation(
        parentColumn = "itineraryId",
        entityColumn = "itineraryId"
    )
    val spotRecommendations: List<SpotRecommendationEntity> = emptyList()
)
