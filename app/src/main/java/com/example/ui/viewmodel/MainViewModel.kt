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
import com.example.data.model.AiChatMessage
import com.example.data.model.AudioStory
import com.example.data.model.BookingStatus
import com.example.data.model.ChannelType
import com.example.data.model.CustomItineraryResult
import com.example.data.model.DestinationSpotlight
import com.example.data.model.InstagramPost
import com.example.data.model.PricingCalculation
import com.example.data.model.PricingEngine
import com.example.data.model.StopLocation
import com.example.data.model.TravelSeason
import com.example.data.model.TravelVoucher
import com.example.data.model.TravelerReview
import com.example.data.model.TravelerType
import com.example.data.model.Trip
import com.example.data.model.TripVibe
import com.example.data.model.VideoProof
import com.example.data.repository.TripRepository
import com.example.data.service.GeminiAiService
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

enum class AppTab(val title: String, val iconName: String) {
    EXPLORE("Explore", "explore"),
    BOOK_ITINERARY("Book Trips", "book"),
    AI_CHAT_PLANNER("AI Copilot", "ai"),
    POCKET_GUIDE("Pocket Guide", "guide"),
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
    private val geminiService = GeminiAiService()

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

    // --- AI CHATBOT COPILOT STATE ---
    private val _chatMessages = MutableStateFlow<List<AiChatMessage>>(
        listOf(
            AiChatMessage(
                id = "welcome_1",
                text = "👋 Hey traveler! I'm your **ComeTripWithMe AI Copilot**.\n\nTell me where you want to go, your travel squad (Solo, Couple, Friends, Family, Luxury VIP), and duration or budget. I'll build you an offbeat custom route with verified @beyondbengalurufoods spots and itemized transparent group pricing!",
                isFromUser = false
            )
        )
    )
    val chatMessages: StateFlow<List<AiChatMessage>> = _chatMessages.asStateFlow()

    private val _isAiThinking = MutableStateFlow(false)
    val isAiThinking: StateFlow<Boolean> = _isAiThinking.asStateFlow()

    // --- BOOKING STATE ---
    private val _selectedBookingTripId = MutableStateFlow("spiti")
    val selectedBookingTripId: StateFlow<String> = _selectedBookingTripId.asStateFlow()

    private val _selectedTravelerType = MutableStateFlow(TravelerType.FRIENDS_SQUAD)
    val selectedTravelerType: StateFlow<TravelerType> = _selectedTravelerType.asStateFlow()

    private val _selectedGroupSize = MutableStateFlow(4)
    val selectedGroupSize: StateFlow<Int> = _selectedGroupSize.asStateFlow()

    private val _selectedTravelSeason = MutableStateFlow(TravelSeason.REGULAR)
    val selectedTravelSeason: StateFlow<TravelSeason> = _selectedTravelSeason.asStateFlow()

    private val _selectedAddOnIds = MutableStateFlow<Set<String>>(setOf("food_tour"))
    val selectedAddOnIds: StateFlow<Set<String>> = _selectedAddOnIds.asStateFlow()

    private val _bookingContactName = MutableStateFlow("Alex Sharma")
    val bookingContactName: StateFlow<String> = _bookingContactName.asStateFlow()

    private val _bookingContactPhone = MutableStateFlow("+91 98765 43210")
    val bookingContactPhone: StateFlow<String> = _bookingContactPhone.asStateFlow()

    private val _bookingContactEmail = MutableStateFlow("traveler@cometripwithme.in")
    val bookingContactEmail: StateFlow<String> = _bookingContactEmail.asStateFlow()

    private val _bookingTravelDate = MutableStateFlow("15 Oct 2026")
    val bookingTravelDate: StateFlow<String> = _bookingTravelDate.asStateFlow()

    private val _bookingSpecialNotes = MutableStateFlow("We love vegetarian food and scenic golden hour viewpoints!")
    val bookingSpecialNotes: StateFlow<String> = _bookingSpecialNotes.asStateFlow()

    // Generated Vouchers
    private val _activeVouchers = MutableStateFlow<List<TravelVoucher>>(emptyList())
    val activeVouchers: StateFlow<List<TravelVoucher>> = _activeVouchers.asStateFlow()

    private val _selectedVoucherForModal = MutableStateFlow<TravelVoucher?>(null)
    val selectedVoucherForModal: StateFlow<TravelVoucher?> = _selectedVoucherForModal.asStateFlow()

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

