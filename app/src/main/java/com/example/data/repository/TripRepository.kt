package com.example.data.repository

import com.example.data.local.ActiveTripEntity
import com.example.data.local.ItineraryDao
import com.example.data.local.ItineraryWithSpots
import com.example.data.local.PackingItemEntity
import com.example.data.local.SpotRecommendationEntity
import com.example.data.local.TravelItineraryEntity
import com.example.data.local.TripDao
import com.example.data.local.WishlistEntity
import com.example.data.model.AudioStory
import com.example.data.model.ChannelType
import com.example.data.model.DayPlan
import com.example.data.model.DestinationSpotlight
import com.example.data.model.FoodSpot
import com.example.data.model.InstagramPost
import com.example.data.model.StopLocation
import com.example.data.model.TravelerReview
import com.example.data.model.Trip
import com.example.data.model.TripVibe
import com.example.data.model.VideoProof
import kotlinx.coroutines.flow.Flow

class TripRepository(
    private val tripDao: TripDao,
    private val itineraryDao: ItineraryDao
) {

    val wishlistTrips: Flow<List<WishlistEntity>> = tripDao.getAllWishlist()
    val activeTrip: Flow<ActiveTripEntity?> = tripDao.getActiveTrip()

    // Room Itineraries with Relational Spots
    val allRoomItineraries: Flow<List<ItineraryWithSpots>> = itineraryDao.getAllItinerariesWithSpots()
    val savedRoomItineraries: Flow<List<ItineraryWithSpots>> = itineraryDao.getSavedItineraries()

    fun getRoomItineraryWithSpots(itineraryId: String): Flow<ItineraryWithSpots?> =
        itineraryDao.getItineraryWithSpotsById(itineraryId)

    fun searchRoomItineraries(query: String): Flow<List<ItineraryWithSpots>> =
        itineraryDao.searchItineraries(query)

    fun getRoomItinerariesByCreator(handle: String): Flow<List<ItineraryWithSpots>> =
        itineraryDao.getItinerariesByCreator(handle)

    suspend fun saveItineraryWithSpots(
        itinerary: TravelItineraryEntity,
        spots: List<SpotRecommendationEntity>
    ) = itineraryDao.insertItineraryWithSpots(itinerary, spots)

    suspend fun toggleItinerarySaved(itineraryId: String, isSaved: Boolean) =
        itineraryDao.updateSavedStatus(itineraryId, isSaved)

    suspend fun deleteRoomItinerary(itineraryId: String) =
        itineraryDao.deleteItineraryById(itineraryId)

    suspend fun seedRoomItinerariesIfEmpty() {
        CURATED_TRIPS.forEach { trip ->
            val existing = itineraryDao.getItineraryWithSpotsByIdOnce(trip.id)
            if (existing == null) {
                val itineraryEntity = TravelItineraryEntity(
                    itineraryId = trip.id,
                    destinationName = trip.name,
                    title = trip.headline,
                    tagline = trip.description,
                    creatorName = "ComeTripWithMe",
                    creatorHandle = if (trip.id == "t2" || trip.id == "t3") "@beyondbengalurufoods" else "@cometriipwme",
                    creatorBio = "Verified travel & food routes curated without tour agency fluff.",
                    creatorAvatarUrl = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=200&q=80",
                    creatorVerified = true,
                    duration = trip.duration,
                    durationDays = trip.days.size,
                    estimatedBudget = trip.price,
                    budgetValue = trip.budgetValue,
                    vibe = trip.vibe.name,
                    reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                    mapLink = "https://maps.google.com/?q=${trip.name}",
                    coverImageUrl = trip.imageUrl,
                    summary = trip.totalEstimateDetails,
                    bestSeason = "All Season",
                    tagsCsv = trip.heroTags.joinToString(","),
                    isSaved = false
                )

                val spots = mutableListOf<SpotRecommendationEntity>()
                var orderCounter = 0

                trip.days.forEach { day ->
                    day.stops.forEach { stop ->
                        spots.add(
                            SpotRecommendationEntity(
                                spotId = "${trip.id}_d${day.dayNumber}_s${stop.id}",
                                itineraryId = trip.id,
                                spotName = stop.name,
                                category = stop.category,
                                description = stop.description,
                                mustTryItem = stop.insiderTip,
                                approxCost = "Included / Free",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelThumbnailUrl = stop.photoUrl,
                                reelCaption = stop.name,
                                reelViews = "Verified 📍",
                                mapLink = "https://maps.google.com/?q=${stop.lat},${stop.lng}",
                                latitude = stop.lat,
                                longitude = stop.lng,
                                bestTimeToVisit = stop.timing,
                                creatorTip = stop.insiderTip,
                                dayNumber = day.dayNumber,
                                orderIndex = orderCounter++
                            )
                        )
                    }

                    day.foodSpots.forEach { food ->
                        spots.add(
                            SpotRecommendationEntity(
                                spotId = "${trip.id}_d${day.dayNumber}_f_${food.name.lowercase().replace(" ", "_")}",
                                itineraryId = trip.id,
                                spotName = food.name,
                                category = "FOOD",
                                description = food.specialty,
                                mustTryItem = food.mustTryDish,
                                approxCost = food.approxCostForTwo,
                                reelUrl = food.reelUrl,
                                reelThumbnailUrl = food.reelThumbnailUrl,
                                reelCaption = food.reelCaption,
                                reelViews = food.reelViews,
                                mapLink = "https://maps.google.com/?q=${food.name}+${trip.name}",
                                latitude = 0.0,
                                longitude = 0.0,
                                bestTimeToVisit = "Meal Time",
                                creatorTip = "Must Order: ${food.mustTryDish}",
                                dayNumber = day.dayNumber,
                                orderIndex = orderCounter++
                            )
                        )
                    }
                }

                itineraryDao.insertItineraryWithSpots(itineraryEntity, spots)
            }
        }
    }

    fun isWishlisted(tripId: String): Flow<Boolean> = tripDao.isWishlisted(tripId)

    suspend fun toggleWishlist(trip: Trip, isCurrentlyWishlisted: Boolean) {
        if (isCurrentlyWishlisted) {
            tripDao.deleteWishlistById(trip.id)
        } else {
            tripDao.insertWishlist(
                WishlistEntity(
                    tripId = trip.id,
                    name = trip.name,
                    duration = trip.duration,
                    price = trip.price,
                    imageUrl = trip.imageUrl,
                    vibe = trip.vibe.label
                )
            )
        }
    }

    suspend fun setActiveTrip(tripId: String, squad: String = "2 of us", date: String = "") {
        val trip = getTripById(tripId) ?: return
        val defaultPacking = listOf(
            PackingItemEntity(tripId = tripId, itemTitle = "Valid ID & Booking confirmation", category = "Essentials"),
            PackingItemEntity(tripId = tripId, itemTitle = "Power bank (min 10,000 mAh)", category = "Tech"),
            PackingItemEntity(tripId = tripId, itemTitle = "Comfortable walking / trek shoes", category = "Apparel"),
            PackingItemEntity(tripId = tripId, itemTitle = "Sunscreen SPF 50+ & Sunglasses", category = "Care"),
            PackingItemEntity(tripId = tripId, itemTitle = "Quick-dry towel & Swimwear", category = "Apparel"),
            PackingItemEntity(tripId = tripId, itemTitle = "Offline downloaded map & playlist", category = "Tech")
        )
        tripDao.saveActiveTrip(
            ActiveTripEntity(
                tripId = tripId,
                currentDayIndex = 0,
                completedStopIdsJson = "[]",
                travelDate = date,
                squadSize = squad
            )
        )
        tripDao.insertPackingItems(defaultPacking)
    }

    suspend fun updateActiveTripDay(dayIndex: Int) {
        tripDao.getActiveTrip()
    }

    suspend fun saveActiveTripEntity(entity: ActiveTripEntity) {
        tripDao.saveActiveTrip(entity)
    }

    suspend fun clearActiveTrip() {
        tripDao.clearActiveTrip()
    }

    fun getPackingItems(tripId: String): Flow<List<PackingItemEntity>> = tripDao.getPackingItems(tripId)

    suspend fun togglePackingItem(item: PackingItemEntity) {
        tripDao.updatePackingItem(item.copy(isChecked = !item.isChecked))
    }

    suspend fun addPackingItem(tripId: String, title: String, category: String = "Personal") {
        tripDao.insertPackingItem(
            PackingItemEntity(
                tripId = tripId,
                itemTitle = title,
                category = category,
                isChecked = false
            )
        )
    }

    suspend fun deletePackingItem(item: PackingItemEntity) {
        tripDao.deletePackingItem(item)
    }

    fun getAllTrips(): List<Trip> = CURATED_TRIPS

    fun getTripById(id: String): Trip? = CURATED_TRIPS.find { it.id.equals(id, ignoreCase = true) }

    fun getDestinationSpotlights(): List<DestinationSpotlight> = SPOTLIGHTS

    fun getVideoProofs(): List<VideoProof> = VIDEOS

    fun getInstagramPosts(channel: ChannelType? = null): List<InstagramPost> {
        return if (channel == null) INSTAGRAM_POSTS else INSTAGRAM_POSTS.filter { it.channelType == channel }
    }

    fun getTravelerReviews(): List<TravelerReview> = REVIEWS

    fun matchTrips(destinationId: String?, maxBudget: Int?, vibe: TripVibe?): List<Trip> {
        return CURATED_TRIPS.filter { trip ->
            val matchDest = destinationId.isNullOrBlank() || trip.id.equals(destinationId, ignoreCase = true)
            val matchBudget = maxBudget == null || trip.budgetValue <= maxBudget
            val matchVibe = vibe == null || trip.vibe == vibe
            matchDest && matchBudget && matchVibe
        }
    }

    fun getSmartMatchRecommendation(destinationId: String?, maxBudget: Int?): Pair<String, String>? {
        if (destinationId.isNullOrBlank()) return null
        return when (destinationId.lowercase()) {
            "goa" -> {
                if (maxBudget != null && maxBudget <= 5000) {
                    "Goa Long Weekend — ₹4,999/person" to "3 nights North Goa. Budget beach shacks, scooty crawl, sunset at Curlies & Anjuna."
                } else {
                    "Full Goa Circuit — ₹8,999/person" to "4 nights, North + South Goa blend. Thalassa sunset, Chapora cliff views, and pristine Palolem silence."
                }
            }
            "thailand" -> {
                if (maxBudget != null && maxBudget <= 15000) {
                    "Bangkok Budget Run — ₹12,999" to "7 nights, street food crawl, Wat Arun at sunrise, and hidden market alleys."
                } else if (maxBudget != null && maxBudget <= 30000) {
                    "Bangkok + Krabi Islands — ₹24,999" to "Best of both worlds: neon Bangkok nights & limestone cliff kayaking in Krabi."
                } else {
                    "Full Thailand Circuit — ₹34,999" to "Bangkok + Krabi + Phi Phi. 7 days with domestic transfers included."
                }
            }
            "himachal" -> {
                if (maxBudget != null && maxBudget <= 5000) {
                    "Kasol & Kheerganga — ₹4,999" to "Bus from Delhi/Chd, 3 nights riverside homestay, hot springs & mountain café trail."
                } else {
                    "Manali + Spiti Edge — ₹12,999" to "6 nights. Old Manali base, trout fishing, Solang Valley, and high-altitude Buddhist passes."
                }
            }
            "pondicherry" -> "Pondi French Coast — ₹4,999" to "3 nights. White Town heritage cycle walks, Auroville bakeries, and Serenity Beach sunrise."
            "malaysia" -> "KL + Penang Food Trail — ₹24,999" to "5 nights. Petronas night skyline to George Town street food legacy in 4 hours."
            "krabi" -> "Krabi Secret Lagoons — ₹28,999" to "5 nights. Railay Beach, 4-Islands longtail cruise, and emerald cave swimming."
            "phuket" -> "Phuket & Maya Bay — ₹26,999" to "5 nights. Sino-Portuguese Old Town, hidden Kata Noi cove, and Phi Phi archipelago."
            "mumbai" -> "Maximum Mumbai Experience — ₹6,499" to "3 nights. South Bombay heritage walk, Bandra café crawl, and Marine Drive 2 AM conversations."
            "srilanka" -> "Sri Lanka Island Odyssey — ₹29,999" to "6 nights. Colombo street food, Sigiriya fortress, Ella scenic train, and Mirissa surf."
            "gokarna" -> "Gokarna Slow Escape — ₹4,499" to "3 nights. Om Beach cliff trail, Half Moon cove trek, and beach campfire acoustic nights."
            else -> "Curated Creator Trip" to "Handpicked route verified with 800GB of video proof. No tourist traps."
        }
    }

    companion object {
        private val CURATED_TRIPS = listOf(
            Trip(
                id = "goa",
                name = "Goa",
                headline = "Beach days, cliffside sundowners, zero tourist traps.",
                description = "Forget the crowded commercial packages. We hit the real North Goa secret spots, cliff viewpoints, legendary bakeries, and wind down with tranquil South Goa kayaking.",
                vibe = TripVibe.PARTY,
                duration = "4D / 3N",
                price = "₹8,999",
                budgetValue = 8999,
                imageUrl = "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800&q=80",
                heroTags = listOf("Sunset Views", "Secret Shacks", "Scooter Crawl", "South Coast Kayak"),
                totalEstimateDetails = "₹8,999 / person (Stays, scooty rental, boat kayak & curated entry)",
                creatorNote = "Goa is only as good as the spots you know. Skip the generic Calangute madness. Follow this day-by-day map.",
                youtubeVideoId = "Cometripwithme",
                days = listOf(
                    DayPlan(
                        dayNumber = 1,
                        title = "North Goa Landing & Sundowner",
                        summary = "Land, pick up rented scooters, check into beachside villa, and catch golden hour at Anjuna cliff.",
                        stops = listOf(
                            StopLocation(
                                id = "goa_d1_s1",
                                name = "Anjuna Cliff & Curlies Trail",
                                timing = "4:30 PM",
                                category = "Sunset Viewpoint",
                                description = "Rocky beach edge where psychedelic Goa culture began. Great music and raw ocean energy.",
                                insiderTip = "Arrive 45 mins before sunset to grab the top deck corner table facing the rocks.",
                                photoUrl = "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600&q=80",
                                lat = 15.5804,
                                lng = 73.7431,
                                audioStory = AudioStory(
                                    title = "The True Story of Anjuna & The 70s Hippie Trail",
                                    durationSeconds = 110,
                                    scriptText = "You're standing on the iconic red laterite cliffs of Anjuna. In the late 1960s, world travelers arrived here on old Enfield motorcycles from Europe. Notice the volcanic rocks below. When the tide hits them right around 5:30 PM, the sea spray catches the sunset in brilliant gold."
                                )
                            ),
                            StopLocation(
                                id = "goa_d1_s2",
                                name = "Anjuna Night Flea Market",
                                timing = "8:00 PM",
                                category = "Night Market",
                                description = "Handmade leather, live acoustic bands, Goan sausages, and chilled draught beer.",
                                insiderTip = "Bargain with a smile. The spice stalls at the back have authentic homemade peri-peri masala.",
                                photoUrl = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80",
                                lat = 15.5780,
                                lng = 73.7410
                            )
                        ),
                        foodSpots = listOf(
                            FoodSpot(
                                name = "Curlies Shack",
                                specialty = "Woodfired pizza & Kingfish Rava fry",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Crispy Kingfish Rava Fry with lemon butter",
                                approxCostForTwo = "₹800 for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Crispy Kingfish Rava fry right by Anjuna rocks 🌊",
                                reelViews = "54K views 🎥"
                            ),
                            FoodSpot(
                                name = "Infantaria Pastry",
                                specialty = "Authentic Goan breakfast & bebinca",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Goan Sausage Poee & Bebinca",
                                approxCostForTwo = "₹450 for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Flaky Goan Poee & fresh Bebinca morning crawl 🥐",
                                reelViews = "38K views 🎥"
                            )
                        ),
                        creatorSecretTip = "Rent your scooter right outside the airport or Thivim station — never through hotel front desks who charge 2x markup."
                    ),
                    DayPlan(
                        dayNumber = 2,
                        title = "North Goa Deep Dive & Fort Viewpoints",
                        summary = "Sunrise walk at Chapora, breakfast at a French bakery, and sunset cliff vibes at Vagator.",
                        stops = listOf(
                            StopLocation(
                                id = "goa_d2_s1",
                                name = "Chapora Fort Vista",
                                timing = "8:00 AM",
                                category = "Heritage Fort",
                                description = "The famous Dil Chahta Hai rampart overlooking the Chapora River meeting the Arabian Sea.",
                                insiderTip = "Climb the northern bastion wall for an unobstructed view of Morjim sandbar.",
                                photoUrl = "https://images.unsplash.com/photo-1596178060671-7a80dc8059ea?w=600&q=80",
                                lat = 15.6059,
                                lng = 73.7380,
                                audioStory = AudioStory(
                                    title = "Chapora Fort: Portuguese Cannons & Bollywood Lore",
                                    durationSeconds = 125,
                                    scriptText = "Built in 1717 by the Portuguese over older Adil Shahi ruins, Chapora was designed to defend against Maratha raids. Look out across the river mouth toward Morjim — that sand spit is where endangered Olive Ridley turtles nest in winter."
                                )
                            ),
                            StopLocation(
                                id = "goa_d2_s2",
                                name = "Little Vagator Hidden Cove",
                                timing = "3:30 PM",
                                category = "Secret Beach",
                                description = "Carved rock faces, Shiva face rock carving, and dramatic red cliffs.",
                                insiderTip = "Walk past the main entrance stairs toward the southern cliff path to skip the crowd.",
                                photoUrl = "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600&q=80",
                                lat = 15.5980,
                                lng = 73.7390
                            )
                        ),
                        foodSpots = listOf(
                            FoodSpot(
                                name = "Thalassa Greek Taverna",
                                specialty = "Greek cuisine & sunset cocktail",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Souvlaki wraps & Baklava",
                                approxCostForTwo = "₹1,800 for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1544025162-d76694265947?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Sunset dining vibes & souvlaki platter at Thalassa 🌅",
                                reelViews = "82K views 🎥"
                            ),
                            FoodSpot(
                                name = "Mango Tree Bar",
                                specialty = "Late-night Goan curry & cold beer",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Prawns Balchão with Steamed Rice",
                                approxCostForTwo = "₹700 for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Spicy Goan Prawn Balchão served with steaming rice 🦐",
                                reelViews = "29K views 🎥"
                            )
                        ),
                        creatorSecretTip = "Book Thalassa sunset table at least 3 days in advance via their Instagram DM or WhatsApp."
                    ),
                    DayPlan(
                        dayNumber = 3,
                        title = "South Goa Tranquil Switch & Kayaking",
                        summary = "Drive down through old Portuguese village lanes to Palolem's crescent bay and secret butterfly cove.",
                        stops = listOf(
                            StopLocation(
                                id = "goa_d3_s1",
                                name = "Palolem Crescent Beach",
                                timing = "11:00 AM",
                                category = "Calm Beach",
                                description = "Gentle bay framed by lush coconut groves, colorful wooden shacks, and dolphins.",
                                insiderTip = "Rent a single kayak for ₹300/hr and paddle around Canacona Island on the north end.",
                                photoUrl = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80",
                                lat = 15.0100,
                                lng = 74.0231,
                                audioStory = AudioStory(
                                    title = "Palolem: The Secret Dolphin Sanctuary",
                                    durationSeconds = 95,
                                    scriptText = "Notice how calm the water is here compared to North Goa? Palolem is a natural amphitheater of granite headlands. If you kayak out 300 meters early morning, Indo-Pacific humpback dolphins frequently surface right next to your boat."
                                )
                            ),
                            StopLocation(
                                id = "goa_d3_s2",
                                name = "Butterfly Beach Sunset Boat",
                                timing = "4:45 PM",
                                category = "Hidden Lagoon",
                                description = "Secluded cove surrounded by dense jungle, only reachable by boat or jungle trek.",
                                insiderTip = "Take the 15-minute boat from Palolem right around 4:30 PM to catch sunset without getting stranded after dark.",
                                photoUrl = "https://images.unsplash.com/photo-1528181304800-259b08848526?w=600&q=80",
                                lat = 15.0250,
                                lng = 74.0090
                            )
                        ),
                        foodSpots = listOf(
                            FoodSpot(
                                name = "Dropadi Beach Restaurant",
                                specialty = "Fresh catch of the day on Palolem beach",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Butter Garlic Squid & Coconut Rice",
                                approxCostForTwo = "₹950 for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Butter Garlic Squid cooked fresh on Palolem sands 🦑",
                                reelViews = "44K views 🎥"
                            ),
                            FoodSpot(
                                name = "Ourem 88",
                                specialty = "Hidden garden bistro in Palolem village",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Slow-roasted pork belly & artisanal cheese",
                                approxCostForTwo = "₹1,200 for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Artisanal cheese boards & slow pork belly in South Goa 🧀",
                                reelViews = "31K views 🎥"
                            )
                        ),
                        creatorSecretTip = "Ask the fishermen at Palolem south end for a shared boat ride to Butterfly Beach — it's ₹400 per person instead of ₹1800 private."
                    ),
                    DayPlan(
                        dayNumber = 4,
                        title = "Arambol Morning & Flight Out",
                        summary = "Fresh ocean swim, sweet lake drum circle memories, artisan bakery breakfast, and return flight.",
                        stops = listOf(
                            StopLocation(
                                id = "goa_d4_s1",
                                name = "Arambol Sweet Water Lake",
                                timing = "7:30 AM",
                                category = "Freshwater Lagoon",
                                description = "Natural freshwater lagoon sitting 50 meters away from the crashing ocean waves.",
                                insiderTip = "Dip in the lake first, then walk up the jungle path to see the ancient Banyan tree.",
                                photoUrl = "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?w=600&q=80",
                                lat = 15.6880,
                                lng = 73.7020
                            )
                        ),
                        foodSpots = listOf(
                            FoodSpot(
                                name = "Baba Au Rhum",
                                specialty = "Acclaimed wood-fired French bakery",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Ham & Cheese Croissant + Filter Coffee",
                                approxCostForTwo = "₹650 for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Croissants and woodfired sourdough breakfast reel 🥐",
                                reelViews = "61K views 🎥"
                            ),
                            FoodSpot(
                                name = "The Black Sheep Bistro",
                                specialty = "Modern Goan farm-to-table cuisine",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Crab Xec Xec tacos",
                                approxCostForTwo = "₹1,400 for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1550547660-d9450f859349?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Modern Goan Crab Xec Xec tacos in Panjim 🌮",
                                reelViews = "47K views 🎥"
                            )
                        ),
                        creatorSecretTip = "Pick up Goan cashew feni and spiced choriz sausages from Mapusa Market on the way to the airport."
                    )
                )
            ),
            Trip(
                id = "thailand",
                name = "Thailand",
                headline = "Street food at midnight. Emerald islands at sunrise.",
                description = "7 days across electric Bangkok street food alleyways and the dramatic limestone sea cliffs of Krabi. We bypass overpriced tours and show you the exact local ferries and food carts.",
                vibe = TripVibe.BACKPACKING,
                duration = "7D / 6N",
                price = "₹34,999",
                budgetValue = 34999,
                imageUrl = "https://images.unsplash.com/photo-1528181304800-259b08848526?w=800&q=80",
                heroTags = listOf("Bangkok Street Food", "Wat Arun Sunrise", "Phi Phi Islands", "Krabi Cliffs"),
                totalEstimateDetails = "₹34,999 / person (Hostels/Boutique stays, domestic flights, ferries & food crawl)",
                creatorNote = "Thailand is ruined by bad itineraries. Our route ensures you eat like a Bangkok local and see Maya Bay before the tourist speedboats arrive.",
                youtubeVideoId = "Cometripwithme",
                days = listOf(
                    DayPlan(
                        dayNumber = 1,
                        title = "Bangkok Arrival & Khao San Night Walk",
                        summary = "Land in Suvarnabhumi, take the Airport Rail Link, eat spicy holy basil chicken, and explore old city alleyways.",
                        stops = listOf(
                            StopLocation(
                                id = "th_d1_s1",
                                name = "Khao San & Rambuttri Road",
                                timing = "8:00 PM",
                                category = "Backpacker Hub",
                                description = "The heartbeat of Southeast Asian backpacking, street artists, and fried noodle stalls.",
                                insiderTip = "Skip noisy Khao San main street; walk one block north to Soi Rambuttri for better vibes.",
                                photoUrl = "https://images.unsplash.com/photo-1528181304800-259b08848526?w=600&q=80",
                                lat = 13.7588,
                                lng = 100.4975,
                                audioStory = AudioStory(
                                    title = "Khao San Road: The Accidental Backpacker Capital",
                                    durationSeconds = 105,
                                    scriptText = "Until 1982, Khao San was just a quiet rice market street in Bangkok. When Thailand celebrated its Bangkok bicentennial, travelers looking for cheap lodging knocked on local family doors here. Today it's the global backpacker rite of passage."
                                )
                            )
                        ),
                        foodSpots = listOf(
                            FoodSpot(
                                name = "Thip Samai Pad Thai",
                                specialty = "World-renowned egg-wrapped Pad Thai",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Superb Pad Thai with fresh prawns & orange juice",
                                approxCostForTwo = "400 THB for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1559847844-5315695dadae?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Watch the legendary egg-wrapped Pad Thai flame wok show 🔥",
                                reelViews = "96K views 🎥"
                            ),
                            FoodSpot(
                                name = "Soi 38 Street Cart",
                                specialty = "Late night Pad Kra Pao stall",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Spicy Minced Pork Pad Kra Pao with crispy fried egg",
                                approxCostForTwo = "120 THB for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1562967914-608f82629710?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Midnight Pad Kra Pao with sizzling crispy duck egg 🍳",
                                reelViews = "73K views 🎥"
                            )
                        ),
                        creatorSecretTip = "Exchange currency at SuperRich counters in Suvarnabhumi Airport basement for the highest rate in Thailand."
                    ),
                    DayPlan(
                        dayNumber = 2,
                        title = "Wat Arun Sunrise & Riverside Markets",
                        summary = "Watch early golden light hit the porcelain spires of Temple of Dawn, take the 5-baht river ferry, and explore Chinatown food stalls.",
                        stops = listOf(
                            StopLocation(
                                id = "th_d2_s1",
                                name = "Wat Arun (Temple of Dawn)",
                                timing = "7:30 AM",
                                category = "Ancient Temple",
                                description = "Majestic spire covered in thousands of colorful glazed Chinese porcelain mosaics along Chao Phraya.",
                                insiderTip = "Rent traditional Thai attire at the temple gate for ₹200 for iconic photography.",
                                photoUrl = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80",
                                lat = 13.7437,
                                lng = 100.4889,
                                audioStory = AudioStory(
                                    title = "Wat Arun: The Porcelain Temple by the River of Kings",
                                    durationSeconds = 120,
                                    scriptText = "Wat Arun stands 82 meters high on the west bank of the Chao Phraya River. Notice the porcelain tiles? In the 18th century, Chinese merchant ships used broken porcelain plates as ballast weights to balance their ships — King Rama III used those discarded plates to decorate this entire temple."
                                )
                            ),
                            StopLocation(
                                id = "th_d2_s2",
                                name = "Yaowarat Chinatown Food Mile",
                                timing = "7:00 PM",
                                category = "Food Market",
                                description = "Neon signs, sizzling woks, crab fried rice, and mango sticky rice carts.",
                                insiderTip = "Look for the green Michelin Bib Gourmand plaques on humble cart wheels.",
                                photoUrl = "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?w=600&q=80",
                                lat = 13.7408,
                                lng = 100.5108
                            )
                        ),
                        foodSpots = listOf(
                            FoodSpot(
                                name = "Guay Tiew Kua Gai",
                                specialty = "Michelin rated wok-fried chicken flat noodles",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Smoky roasted chicken rice noodles with soft egg",
                                approxCostForTwo = "150 THB for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Michelin Bib Gourmand smoky wok flat noodles 🥢",
                                reelViews = "88K views 🎥"
                            ),
                            FoodSpot(
                                name = "Nai Ek Roll Noodle",
                                specialty = "Crispy pork belly in peppery broth",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Crispy pork belly soup",
                                approxCostForTwo = "180 THB for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Ultra crispy pork belly roll soup in Chinatown Yaowarat 🍜",
                                reelViews = "105K views 🎥"
                            )
                        ),
                        creatorSecretTip = "Use the Chao Phraya Express Orange Flag boat for 16 THB to travel anywhere along the river instead of tourist boats."
                    ),
                    DayPlan(
                        dayNumber = 3,
                        title = "Fly to Krabi & Railay Beach Sunset",
                        summary = "Morning 1-hour flight to Krabi, check into beach hotel, longtail boat to Railay surrounded by limestone towers.",
                        stops = listOf(
                            StopLocation(
                                id = "th_d3_s1",
                                name = "Railay Beach & Phra Nang Cave",
                                timing = "3:30 PM",
                                category = "Limestone Peninsula",
                                description = "Cut off from the mainland by gigantic karst cliffs, accessible exclusively by wooden longtail boat.",
                                insiderTip = "Walk from Railay West to Railay East at low tide to watch rock climbers scale 150m vertical cliffs.",
                                photoUrl = "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600&q=80",
                                lat = 8.0119,
                                lng = 98.8396,
                                audioStory = AudioStory(
                                    title = "Railay: The Fortress Cut Off by Ancient Cliffs",
                                    durationSeconds = 110,
                                    scriptText = "Because towering limestone headlands block all roads from the mainland, Railay has zero cars and zero scooters. You arrive by splashing into the turquoise surf from a wooden longtail boat. It feels like entering an untouched island paradise."
                                )
                            )
                        ),
                        foodSpots = listOf(
                            FoodSpot(
                                name = "Krabi Town Night Market",
                                specialty = "Southern Thai curries & roti stalls",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Banana Nutella Roti + Green Curry",
                                approxCostForTwo = "300 THB for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Hot Banana Nutella Roti cooked live in Krabi 🥞",
                                reelViews = "52K views 🎥"
                            )
                        ),
                        creatorSecretTip = "Book longtail boat tickets directly at the Ao Nang cooperative booth at the beach head for fixed standard rates."
                    ),
                    DayPlan(
                        dayNumber = 4,
                        title = "Early Bird Phi Phi & Maya Bay Run",
                        summary = "6:30 AM speedboat to Maya Bay before the 10:00 AM tourist crowds arrive from Phuket.",
                        stops = listOf(
                            StopLocation(
                                id = "th_d4_s1",
                                name = "Maya Bay & Pileh Lagoon",
                                timing = "7:45 AM",
                                category = "World Heritage Bay",
                                description = "Dramatic 100-meter cliffs enclosing crystalline emerald water and blacktip reef sharks.",
                                insiderTip = "Swim inside Pileh Lagoon where the water is calm like a heated swimming pool.",
                                photoUrl = "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?w=600&q=80",
                                lat = 7.6784,
                                lng = 98.7672
                            )
                        ),
                        foodSpots = listOf(
                            FoodSpot(
                                name = "Island Boat Fresh Catch",
                                specialty = "Barbecue seafood cooked fresh on longtail boat",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Grilled Tiger Prawns & Papaya Salad",
                                approxCostForTwo = "500 THB for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1544025162-d76694265947?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Freshly grilled tiger prawns right on the island beach 🦐",
                                reelViews = "68K views 🎥"
                            )
                        ),
                        creatorSecretTip = "Take an early 6:30 AM departure. You'll have Maya Bay almost entirely to yourself for pristine photos."
                    ),
                    DayPlan(
                        dayNumber = 5,
                        title = "Slow Day & Emerald Pool Kayaking",
                        summary = "Relaxed morning, kayak through Bor Thor mangrove river caves, and fresh coconut water on the beach.",
                        stops = listOf(
                            StopLocation(
                                id = "th_d5_s1",
                                name = "Bor Thor Mangrove Caves",
                                timing = "10:30 AM",
                                category = "Nature Reserve",
                                description = "Paddling under massive stalactites with 3,000-year-old prehistoric cave paintings.",
                                insiderTip = "Rent a double kayak and guide to enter the skull cave at high tide.",
                                photoUrl = "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600&q=80",
                                lat = 8.4200,
                                lng = 98.7100
                            )
                        ),
                        foodSpots = listOf(
                            FoodSpot(
                                name = "Mama's Krabi Seafood",
                                specialty = "Local family-run shack overlooking the ocean",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Tom Yum Goong & Crab Fried Rice",
                                approxCostForTwo = "600 THB for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1535400255456-984241443b29?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Spicy Tom Yum Goong soup by the ocean 🍲",
                                reelViews = "41K views 🎥"
                            )
                        ),
                        creatorSecretTip = "Buy waterproof dry bags in Ao Nang for 150 THB before heading out to the caves."
                    ),
                    DayPlan(
                        dayNumber = 6,
                        title = "Return to Bangkok & Sky Bar Sunset",
                        summary = "Afternoon flight back to Bangkok, rooftop sunset cocktail at Vertigo Bar, and Chatuchak shopping.",
                        stops = listOf(
                            StopLocation(
                                id = "th_d6_s1",
                                name = "Vertigo & Moon Bar",
                                timing = "5:45 PM",
                                category = "Rooftop Lounge",
                                description = "Open-air 61st floor panorama of the glowing Bangkok metropolis.",
                                insiderTip = "Dress smart-casual; flip flops and tank tops are not permitted on the 61st floor.",
                                photoUrl = "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&q=80",
                                lat = 13.7237,
                                lng = 100.5398
                            )
                        ),
                        foodSpots = listOf(
                            FoodSpot(
                                name = "Chatuchak Weekend Market Stalls",
                                specialty = "Giant market food lane",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Coconut Ice cream served in real coconut husk",
                                approxCostForTwo = "100 THB for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1501443762994-82bd5dace89a?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Coconut ice cream with roasted peanuts & sticky rice 🥥",
                                reelViews = "77K views 🎥"
                            )
                        ),
                        creatorSecretTip = "The BTS Skytrain is your best friend in evening Bangkok traffic. Download the Rabbit card app."
                    ),
                    DayPlan(
                        dayNumber = 7,
                        title = "Suvarnabhumi Departure & Final Feast",
                        summary = "Last morning stroll, suitcase packed with Thai snacks, and smooth airport rail transit.",
                        stops = listOf(
                            StopLocation(
                                id = "th_d7_s1",
                                name = "Bangkok Suvarnabhumi Airport",
                                timing = "12:00 PM",
                                category = "Departure",
                                description = "Final duty-free shopping and mango sticky rice treat before the flight back home.",
                                insiderTip = "The Magic Food Point food court on Level 1 has airport workers' street food prices.",
                                photoUrl = "https://images.unsplash.com/photo-1528181304800-259b08848526?w=600&q=80",
                                lat = 13.6900,
                                lng = 100.7501
                            )
                        ),
                        foodSpots = listOf(
                            FoodSpot(
                                name = "Magic Food Court Level 1",
                                specialty = "Affordable authentic airport meals",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Crispy Duck Noodle Soup",
                                approxCostForTwo = "140 THB for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Airport staff secret food court duck noodles 🦆",
                                reelViews = "35K views 🎥"
                            )
                        ),
                        creatorSecretTip = "Keep 500 THB cash for departure-day snacks and airport rail tokens."
                    )
                )
            ),
            Trip(
                id = "himachal",
                name = "Himachal Pradesh",
                headline = "The mountains will fix whatever is broken in you.",
                description = "Riverside Kasol cafés, Kheerganga hot springs trek, Solang snow peaks, and serene pine forest walks. Authentic homestays and zero commercial tourist jams.",
                vibe = TripVibe.CHILL,
                duration = "6D / 5N",
                price = "₹12,999",
                budgetValue = 12999,
                imageUrl = "https://images.unsplash.com/photo-1605649487212-47bdab064df7?w=800&q=80",
                heroTags = listOf("Kheerganga Hot Springs", "Old Manali Cafés", "Beas River Walks", "Mountain Homestays"),
                totalEstimateDetails = "₹12,999 / person (Volvo transit, valley homestays, trek guides & hot meals)",
                creatorNote = "Himachal changes you. The secret is knowing which village to sleep in so you hear the pine needles, not car honks.",
                youtubeVideoId = "Cometripwithme",
                days = listOf(
                    DayPlan(
                        dayNumber = 1,
                        title = "Delhi/Chandigarh Volvo to Kasol",
                        summary = "Scenic overnight bus ascending into the Parvati Valley. Wake up to misty river views and fresh ginger lemon honey tea.",
                        stops = listOf(
                            StopLocation(
                                id = "hp_d1_s1",
                                name = "Parvati River Bank Walk",
                                timing = "9:00 AM",
                                category = "Riverside Nature",
                                description = "Glacial turquoise waters roaring through giant mossy granite boulders and pine woods.",
                                insiderTip = "Cross the suspension bridge toward Chalal village for secluded wooden riverside benches.",
                                photoUrl = "https://images.unsplash.com/photo-1605649487212-47bdab064df7?w=600&q=80",
                                lat = 32.0098,
                                lng = 77.3150,
                                audioStory = AudioStory(
                                    title = "Parvati Valley: The Legend of Shiva's Meditation",
                                    durationSeconds = 100,
                                    scriptText = "According to folklore, Lord Shiva meditated here in this valley for three thousand years. As you listen to the roaring Parvati River, you'll understand why travelers from across the world come here to disconnect."
                                )
                            )
                        ),
                        foodSpots = listOf(
                            FoodSpot(
                                name = "Café 1947",
                                specialty = "Old Manali's oldest Italian riverside café",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Woodfired Quattro Formaggi & Hot Chocolate",
                                approxCostForTwo = "₹850 for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Riverside woodfired pizza listening to roaring Beas river 🍕",
                                reelViews = "59K views 🎥"
                            ),
                            FoodSpot(
                                name = "Dylan's Toasted & Roasted",
                                specialty = "Iconic coffee and cookie corner",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Warm Chocolate Chip Cookie with Espresso",
                                approxCostForTwo = "₹300 for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Old Manali's iconic hot chocolate chip cookie & espresso ☕",
                                reelViews = "43K views 🎥"
                            )
                        ),
                        creatorSecretTip = "Carry cash in Kasol and Parvati valley. ATMs frequently run dry in peak mountain season."
                    ),
                    DayPlan(
                        dayNumber = 2,
                        title = "The Kheerganga Trek & Natural Hot Springs",
                        summary = "12km trek through apple orchards, pine forests, and waterfalls to natural sulfur hot springs under the stars.",
                        stops = listOf(
                            StopLocation(
                                id = "hp_d2_s1",
                                name = "Kheerganga Hot Spring Top",
                                timing = "3:30 PM",
                                category = "Natural Hot Spring",
                                description = "Natural therapeutic hot sulfur pool overlooking snowcapped 4,000m Himalayan ridges.",
                                insiderTip = "Enter the pool right around sunset when the mountain air chills to 8°C — pure magic.",
                                photoUrl = "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&q=80",
                                lat = 31.9890,
                                lng = 77.5020
                            )
                        ),
                        foodSpots = listOf(
                            FoodSpot(
                                name = "Kheerganga Ridge Dhaba",
                                specialty = "Steaming mountain comfort food",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Maggi with Fried Egg & Kashmiri Kahwa",
                                approxCostForTwo = "₹250 for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1612927601601-6638404737ce?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Steaming mountain Maggi and hot Kashmiri Kahwa after 12km trek 🏔️",
                                reelViews = "36K views 🎥"
                            )
                        ),
                        creatorSecretTip = "Start the trek from Barshaini by 8:30 AM to reach the top comfortably before afternoon mist rolls in."
                    )
                )
            ),
            Trip(
                id = "pondicherry",
                name = "Pondicherry",
                headline = "French heritage lanes, Indian soul, ₹400 filter coffee & croissants.",
                description = "Cycle through the mustard-yellow French Quarter at 6:30 AM before tourists wake up. Experience spiritual Auroville, golden beaches, and authentic French bakeries.",
                vibe = TripVibe.CHILL,
                duration = "3D / 2N",
                price = "₹4,999",
                budgetValue = 4999,
                imageUrl = "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=800&q=80",
                heroTags = listOf("White Town French Quarter", "Auroville Matrimandir", "Promenade Sunrise", "Artisanal Bakeries"),
                totalEstimateDetails = "₹4,999 / person (Heritage stay, vintage cycle rental, Auroville entry & café trail)",
                creatorNote = "Pondi is meant to be done slowly. Wake up at 6:00 AM, rent a cycle with a wicker basket, and smell the fresh baguettes.",
                youtubeVideoId = "Cometripwithme",
                days = listOf(
                    DayPlan(
                        dayNumber = 1,
                        title = "White Town Heritage Walk & Promenade",
                        summary = "French Quarter architecture, bougainvillea covered colonial gates, and ocean breeze.",
                        stops = listOf(
                            StopLocation(
                                id = "pon_d1_s1",
                                name = "White Town French Quarter",
                                timing = "6:30 AM",
                                category = "Heritage Architecture",
                                description = "Preserved 18th-century French colonial mansions, arched windows, and cobblestone lanes.",
                                insiderTip = "Rue Suffren and Rue Romain Rolland have the most vibrant yellow colonial façades.",
                                photoUrl = "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=600&q=80",
                                lat = 11.9338,
                                lng = 79.8350,
                                audioStory = AudioStory(
                                    title = "White Town: Where France Met the Coromandel Coast",
                                    durationSeconds = 115,
                                    scriptText = "In 1674, the French East India Company designed this grid city with a canal separating the French Quarter from the Tamil Quarter. As you cycle past these arched doorways, notice how Tamil courtyard architecture blended into French balconies."
                                )
                            )
                        ),
                        foodSpots = listOf(
                            FoodSpot(
                                name = "Baker Street",
                                specialty = "French boulangerie and viennoiseries",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Almond Croissant & Quiche Lorraine",
                                approxCostForTwo = "₹450 for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Flaky Parisian almond croissants in French Quarter 🥐",
                                reelViews = "64K views 🎥"
                            ),
                            FoodSpot(
                                name = "Café des Arts",
                                specialty = "Bohemian courtyard café with vintage books",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Nutella Crêpes & Cold Brew",
                                approxCostForTwo = "₹500 for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Nutella crêpes in a sunny vintage courtyard ☕",
                                reelViews = "49K views 🎥"
                            )
                        ),
                        creatorSecretTip = "Rent a classic bicycle near the railway station for ₹100/day rather than booking expensive e-rickshaws."
                    )
                )
            ),
            Trip(
                id = "malaysia",
                name = "Malaysia",
                headline = "KL skyline to Penang street food legacy in 4 hours.",
                description = "5 days taking you from the gleaming Petronas Towers and Batu Caves to the UNESCO World Heritage street murals and sizzling hawker stalls of George Town.",
                vibe = TripVibe.BACKPACKING,
                duration = "5D / 4N",
                price = "₹24,999",
                budgetValue = 24999,
                imageUrl = "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?w=800&q=80",
                heroTags = listOf("Petronas Towers", "George Town UNESCO", "Jalan Alor Night Market", "Penang Food Trail"),
                totalEstimateDetails = "₹24,999 / person (Boutique hotels, KTM ETS express train, city transfers & food tour)",
                creatorNote = "Penang has the best street food on planet Earth. This trip is designed completely around your palate.",
                youtubeVideoId = "Cometripwithme",
                days = listOf(
                    DayPlan(
                        dayNumber = 1,
                        title = "Kuala Lumpur Neon & Batu Caves",
                        summary = "Climb the 272 rainbow steps at Batu Caves and experience the night glow of Petronas Twin Towers.",
                        stops = listOf(
                            StopLocation(
                                id = "my_d1_s1",
                                name = "Batu Caves Rainbow Steps",
                                timing = "8:00 AM",
                                category = "Limestone Shrine",
                                description = "Gigantic 140-foot golden Lord Murugan statue guarding 400-million-year-old limestone cavern.",
                                insiderTip = "Beware of macaque monkeys; do not carry plastic bags or uncovered snacks on the stairs.",
                                photoUrl = "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?w=600&q=80",
                                lat = 3.2379,
                                lng = 101.6840
                            )
                        ),
                        foodSpots = listOf(
                            FoodSpot(
                                name = "Jalan Alor Night Market",
                                specialty = "Sizzling street food central",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Satay Skewers with peanut sauce & Char Kway Teow",
                                approxCostForTwo = "45 MYR for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Char Kway Teow wok hei & sizzling peanut chicken satay 🍢",
                                reelViews = "77K views 🎥"
                            )
                        ),
                        creatorSecretTip = "Take the KTM ETS high-speed train from KL Sentral to Butterworth (Penang) — comfortable 4-hour scenic ride."
                    )
                )
            ),
            Trip(
                id = "krabi",
                name = "Krabi",
                headline = "The kind of turquoise water that breaks your camera settings.",
                description = "5 days in paradise. Railay peninsula cliffs, 4 Islands longtail cruise, emerald freshwater lagoons, and sunset beach seafood barbecues.",
                vibe = TripVibe.LUXURY,
                duration = "5D / 4N",
                price = "₹28,999",
                budgetValue = 28999,
                imageUrl = "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",
                heroTags = listOf("Railay Beach", "4-Islands Cruise", "Tiger Cave Vista", "Emerald Pool"),
                totalEstimateDetails = "₹28,999 / person (Resort stay, private longtail charter, kayak rentals & meals)",
                creatorNote = "Krabi feels completely different from commercial Phuket. More jungle, higher cliffs, and untouched emerald coves.",
                youtubeVideoId = "Cometripwithme",
                days = listOf(
                    DayPlan(
                        dayNumber = 1,
                        title = "Arrive Krabi & Ao Nang Beach Sunset",
                        summary = "Fly directly into Krabi Airport. Check into oceanfront resort and watch longtail boats silhouetted against the sunset.",
                        stops = listOf(
                            StopLocation(
                                id = "kb_d1_s1",
                                name = "Noppharat Thara Sunset Strip",
                                timing = "5:30 PM",
                                category = "Sunset Beach",
                                description = "Lush pine-fringed coastline with sand flats extending out to offshore islands during low tide.",
                                insiderTip = "Walk across the shallow sand spit to Koh Khao Sam Hak during low tide at 5:00 PM.",
                                photoUrl = "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600&q=80",
                                lat = 8.0410,
                                lng = 98.8100
                            )
                        ),
                        foodSpots = listOf(
                            FoodSpot(
                                name = "The Hilltop Restaurant",
                                specialty = "Panoramic cliff dining over Ao Nang bay",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Steamed Seabass with lime and garlic",
                                approxCostForTwo = "850 THB for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1544025162-d76694265947?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Seabass with fresh lime & garlic overlooking the sunset cliffs 🐟",
                                reelViews = "58K views 🎥"
                            )
                        ),
                        creatorSecretTip = "Fly straight into KBV (Krabi Airport) rather than landing in Phuket and enduring a 3.5 hour road transfer."
                    )
                )
            ),
            Trip(
                id = "gokarna",
                name = "Gokarna",
                headline = "Cliff hikes, hidden crescent coves, and acoustic campfire nights.",
                description = "4 days discovering the raw beauty of coastal Karnataka. The 5-beach cliff trek, Half Moon beach camp, secret lagoons, and oceanfront shacks.",
                vibe = TripVibe.CHILL,
                duration = "4D / 3N",
                price = "₹4,499",
                budgetValue = 4499,
                imageUrl = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",
                heroTags = listOf("5-Beach Cliff Trek", "Om Beach Rock Formations", "Half Moon Seclusion", "Kudle Sunset"),
                totalEstimateDetails = "₹4,499 / person (Beach huts, cliff guide, ferry transfers & fresh seafood)",
                creatorNote = "Gokarna is what Goa was 30 years ago. Pure nature, zero chaos, and breathtaking cliffside paths.",
                youtubeVideoId = "Cometripwithme",
                days = listOf(
                    DayPlan(
                        dayNumber = 1,
                        title = "Kudle Beach & Sunset Drum Circle",
                        summary = "Check into cliff hut above Kudle Beach, fresh coconut water, and sunset over the Arabian Sea.",
                        stops = listOf(
                            StopLocation(
                                id = "gk_d1_s1",
                                name = "Kudle Beach Cliff Path",
                                timing = "4:00 PM",
                                category = "Scenic Cliff",
                                description = "Winding coastal cliff trail connecting Gokarna town to Kudle's sweeping sandy bay.",
                                insiderTip = "Wear proper sneakers for the rocky cliff walk down to the beach.",
                                photoUrl = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80",
                                lat = 14.5300,
                                lng = 74.3160
                            )
                        ),
                        foodSpots = listOf(
                            FoodSpot(
                                name = "Namaste Café Om Beach",
                                specialty = "Iconic seaside terrace eatery",
                                recommendedBy = "@beyondbengalurufoods",
                                mustTryDish = "Nutella Banana Pancake & Iced Lemon Tea",
                                approxCostForTwo = "₹400 for two",
                                reelThumbnailUrl = "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&q=80",
                                reelUrl = "https://www.instagram.com/beyondbengalurufoods/",
                                reelCaption = "Nutella banana pancakes right on the rock ledge of Om Beach 🥞",
                                reelViews = "42K views 🎥"
                            )
                        ),
                        creatorSecretTip = "Start the 5-beach trek (Kudle -> Om -> Half Moon -> Paradise -> God's Own) early at 6:30 AM."
                    )
                )
            )
        )

        private val SPOTLIGHTS = listOf(
            DestinationSpotlight(
                id = "bengaluru",
                title = "Bengaluru & Beyond",
                subtitle = "Urban culture, heritage lanes & secret dosas",
                region = "Karnataka · Urban Culture",
                documentedSpotsCount = "15+ documented spots",
                imageUrl = "https://images.unsplash.com/photo-1596178060671-7a80dc8059ea?w=800&q=80",
                tags = listOf("Food Walks", "Malleswaram Heritage", "Cubbon Park", "Secret Filter Coffee")
            ),
            DestinationSpotlight(
                id = "coorg",
                title = "Coorg & Chikmagalur",
                subtitle = "Coffee estates, misty mountain sunrises & waterfalls",
                region = "Western Ghats · Hill Stations",
                documentedSpotsCount = "12+ verified trails",
                imageUrl = "https://images.unsplash.com/photo-1605649487212-47bdab064df7?w=800&q=80",
                tags = listOf("Coffee Plantations", "Mullayanagiri Peak", "Abbi Falls", "Homestay Dinners")
            ),
            DestinationSpotlight(
                id = "hampi",
                title = "Hampi & Badami Ruins",
                subtitle = "Boulders, Vijayanagara empire & Tungabhadra sunsets",
                region = "Ancient · UNESCO World Heritage",
                documentedSpotsCount = "18+ historical spots",
                imageUrl = "https://images.unsplash.com/photo-1590001155093-a3c66ab0c3ff?w=800&q=80",
                tags = listOf("Virupaksha Temple", "Matanga Hill", "Coracle Boat", "Hippie Island")
            ),
            DestinationSpotlight(
                id = "thailand_spot",
                title = "Thailand & Islands",
                subtitle = "Bangkok street food woks & Krabi emerald lagoons",
                region = "Southeast Asia · Tropical",
                documentedSpotsCount = "24+ verified locations",
                imageUrl = "https://images.unsplash.com/photo-1528181304800-259b08848526?w=800&q=80",
                tags = listOf("Railay Beach", "Wat Arun", "Maya Bay", "Yaowarat Chinatown")
            )
        )

        private val VIDEOS = listOf(
            VideoProof(
                id = "v1",
                title = "ComeTripWithMe: Real Trips, Real Proof (Watch Before You Book)",
                destination = "Bengaluru & Thailand",
                duration = "14:20",
                views = "45K views",
                thumbnailUrl = "https://images.unsplash.com/photo-1528181304800-259b08848526?w=800&q=80",
                videoUrl = "https://youtube.com/@Cometripwithme",
                highlights = listOf("Creator-Led Routes", "No tourist traps", "Real street prices", "Local contacts")
            ),
            VideoProof(
                id = "v2",
                title = "Gokarna: The Secret Beach Nobody Tells You About",
                destination = "Gokarna Coast",
                duration = "9:45",
                views = "32K views",
                thumbnailUrl = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",
                videoUrl = "https://youtube.com/@Cometripwithme",
                highlights = listOf("Half Moon cliff trail", "₹300 boat negotiation", "Hidden natural rock pool")
            ),
            VideoProof(
                id = "v3",
                title = "Bengaluru Food Spots That Are Not On Any Online List",
                destination = "Bengaluru",
                duration = "11:15",
                views = "89K views",
                thumbnailUrl = "https://images.unsplash.com/photo-1596178060671-7a80dc8059ea?w=800&q=80",
                videoUrl = "https://youtube.com/@Cometripwithme",
                highlights = listOf("Old City military hotel", "Crisp benne dosa", "₹20 filter coffee ritual")
            ),
            VideoProof(
                id = "v4",
                title = "Himachal: The Riverside Mountain Café That Changed Everything",
                destination = "Parvati Valley",
                duration = "12:50",
                views = "58K views",
                thumbnailUrl = "https://images.unsplash.com/photo-1605649487212-47bdab064df7?w=800&q=80",
                videoUrl = "https://youtube.com/@Cometripwithme",
                highlights = listOf("Pine forest homestay", "Secret hot springs timing", "Trout fish preparation")
            ),
            VideoProof(
                id = "v5",
                title = "KL to Penang in 4 Hours: The Malaysia Nobody Talks About",
                destination = "Malaysia",
                duration = "16:05",
                views = "27K views",
                thumbnailUrl = "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?w=800&q=80",
                videoUrl = "https://youtube.com/@Cometripwithme",
                highlights = listOf("KTM train hack", "George Town Asam Laksa", "Murals without crowd")
            )
        )

        private val INSTAGRAM_POSTS = listOf(
            InstagramPost(
                id = "ig1",
                handle = "@cometriipwme",
                channelType = ChannelType.TRAVEL,
                caption = "The exact moment the morning sun broke over Chapora Fort. 0 tourists, 100% ocean breeze. 📍 Goa",
                location = "Chapora Fort, North Goa",
                imageUrl = "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600&q=80",
                likesCount = "1,840"
            ),
            InstagramPost(
                id = "ig2",
                handle = "@cometriipwme",
                channelType = ChannelType.TRAVEL,
                caption = "Phra Nang Cave beach right before the longtails arrived. Water clarity was unreal today. 🏝️",
                location = "Railay Peninsula, Krabi",
                imageUrl = "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600&q=80",
                likesCount = "2,410"
            ),
            InstagramPost(
                id = "ig3",
                handle = "@beyondbengalurufoods",
                channelType = ChannelType.FOOD,
                caption = "Piping hot butter garlic kingfish rava fry right by the shore. The crunch is everything. 🍜",
                location = "Anjuna Beach, Goa",
                imageUrl = "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600&q=80",
                likesCount = "3,120"
            ),
            InstagramPost(
                id = "ig4",
                handle = "@beyondbengalurufoods",
                channelType = ChannelType.FOOD,
                caption = "Pad Kra Pao with duck egg cooked on a 40-year-old roaring wok in Bangkok Chinatown. 🔥",
                location = "Yaowarat, Bangkok",
                imageUrl = "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=600&q=80",
                likesCount = "4,200"
            ),
            InstagramPost(
                id = "ig5",
                handle = "@cometriipwme",
                channelType = ChannelType.TRAVEL,
                caption = "Hiking the five beaches of Gokarna. Why pay ₹50,000 when this paradise is right in Karnataka? 🌊",
                location = "Om Beach, Gokarna",
                imageUrl = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80",
                likesCount = "1,980"
            ),
            InstagramPost(
                id = "ig6",
                handle = "@beyondbengalurufoods",
                channelType = ChannelType.FOOD,
                caption = "The most comforting ginger lemon honey tea with apple strudel in Old Manali. ☕🏔️",
                location = "Old Manali, Himachal",
                imageUrl = "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&q=80",
                likesCount = "2,750"
            )
        )

        private val REVIEWS = listOf(
            TravelerReview(
                id = "r1",
                authorHandle = "@rohini.explores",
                city = "Bengaluru",
                tripTag = "🌆 Old City Food Walk",
                rating = 5,
                reviewQuote = "Tried three different tour operators in Bengaluru. This was the only one that felt like an actual secret. The chai and military hotel spot alone was worth every rupee."
            ),
            TravelerReview(
                id = "r2",
                authorHandle = "@arjun_wanders",
                city = "Chennai",
                tripTag = "☁️ Coorg & Chikmagalur Weekend",
                rating = 5,
                reviewQuote = "Watched the YouTube video, booked the trip, went. Every single stop matched the video proof. Felt like being inside a vlog in real life. That doesn't happen with agency brochures."
            ),
            TravelerReview(
                id = "r3",
                authorHandle = "@priya.irl",
                city = "Hyderabad",
                tripTag = "🏔️ Himachal Mountain Trail",
                rating = 5,
                reviewQuote = "Finally a tour operator who communicates over WhatsApp like a normal human friend. Mullayanagiri and Kheerganga hit different. No PDF itinerary = 10/10."
            )
        )
    }
}
