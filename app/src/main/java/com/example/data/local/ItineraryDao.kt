package com.example.data.local

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Transaction
import androidx.room.Update
import kotlinx.coroutines.flow.Flow

/**
 * Data Access Object (DAO) for managing travel itineraries and spot recommendations in Room.
 */
@Dao
interface ItineraryDao {

    // --- Query Itineraries with relational Spots ---

    @Transaction
    @Query("SELECT * FROM travel_itineraries ORDER BY createdAtTimestamp DESC")
    fun getAllItinerariesWithSpots(): Flow<List<ItineraryWithSpots>>

    @Transaction
    @Query("SELECT * FROM travel_itineraries WHERE itineraryId = :itineraryId LIMIT 1")
    fun getItineraryWithSpotsById(itineraryId: String): Flow<ItineraryWithSpots?>

    @Transaction
    @Query("SELECT * FROM travel_itineraries WHERE itineraryId = :itineraryId LIMIT 1")
    suspend fun getItineraryWithSpotsByIdOnce(itineraryId: String): ItineraryWithSpots?

    @Transaction
    @Query("SELECT * FROM travel_itineraries WHERE LOWER(destinationName) LIKE '%' || LOWER(:query) || '%' OR LOWER(title) LIKE '%' || LOWER(:query) || '%'")
    fun searchItineraries(query: String): Flow<List<ItineraryWithSpots>>

    @Transaction
    @Query("SELECT * FROM travel_itineraries WHERE LOWER(creatorHandle) = LOWER(:handle)")
    fun getItinerariesByCreator(handle: String): Flow<List<ItineraryWithSpots>>

    @Transaction
    @Query("SELECT * FROM travel_itineraries WHERE isSaved = 1 ORDER BY createdAtTimestamp DESC")
    fun getSavedItineraries(): Flow<List<ItineraryWithSpots>>

    // --- Direct Itinerary CRUD ---

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertItinerary(itinerary: TravelItineraryEntity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertItineraries(itineraries: List<TravelItineraryEntity>)

    @Update
    suspend fun updateItinerary(itinerary: TravelItineraryEntity)

    @Query("UPDATE travel_itineraries SET isSaved = :isSaved WHERE itineraryId = :itineraryId")
    suspend fun updateSavedStatus(itineraryId: String, isSaved: Boolean)

    @Query("DELETE FROM travel_itineraries WHERE itineraryId = :itineraryId")
    suspend fun deleteItineraryById(itineraryId: String)

    @Query("DELETE FROM travel_itineraries")
    suspend fun clearAllItineraries()

    // --- Spot Recommendations CRUD ---

    @Query("SELECT * FROM spot_recommendations WHERE itineraryId = :itineraryId ORDER BY dayNumber ASC, orderIndex ASC")
    fun getSpotsForItinerary(itineraryId: String): Flow<List<SpotRecommendationEntity>>

    @Query("SELECT * FROM spot_recommendations WHERE category = :category")
    fun getSpotsByCategory(category: String): Flow<List<SpotRecommendationEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertSpot(spot: SpotRecommendationEntity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertSpots(spots: List<SpotRecommendationEntity>)

    @Update
    suspend fun updateSpot(spot: SpotRecommendationEntity)

    @Delete
    suspend fun deleteSpot(spot: SpotRecommendationEntity)

    @Query("DELETE FROM spot_recommendations WHERE itineraryId = :itineraryId")
    suspend fun deleteSpotsForItinerary(itineraryId: String)

    // --- Atomic Combined Insert ---

    @Transaction
    suspend fun insertItineraryWithSpots(
        itinerary: TravelItineraryEntity,
        spots: List<SpotRecommendationEntity>
    ) {
        insertItinerary(itinerary)
        deleteSpotsForItinerary(itinerary.itineraryId)
        if (spots.isNotEmpty()) {
            insertSpots(spots)
        }
    }
}