    // --- AI CHATBOT COPILOT METHODS ---
    fun sendAiChatMessage(userMessage: String) {
        if (userMessage.isBlank()) return
        val userMsg = AiChatMessage(
            id = "user_${System.currentTimeMillis()}",
            text = userMessage,
            isFromUser = true
        )
        _chatMessages.value = _chatMessages.value + userMsg
        _isAiThinking.value = true

        viewModelScope.launch {
            try {
                val (replyText, customItinerary) = geminiService.generateCustomItinerary(
                    userPrompt = userMessage,
                    destinationHint = null,
                    durationDaysHint = 4,
                    budgetHint = 15000,
                    preferredVibe = TripVibe.BACKPACKING,
                    travelerGroupHint = _selectedTravelerType.value
                )
                val assistantMsg = AiChatMessage(
                    id = "assistant_${System.currentTimeMillis()}",
                    text = replyText,
                    isFromUser = false,
                    customItinerary = customItinerary
                )
                _chatMessages.value = _chatMessages.value + assistantMsg
            } catch (e: Exception) {
                val errorMsg = AiChatMessage(
                    id = "error_${System.currentTimeMillis()}",
                    text = "I encountered an issue generating your plan. Let me connect you directly to our travel desk or try another prompt!",
                    isFromUser = false
                )
                _chatMessages.value = _chatMessages.value + errorMsg
            } finally {
                _isAiThinking.value = false
            }
        }
    }

    fun saveCustomItineraryToRoom(customResult: CustomItineraryResult) {
        viewModelScope.launch {
            val entity = TravelItineraryEntity(
                itineraryId = customResult.id,
                destinationName = customResult.destinationName,
                title = customResult.title,
                tagline = customResult.tagline,
                duration = customResult.duration,
                durationDays = customResult.dayWisePlans.size,
                estimatedBudget = "₹${customResult.basePerPersonBudget}",
                budgetValue = customResult.basePerPersonBudget,
                vibe = customResult.vibe.name,
                coverImageUrl = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800&q=80",
                summary = customResult.creatorVerdict,
                isSaved = true
            )
            val spots = customResult.dayWisePlans.mapIndexed { idx, day ->
                SpotRecommendationEntity(
                    spotId = "spot_${customResult.id}_$idx",
                    itineraryId = customResult.id,
                    spotName = day.offbeatSecretSpot,
                    category = "OFFBEAT_GEM",
                    description = "${day.morningActivity}. ${day.eveningActivity}",
                    creatorTip = day.creatorTip,
                    mustTryItem = day.mustTryFoodSpot,
                    approxCost = "₹${customResult.basePerPersonBudget / customResult.dayWisePlans.size}",
                    dayNumber = day.dayNumber,
                    orderIndex = idx
                )
            }
            database.itineraryDao().insertItinerary(entity)
            database.itineraryDao().insertSpots(spots)

            // Update in-memory chat message state
            _chatMessages.value = _chatMessages.value.map { msg ->
                if (msg.customItinerary?.id == customResult.id) {
                    msg.copy(customItinerary = msg.customItinerary.copy(isSavedToRoom = true))
                } else msg
            }
            Toast.makeText(getApplication(), "Saved '${customResult.title}' to Room Database! ✦", Toast.LENGTH_SHORT).show()
        }
    }

    fun startBookingForTrip(trip: Trip) {
        _selectedBookingTripId.value = trip.id
        _currentTab.value = AppTab.BOOK_ITINERARY
    }

    fun startBookingForDestinationId(destinationId: String) {
        val matchingTrip = repository.getTripById(destinationId) ?: repository.getAllTrips().find {
            it.id.contains(destinationId, ignoreCase = true) || destinationId.contains(it.id, ignoreCase = true)
        }
        if (matchingTrip != null) {
            _selectedBookingTripId.value = matchingTrip.id
        } else {
            _selectedBookingTripId.value = "spiti"
        }
        _currentTab.value = AppTab.BOOK_ITINERARY
        Toast.makeText(getApplication(), "Configuring booking for itinerary...", Toast.LENGTH_SHORT).show()
    }

    fun startBookingForCustom(customResult: CustomItineraryResult) {
        _selectedBookingTripId.value = "custom"
        _currentTab.value = AppTab.BOOK_ITINERARY
        Toast.makeText(getApplication(), "Configuring booking for ${customResult.destinationName}...", Toast.LENGTH_SHORT).show()
    }

    // --- BOOKING LOGIC METHODS ---
    fun setBookingTrip(tripId: String) {
        _selectedBookingTripId.value = tripId
    }

    fun setBookingTravelerType(type: TravelerType) {
        _selectedTravelerType.value = type
        // adjust default group size if needed
        when (type) {
            TravelerType.SOLO_BACKPACKER -> _selectedGroupSize.value = 1
            TravelerType.COUPLE_DUO -> _selectedGroupSize.value = 2
            TravelerType.FRIENDS_SQUAD -> if (_selectedGroupSize.value < 3) _selectedGroupSize.value = 4
            TravelerType.FAMILY_KIDS_ELDERS -> if (_selectedGroupSize.value < 3) _selectedGroupSize.value = 4
            TravelerType.LUXURY_VIP -> if (_selectedGroupSize.value < 1) _selectedGroupSize.value = 2
        }
    }

