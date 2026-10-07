package com.example.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "wishlist_trips")
data class WishlistEntity(
    @PrimaryKey val tripId: String,
    val name: String,
    val duration: String,
    val price: String,
    val imageUrl: String,
    val vibe: String,
    val addedTimestamp: Long = System.currentTimeMillis()
)

@Entity(tableName = "active_trip_state")
data class ActiveTripEntity(
    @PrimaryKey val id: String = "CURRENT_ACTIVE_TRIP",
    val tripId: String,
    val currentDayIndex: Int = 0,
    val completedStopIdsJson: String = "[]",
    val travelDate: String = "",
    val squadSize: String = "2 of us",
    val tripNotes: String = ""
)

@Entity(tableName = "trip_packing_items")
data class PackingItemEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val tripId: String,
    val itemTitle: String,
    val category: String,
    val isChecked: Boolean = false
)
