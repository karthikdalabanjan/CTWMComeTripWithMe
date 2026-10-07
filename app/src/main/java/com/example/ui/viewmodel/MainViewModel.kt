package com.example.ui.viewmodel

import android.app.Application
import android.content.Intent
import android.net.Uri
import android.widget.Toast
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.local.ActiveTripEntity
import com.example.data.local.AppDatabase
import com.example.data.local.ItineraryWithSpots
import com.example.data.local.PackingItemEntity
import com.example.data.local.SpotRecommendationEntity
import com.example.data.local.TravelItineraryEntity
import com.example.data.local.WishlistEntity
import com.example.data.model.AudioStory
import com.example.data.model.ChannelType
import com.example.data.model.DestinationSpotlight
import com.example.data.model.InstagramPost
import com.example.data.model.StopLocation
import com.example.data.model.TravelerReview
import com.example.data.model.Trip
import com.example.data.model.TripVibe
import com.example.data.model.VideoProof
import com.example.data.repository.TripRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

enum class AppTab(val title: String, val iconName: String) {
    EXPLORE("Explore", "explore"),
    POCKET_GUIDE("Pocket Guide", "guide"),
    CREATOR_HUB("Proof & Videos", "video"),
    TRIP_PLANNER("Custom Plan", "planner"),
    SAVED_TRIPS("Saved", "bookmark")
}

data class SmartMatchState(
    val selectedDestinationId: String? = null,
    val selectedBudgetTier: Int? = null,
    val selectedTravelers: String = "2 of us",
    val travelDate: String = "",
    val recommendationTitle: String? = null,
    val recommendationSub: String? = null
)

class MainViewModel(application: Application) : AndroidViewModel(application) {

    private val database = AppDatabase.getInstance(application)
    private val repository = TripRepository(database.tripDao(), database.itineraryDao())

    // Navigation State
    private val _currentTab = MutableStateFlow(AppTab.EXPLORE)
    val currentTab: StateFlow<AppTab> = _currentTab.asStateFlow()

    // Selected Trip for detailed view
    private val _selectedTrip = MutableStateFlow<Trip?>(null)
    val selectedTrip: StateFlow<Trip?> = _selectedTrip.asStateFlow()

    // Smart Matcher State
    private val _smartMatchState = MutableStateFlow(SmartMatchState())
    val smartMatchState: StateFlow<SmartMatchState> = _smartMatchState.asStateFlow()

    // Active Audio Story playing in Pocket Guide
    private val _activeAudioStory = MutableStateFlow<Pair<AudioStory, String>?>(null)
    val activeAudioStory: StateFlow<Pair<AudioStory, String>?> = _activeAudioStory.asStateFlow()

    // Selected Channel Filter for Instagram Proof (Travel vs Food)
    private val _selectedInstagramChannel = MutableStateFlow<ChannelType?>(null)
    val selectedInstagramChannel: StateFlow<ChannelType?> = _selectedInstagramChannel.asStateFlow()

    // Active Day Index for the Live Pocket Guide
    private val _activeGuideDayIndex = MutableStateFlow(0)
    val activeGuideDayIndex: StateFlow<Int> = _activeGuideDayIndex.asStateFlow()

    // Selected Spot in Pocket Guide for deep dive inspection
    private val _inspectedSpot = MutableStateFlow<StopLocation?>(null)
    val inspectedSpot: StateFlow<StopLocation?> = _inspectedSpot.asStateFlow()