    fun setBookingGroupSize(size: Int) {
        _selectedGroupSize.value = size.coerceIn(1, 16)
    }

    fun setBookingSeason(season: TravelSeason) {
        _selectedTravelSeason.value = season
    }

    fun toggleBookingAddOn(addonId: String) {
        val current = _selectedAddOnIds.value.toMutableSet()
        if (current.contains(addonId)) current.remove(addonId) else current.add(addonId)
        _selectedAddOnIds.value = current
    }

    fun updateBookingContact(
        name: String = _bookingContactName.value,
        phone: String = _bookingContactPhone.value,
        email: String = _bookingContactEmail.value,
        date: String = _bookingTravelDate.value,
        notes: String = _bookingSpecialNotes.value
    ) {
        _bookingContactName.value = name
        _bookingContactPhone.value = phone
        _bookingContactEmail.value = email
        _bookingTravelDate.value = date
        _bookingSpecialNotes.value = notes
    }

    fun calculateCurrentBookingPricing(): PricingCalculation {
        val trip = repository.getTripById(_selectedBookingTripId.value)
        val budgetValue = trip?.budgetValue ?: 16999
        return PricingEngine.calculate(
            tripBudgetValue = budgetValue,
            travelerType = _selectedTravelerType.value,
            groupSize = _selectedGroupSize.value,
            season = _selectedTravelSeason.value,
            selectedAddOnIds = _selectedAddOnIds.value
        )
    }

    fun confirmBookingAndGenerateVoucher(): TravelVoucher {
        val trip = repository.getTripById(_selectedBookingTripId.value)
        val tripTitle = trip?.name ?: "Custom Creator Expedition"
        val tripDuration = trip?.duration ?: "5D / 4N"
        val calc = calculateCurrentBookingPricing()

        val addOnNames = _selectedAddOnIds.value.mapNotNull { id ->
            com.example.data.model.AVAILABLE_ADD_ONS.find { it.id == id }?.name
        }

        val voucher = TravelVoucher(
            voucherId = "CTWM-${System.currentTimeMillis().toString().takeLast(6)}",
            tripTitle = tripTitle,
            destination = trip?.headline ?: "Curated Creator Itinerary",
            travelerName = _bookingContactName.value,
            contactPhone = _bookingContactPhone.value,
            travelerTier = _selectedTravelerType.value.title,
            groupCount = _selectedGroupSize.value,
            travelDate = _bookingTravelDate.value,
            durationText = tripDuration,
            totalAmountPaid = "₹${String.format("%,d", calc.totalGroupPrice)}",
            perPersonRate = "₹${String.format("%,d", calc.perPersonFinalPrice)} / person",
            includedAddOns = addOnNames,
            qrCodePayload = "CTWM-VERIFIED-${_selectedBookingTripId.value}-${_bookingContactPhone.value}"
        )

        _activeVouchers.value = listOf(voucher) + _activeVouchers.value
        _selectedVoucherForModal.value = voucher
        Toast.makeText(getApplication(), "🎉 Booking confirmed! Voucher generated.", Toast.LENGTH_LONG).show()
        return voucher
    }

    fun openWhatsAppForBooking(voucher: TravelVoucher) {
        val msg = """
            👋 Hey ComeTripWithMe Team! I would like to confirm my booking:
            
            🎫 Voucher ID: ${voucher.voucherId}
            📍 Trip: ${voucher.tripTitle} (${voucher.durationText})
            📅 Departure Date: ${voucher.travelDate}
            👥 Traveler Squad: ${voucher.travelerTier} (${voucher.groupCount} travelers)
            💰 Total Package Price: ${voucher.totalAmountPaid} (${voucher.perPersonRate})
            ✨ Add-ons Included: ${voucher.includedAddOns.joinToString(", ")}
            👤 Lead Traveler: ${voucher.travelerName} (${voucher.contactPhone})
            
            Please assign our dedicated local fixer & coordinator!
        """.trimIndent()
        openWhatsApp(msg)
    }

    fun dismissVoucherModal() {
        _selectedVoucherForModal.value = null
    }

    fun getAllTrips(): List<Trip> = repository.getAllTrips()
    fun getSpotlights(): List<DestinationSpotlight> = repository.getDestinationSpotlights()
    fun getVideoProofs(): List<VideoProof> = repository.getVideoProofs()
    fun getInstagramPosts(): List<InstagramPost> = repository.getInstagramPosts(_selectedInstagramChannel.value)
    fun getTravelerReviews(): List<TravelerReview> = repository.getTravelerReviews()
}
