package com.example.data.local

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import kotlinx.coroutines.flow.Flow

@Dao
interface TripDao {
    // Wishlist
    @Query("SELECT * FROM wishlist_trips ORDER BY addedTimestamp DESC")
    fun getAllWishlist(): Flow<List<WishlistEntity>>

    @Query("SELECT EXISTS(SELECT 1 FROM wishlist_trips WHERE tripId = :tripId)")
    fun isWishlisted(tripId: String): Flow<Boolean>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertWishlist(item: WishlistEntity)

    @Query("DELETE FROM wishlist_trips WHERE tripId = :tripId")
    suspend fun deleteWishlistById(tripId: String)

    // Active Trip State
    @Query("SELECT * FROM active_trip_state WHERE id = 'CURRENT_ACTIVE_TRIP' LIMIT 1")
    fun getActiveTrip(): Flow<ActiveTripEntity?>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun saveActiveTrip(activeTrip: ActiveTripEntity)

    @Query("DELETE FROM active_trip_state WHERE id = 'CURRENT_ACTIVE_TRIP'")
    suspend fun clearActiveTrip()

    // Packing checklist
    @Query("SELECT * FROM trip_packing_items WHERE tripId = :tripId ORDER BY id ASC")
    fun getPackingItems(tripId: String): Flow<List<PackingItemEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertPackingItem(item: PackingItemEntity)

    @Update
    suspend fun updatePackingItem(item: PackingItemEntity)

    @Delete
    suspend fun deletePackingItem(item: PackingItemEntity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertPackingItems(items: List<PackingItemEntity>)
}