    // Room DB Flows
    val wishlist: StateFlow<List<WishlistEntity>> = repository.wishlistTrips
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    val activeTripEntity: StateFlow<ActiveTripEntity?> = repository.activeTrip
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), null)

    // Room Itineraries with Relational Spot Recommendations
    val roomItineraries: StateFlow<List<ItineraryWithSpots>> = repository.allRoomItineraries
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    val savedRoomItineraries: StateFlow<List<ItineraryWithSpots>> = repository.savedRoomItineraries
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    // Current active Trip model for the Pocket Guide
    val activeGuideTrip: StateFlow<Trip> = combine(activeTripEntity, _selectedTrip) { active, selected ->
        val tripId = active?.tripId ?: selected?.id ?: "goa"
        repository.getTripById(tripId) ?: repository.getAllTrips().first()
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), repository.getAllTrips().first())

    init {
        // Seed Room Database with rich curated creator itineraries
        viewModelScope.launch {
            repository.seedRoomItinerariesIfEmpty()
        }
        // Default smart match recommendation
        updateSmartMatch(destinationId = "goa", budget = 15000)
    }

    fun setTab(tab: AppTab) {
        _currentTab.value = tab
    }

    fun selectTrip(trip: Trip?) {
        _selectedTrip.value = trip
    }

    fun updateSmartMatch(destinationId: String?, budget: Int?) {
        val rec = repository.getSmartMatchRecommendation(destinationId, budget)
        _smartMatchState.value = _smartMatchState.value.copy(
            selectedDestinationId = destinationId,
            selectedBudgetTier = budget,
            recommendationTitle = rec?.first,
            recommendationSub = rec?.second
        )
    }

    fun setSmartTravelers(travelers: String) {
        _smartMatchState.value = _smartMatchState.value.copy(selectedTravelers = travelers)
    }

    fun setSmartDate(date: String) {
        _smartMatchState.value = _smartMatchState.value.copy(travelDate = date)
    }

    fun toggleWishlist(trip: Trip) {
        viewModelScope.launch {
            val isWishlisted = wishlist.value.any { it.tripId == trip.id }
            repository.toggleWishlist(trip, isWishlisted)
            val msg = if (isWishlisted) "Removed from wishlist" else "Added to wishlist ♡"
            Toast.makeText(getApplication(), msg, Toast.LENGTH_SHORT).show()
        }
    }

    fun startLivePocketGuide(trip: Trip) {
        viewModelScope.launch {
            repository.setActiveTrip(
                tripId = trip.id,
                squad = _smartMatchState.value.selectedTravelers,
                date = _smartMatchState.value.travelDate
            )
            _activeGuideDayIndex.value = 0
            _currentTab.value = AppTab.POCKET_GUIDE
            Toast.makeText(getApplication(), "Pocket Guide active for ${trip.name} ✦", Toast.LENGTH_SHORT).show()
        }
    }

    fun setGuideDay(dayIndex: Int) {
        _activeGuideDayIndex.value = dayIndex
    }

    fun inspectSpot(spot: StopLocation?) {
        _inspectedSpot.value = spot
    }

    fun playAudioStory(story: AudioStory, spotName: String) {
        _activeAudioStory.value = story to spotName
    }

    fun dismissAudioStory() {
        _activeAudioStory.value = null
    }

    fun setInstagramChannel(channel: ChannelType?) {
        _selectedInstagramChannel.value = channel
    }

    fun surpriseTrip(): Trip {
        val all = repository.getAllTrips()
        val random = all.random()
        selectTrip(random)
        Toast.makeText(getApplication(), "🎲 How about ${random.name}?", Toast.LENGTH_SHORT).show()
        return random
    }

    // External Launchers
    fun openInstagram(handle: String = "cometriipwme") {
        val cleanHandle = handle.replace("@", "")
        val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://instagram.com/$cleanHandle")).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK
        }
        try {
            getApplication<Application>().startActivity(intent)
        } catch (e: Exception) {
            Toast.makeText(getApplication(), "Unable to open Instagram", Toast.LENGTH_SHORT).show()
        }
    }

    fun openReel(reelUrl: String) {
        val url = if (reelUrl.isNotBlank()) reelUrl else "https://instagram.com/beyondbengalurufoods"
        val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url)).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK
        }
        try {
            getApplication<Application>().startActivity(intent)
        } catch (e: Exception) {
            Toast.makeText(getApplication(), "Opening Instagram Reel...", Toast.LENGTH_SHORT).show()
        }
    }

    fun openWhatsApp(message: String = "Hey ComeTripWithMe! I want to plan a trip.") {
        val encoded = Uri.encode(message)
        val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://wa.me/919742311023?text=$encoded")).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK
        }
        try {
            getApplication<Application>().startActivity(intent)
        } catch (e: Exception) {
            Toast.makeText(getApplication(), "WhatsApp not available", Toast.LENGTH_SHORT).show()
        }
    }

    fun openEmail(subject: String = "Trip Inquiry - ComeTripWithMe", body: String = "") {
        val intent = Intent(Intent.ACTION_SENDTO).apply {
            data = Uri.parse("mailto:bengalurufoodss@gmail.com")
            putExtra(Intent.EXTRA_SUBJECT, subject)
            putExtra(Intent.EXTRA_TEXT, body)
            flags = Intent.FLAG_ACTIVITY_NEW_TASK
        }
        try {
            getApplication<Application>().startActivity(intent)
        } catch (e: Exception) {
            Toast.makeText(getApplication(), "Email app not available", Toast.LENGTH_SHORT).show()
        }
    }

    fun callPhone() {
        val intent = Intent(Intent.ACTION_DIAL, Uri.parse("tel:+919742311023")).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK
        }
        try {
            getApplication<Application>().startActivity(intent)
        } catch (e: Exception) {
            Toast.makeText(getApplication(), "Phone dialer not available", Toast.LENGTH_SHORT).show()
        }
    }

    fun openYouTube(channel: String = "Cometripwithme") {
        val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://youtube.com/@$channel")).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK
        }
        try {
            getApplication<Application>().startActivity(intent)
        } catch (e: Exception) {
            Toast.makeText(getApplication(), "Unable to open YouTube", Toast.LENGTH_SHORT).show()
        }
    }

    fun subscribeNewsletter(email: String) {
        if (email.contains("@") && email.contains(".")) {
            Toast.makeText(getApplication(), "✦ You're in! First access to verified creator routes.", Toast.LENGTH_LONG).show()
        } else {
            Toast.makeText(getApplication(), "Please enter a valid email address.", Toast.LENGTH_SHORT).show()
        }
    }

    // Packing list
    fun getPackingItems(tripId: String) = repository.getPackingItems(tripId)

    fun togglePackingItem(item: PackingItemEntity) {
        viewModelScope.launch {
            repository.togglePackingItem(item)
        }
    }

    fun addPackingItem(tripId: String, title: String) {
        viewModelScope.launch {
            repository.addPackingItem(tripId, title)
        }
    }

    fun deletePackingItem(item: PackingItemEntity) {
        viewModelScope.launch {
            repository.deletePackingItem(item)
        }
    }

    fun getAllTrips(): List<Trip> = repository.getAllTrips()
    fun getSpotlights(): List<DestinationSpotlight> = repository.getDestinationSpotlights()
    fun getVideoProofs(): List<VideoProof> = repository.getVideoProofs()
    fun getInstagramPosts(): List<InstagramPost> = repository.getInstagramPosts(_selectedInstagramChannel.value)
    fun getTravelerReviews(): List<TravelerReview> = repository.getTravelerReviews()
}
