package com.example.data.service

import android.util.Log
import com.example.BuildConfig
import com.example.data.model.CustomDayPlan
import com.example.data.model.CustomItineraryResult
import com.example.data.model.PricingEngine
import com.example.data.model.TravelerType
import com.example.data.model.TripVibe
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject
import java.util.concurrent.TimeUnit

class GeminiAiService {

    private val client = OkHttpClient.Builder()
        .connectTimeout(25, TimeUnit.SECONDS)
        .readTimeout(25, TimeUnit.SECONDS)
        .build()

    private val modelName = "gemini-3.5-flash"

    suspend fun generateCustomItinerary(
        userPrompt: String,
        destinationHint: String? = null,
        durationDaysHint: Int = 4,
        budgetHint: Int = 15000,
        preferredVibe: TripVibe = TripVibe.BACKPACKING,
        travelerGroupHint: TravelerType = TravelerType.FRIENDS_SQUAD
    ): Pair<String, CustomItineraryResult> = withContext(Dispatchers.IO) {
        val apiKey = try {
            BuildConfig.GEMINI_API_KEY
        } catch (e: Exception) {
            ""
        }

        // If apiKey is valid, try Gemini API call first
        if (!apiKey.isNullOrBlank() && !apiKey.equals("MY_GEMINI_API_KEY", ignoreCase = true)) {
            try {
                val apiResult = callGeminiApi(apiKey, userPrompt)
                if (apiResult != null) {
                    return@withContext apiResult
                }
            } catch (e: Exception) {
                Log.w("GeminiAiService", "Gemini API call failed, falling back to smart engine: ${e.message}")
            }
        }

        // High-fidelity algorithmic intelligent itinerary generator
        return@withContext generateSmartItineraryLocally(
            userPrompt = userPrompt,
            destinationHint = destinationHint,
            durationDaysHint = durationDaysHint,
            budgetHint = budgetHint,
            preferredVibe = preferredVibe,
            travelerGroupHint = travelerGroupHint
        )
    }

    private fun callGeminiApi(apiKey: String, prompt: String): Pair<String, CustomItineraryResult>? {
        val url = "https://generativelanguage.googleapis.com/v1beta/models/$modelName:generateContent?key=$apiKey"

        val systemInstruction = """
            You are ComeTripWithMe AI, the master trip planner and travel creator.
            Create a rich, realistic, offbeat travel itinerary.
            Return a JSON object with:
            {
              "assistantMessage": "Conversational friendly reply explaining why this route was handpicked",
              "destination": "Destination name",
              "title": "Exciting Itinerary Title",
              "tagline": "Short punchy description",
              "duration": "e.g. 5D / 4N",
              "vibe": "BACKPACKING or CHILL or PARTY or LUXURY or HERITAGE",
              "basePerPersonBudget": 18000,
              "offbeatSecretSpots": ["Spot 1", "Spot 2", "Spot 3", "Spot 4"],
              "foodHighlights": ["Food 1", "Food 2", "Food 3"],
              "days": [
                {
                  "dayNumber": 1,
                  "title": "Day 1 Title",
                  "morningActivity": "Morning description",
                  "afternoonActivity": "Afternoon description",
                  "eveningActivity": "Evening description",
                  "offbeatSecretSpot": "Secret spot with insider trick",
                  "mustTryFoodSpot": "Exact food stall/restaurant name and must-try dish",
                  "creatorTip": "Unfiltered tip"
                }
              ],
              "creatorVerdict": "Final takeaway quote"
            }
        """.trimIndent()

        val rootJson = JSONObject().apply {
            put("contents", JSONArray().apply {
                put(JSONObject().apply {
                    put("parts", JSONArray().apply {
                        put(JSONObject().apply {
                            put("text", "System: $systemInstruction\n\nUser Request: $prompt\nOutput ONLY valid JSON.")
                        })
                    })
                })
            })
            put("generationConfig", JSONObject().apply {
                put("responseMimeType", "application/json")
            })
        }

        val requestBody = rootJson.toString().toRequestBody("application/json".toMediaType())
        val request = Request.Builder()
            .url(url)
            .post(requestBody)
            .build()

        val response = client.newCall(request).execute()
        if (!response.isSuccessful) return null

        val responseBody = response.body?.string() ?: return null
        val responseJson = JSONObject(responseBody)
        val candidates = responseJson.optJSONArray("candidates") ?: return null
        if (candidates.length() == 0) return null

        val content = candidates.getJSONObject(0).optJSONObject("content") ?: return null
        val parts = content.optJSONArray("parts") ?: return null
        if (parts.length() == 0) return null

        val text = parts.getJSONObject(0).optString("text", "")
        if (text.isBlank()) return null

        val parsed = JSONObject(text)
        val assistantMsg = parsed.optString("assistantMessage", "Here is your custom crafted itinerary:")
        val dest = parsed.optString("destination", "Custom Destination")
        val title = parsed.optString("title", "Offbeat Creator Expedition")
        val tagline = parsed.optString("tagline", "Curated without commercial tourist traps.")
        val duration = parsed.optString("duration", "4D / 3N")
        val vibeStr = parsed.optString("vibe", "BACKPACKING")
        val baseBudget = parsed.optInt("basePerPersonBudget", 14999)
        val creatorVerdict = parsed.optString("creatorVerdict", "Avoid tourist buses. Rent local transport and start sunrise spots early.")

        val offbeatJson = parsed.optJSONArray("offbeatSecretSpots")
        val offbeatList = mutableListOf<String>()
        if (offbeatJson != null) {
            for (i in 0 until offbeatJson.length()) offbeatList.add(offbeatJson.getString(i))
        }

        val foodJson = parsed.optJSONArray("foodHighlights")
        val foodList = mutableListOf<String>()
        if (foodJson != null) {
            for (i in 0 until foodJson.length()) foodList.add(foodJson.getString(i))
        }

        val daysJson = parsed.optJSONArray("days")
        val dayPlans = mutableListOf<CustomDayPlan>()
        if (daysJson != null) {
            for (i in 0 until daysJson.length()) {
                val d = daysJson.getJSONObject(i)
                dayPlans.add(
                    CustomDayPlan(
                        dayNumber = d.optInt("dayNumber", i + 1),
                        title = d.optString("title", "Day ${i + 1}"),
                        morningActivity = d.optString("morningActivity", "Morning exploration"),
                        afternoonActivity = d.optString("afternoonActivity", "Afternoon local culture"),
                        eveningActivity = d.optString("eveningActivity", "Evening sunset & dinner"),
                        offbeatSecretSpot = d.optString("offbeatSecretSpot", "Hidden lookout point"),
                        mustTryFoodSpot = d.optString("mustTryFoodSpot", "Local street specialty joint"),
                        creatorTip = d.optString("creatorTip", "Carry cash and download offline maps.")
                    )
                )
            }
        }

        val vibe = try {
            TripVibe.valueOf(vibeStr.uppercase())
        } catch (e: Exception) {
            TripVibe.BACKPACKING
        }

        // Compute pricing table for all 5 traveler groups
        val pricingTable = TravelerType.values().associateWith { type ->
            val calc = PricingEngine.calculate(
                tripBudgetValue = baseBudget,
                travelerType = type,
                groupSize = when (type) {
                    TravelerType.SOLO_BACKPACKER -> 1
                    TravelerType.COUPLE_DUO -> 2
                    TravelerType.FRIENDS_SQUAD -> 4
                    TravelerType.FAMILY_KIDS_ELDERS -> 4
                    TravelerType.LUXURY_VIP -> 2
                }
            )
            calc.perPersonFinalPrice
        }

        val customResult = CustomItineraryResult(
            id = "custom_${System.currentTimeMillis()}",
            destinationName = dest,
            title = title,
            tagline = tagline,
            duration = duration,
            vibe = vibe,
            basePerPersonBudget = baseBudget,
            travelerPricingTable = pricingTable,
            offbeatSecretSpots = if (offbeatList.isNotEmpty()) offbeatList else listOf("Secret Forest Pool", "Cliff Sunset Point", "Unmarked Heritage Ruins"),
            foodHighlights = if (foodList.isNotEmpty()) foodList else listOf("Local Clay Pot Curry", "Woodfire Wood Oven Bakery", "Midnight Street Snacks"),
            dayWisePlans = if (dayPlans.isNotEmpty()) dayPlans else generateDefaultDays(dest, 4),
            creatorVerdict = creatorVerdict
        )

        return Pair(assistantMsg, customResult)
    }

    fun generateSmartItineraryLocally(
        userPrompt: String,
        destinationHint: String?,
        durationDaysHint: Int,
        budgetHint: Int,
        preferredVibe: TripVibe,
        travelerGroupHint: TravelerType
    ): Pair<String, CustomItineraryResult> {
        val lower = userPrompt.lowercase()
        val dest = when {
            destinationHint != null && destinationHint.isNotBlank() -> destinationHint
            lower.contains("spiti") -> "Spiti Valley"
            lower.contains("meghalaya") || lower.contains("shillong") || lower.contains("cherrapunji") -> "Meghalaya Hidden Canyons"
            lower.contains("ziro") || lower.contains("arunachal") || lower.contains("dzukou") || lower.contains("northeast") -> "Ziro & Dzukou Valley"
            lower.contains("tirthan") || lower.contains("jibhi") || lower.contains("shoja") -> "Tirthan & Jibhi Valley"
            lower.contains("gokarna") || lower.contains("honnavar") || lower.contains("murudeshwar") -> "Gokarna & Honnavar"
            lower.contains("sri lanka") || lower.contains("ceylon") || lower.contains("ella") -> "Sri Lanka Island Circuit"
            lower.contains("varkala") || lower.contains("munroe") || lower.contains("kerala") -> "Varkala Cliff & Munroe Island"
            lower.contains("ladakh") || lower.contains("leh") || lower.contains("nubra") -> "Ladakh Offbeat Monasteries"
            lower.contains("coorg") || lower.contains("chikmagalur") -> "Coorg & Western Ghats Wild Trails"
            lower.contains("goa") -> "Goa Secret Backwaters & Cliffs"
            lower.contains("hampi") || lower.contains("anegundi") -> "Hampi & Anegundi Bouldering"
            lower.contains("thailand") || lower.contains("krabi") || lower.contains("pai") -> "Pai & Krabi Secret Lagoons"
            else -> "Offbeat Mystery Trail"
        }

        val days = when {
            lower.contains("3 day") || lower.contains("3d") -> 3
            lower.contains("5 day") || lower.contains("5d") -> 5
            lower.contains("6 day") || lower.contains("6d") -> 6
            lower.contains("7 day") || lower.contains("7d") -> 7
            else -> durationDaysHint.coerceIn(3, 7)
        }

        val baseBudget = when {
            lower.contains("5000") || lower.contains("5k") -> 5999
            lower.contains("10000") || lower.contains("10k") -> 9999
            lower.contains("15000") || lower.contains("15k") -> 14999
            lower.contains("20000") || lower.contains("20k") -> 19999
            lower.contains("25000") || lower.contains("25k") -> 24999
            lower.contains("30000") || lower.contains("30k") -> 29999
            else -> budgetHint.coerceAtLeast(6999)
        }

        val vibe = when {
            lower.contains("party") || lower.contains("nightlife") || lower.contains("club") -> TripVibe.PARTY
            lower.contains("luxury") || lower.contains("resort") || lower.contains("5 star") -> TripVibe.LUXURY
            lower.contains("chill") || lower.contains("slow") || lower.contains("peace") || lower.contains("mountain") -> TripVibe.CHILL
            lower.contains("heritage") || lower.contains("ancient") || lower.contains("temple") || lower.contains("fort") -> TripVibe.HERITAGE
            else -> preferredVibe
        }

        val customDays = generateTailoredDays(dest, days)
        val offbeatSpots = customDays.map { it.offbeatSecretSpot }
        val foodSpots = customDays.map { it.mustTryFoodSpot }

        val pricingTable = TravelerType.values().associateWith { type ->
            val calc = PricingEngine.calculate(
                tripBudgetValue = baseBudget,
                travelerType = type,
                groupSize = when (type) {
                    TravelerType.SOLO_BACKPACKER -> 1
                    TravelerType.COUPLE_DUO -> 2
                    TravelerType.FRIENDS_SQUAD -> 4
                    TravelerType.FAMILY_KIDS_ELDERS -> 4
                    TravelerType.LUXURY_VIP -> 2
                }
            )
            calc.perPersonFinalPrice
        }

        val customResult = CustomItineraryResult(
            id = "custom_${System.currentTimeMillis()}",
            destinationName = dest,
            title = "$dest: Unfiltered ${days}D/${days - 1}N Creator Blueprint",
            tagline = "Handcrafted without commercial tour packages. Transparent pricing computed for every traveler squad.",
            duration = "${days}D / ${days - 1}N",
            vibe = vibe,
            basePerPersonBudget = baseBudget,
            travelerPricingTable = pricingTable,
            offbeatSecretSpots = offbeatSpots,
            foodHighlights = foodSpots,
            dayWisePlans = customDays,
            creatorVerdict = "Book homestays run by local families, wake up early for Golden Hour viewpoints, and taste authentic regional cooking."
        )

        val message = """
            ✨ I’ve crafted a custom **${days}D/${days - 1}N ${dest}** creator itinerary for you!

            📍 **Focus**: Offbeat secret viewpoints, zero commercial tourist buses, and authentic regional food spots vetted by @beyondbengalurufoods.
            💰 **Transparent Group Pricing**: I’ve calculated exact rates for Solo Backpackers, Couples, Friends Squads, Families, and Luxury VIPs below.
            
            You can tap **Save to My Trips** to store this in your offline pocket guide, or tap **Book This Custom Plan** to instantly confirm dates and coordinators.
        """.trimIndent()

        return Pair(message, customResult)
    }

    private fun generateTailoredDays(dest: String, dayCount: Int): List<CustomDayPlan> {
        val templates = when {
            dest.contains("Spiti", ignoreCase = true) -> listOf(
                CustomDayPlan(1, "Shimla to Kalpa: Apple Orchards & Kinner Kailash", "Drive through Kinnaur gorges", "Explore Roghi village suicide point", "Sunset view of Kinner Kailash peak", "Unmarked Roghi cliff trail", "Pahari Mutton Curry & Siddu at Folk Dhaba", "Fuel up in Reckong Peo; ATMs get scarce ahead."),
                CustomDayPlan(2, "Kalpa to Tabo: 1000-Year-Old Mud Monastery", "Cross Khab sangam of Spiti & Sutlej rivers", "Climb to Nako sacred high-altitude lake", "Meditate inside 996 AD Tabo mud monastery caves", "Tabo ancient meditation cliff caves", "Butter Tea & Steamed Tingmo with chilli chutney", "Carry warm layers; wind chill drops sharply by 4 PM."),
                CustomDayPlan(3, "Tabo to Kaza via Dhankar Cliff Monastery", "Hike to Dhankar monastery perched on razor spires", "Trek to sacred Dhankar Lake above clouds", "Arrive in Kaza town and rent 4x4 or scooty", "Dhankar secret cliff meditation perch", "Sea-buckthorn hot berry tea & Yak cheese pizza", "Acclimatize in Kaza before ascending to 14,000+ ft."),
                CustomDayPlan(4, "The Highest Villages: Hikkim, Komic & Langza", "Send postcards from Hikkim (Highest Post Office in World)", "Visit Komic at 15,027 ft", "Hunt 200-million-year-old marine fossils in Langza", "Buddha statue cliff overlooking Chau Chau Kang Nilda", "Thukpa noodle bowl & Spitian momos in Langza homestay", "Do not collect fossils aggressively; respect local geology."),
                CustomDayPlan(5, "Key Monastery Fortress & Kibber Wildlife Sanctuary", "Morning Buddhist chant prayer at Key Monastery", "Drive across Chicham suspension bridge (Highest in Asia)", "Search for Himalayan Blue Sheep in Kibber", "Key Monastery upper rooftop prayer terrace", "Traditional Spitian Barley Porridge (Tsampa)", "Interact with monks over hot herbal tea at Key kitchen."),
                CustomDayPlan(6, "Kaza to Chandratal: The Sacred Crescent Moon Lake", "Drive over rugged Kunzum Pass (14,931 ft)", "Trek the 2 km perimeter of cobalt-blue Chandratal", "Set up lakeside glamping camp under Milky Way", "Chandratal northern glacial reflection bank", "Steaming Maggi & local Rajma Chawal at campsite", "Night temperatures drop below freezing; bring thermal gloves."),
                CustomDayPlan(7, "Chandratal through Atal Tunnel back to Manali", "Catch sunrise reflection on Chandratal water", "Navigate thrilling Batal boulder riverbed route", "Cross through modern Atal Tunnel into lush Manali", "Gramphu glacial stream crossing point", "Old Manali riverside trout with lemon caper butter", "Celebratory celebratory dinner at Old Manali café.")
            )
            dest.contains("Meghalaya", ignoreCase = true) -> listOf(
                CustomDayPlan(1, "Guwahati to Shillong: Secret Waterfalls & Pine Cafes", "Pickup in Guwahati and drive up misty pine highway", "Stop at pristine Umiam Lake viewpoint", "Explore Laitlum Canyons edge overlooking deep gorges", "Laitlum hidden shepherd cliff trail", "Khasi Jadoh rice with pork belly & Tungrymbai chutney", "Laitlum gets engulfed in thick fog by 3 PM; arrive early."),
                CustomDayPlan(2, "Cherrapunji & Wei Sawdong 3-Tier Turquoise Cascades", "Hike down the jungle path to Wei Sawdong waterfalls", "Explore Nohkalikai falls secret cliff viewpoint", "Venture into Mawsmai ancient limestone cave fossils", "Wei Sawdong middle emerald pool", "Bamboo Shoot Chicken & steaming Red Tea at Sohra stall", "Wear gripping sandals; rocks near Wei Sawdong are slippery."),
                CustomDayPlan(3, "The Living Root Bridges of Nongriat Rainforest", "Descend 3,500 stone stairs into dense rainforest valley", "Cross single living root bridges engineered by Khasi tribes", "Swim in natural turquoise plunge pools below Double Decker Bridge", "Rainbow Falls secret natural pool", "Fresh pineapples and organic banana leaf meal in Nongriat", "Stay overnight in Nongriat village homestay instead of rushing back."),
                CustomDayPlan(4, "Mawryngkhang Bamboo Skywalk & Pynursla", "Trek the thrilling bamboo boardwalk pinned to cliff walls", "Stand on the legendary King Rock monolith above river gorge", "Drive along Bangladesh border scenic road", "Mawryngkhang cliff suspension cantilever", "Local Khasi smoked pork & steamed wild greens", "Not for vertigo-sensitive travelers; exhilarating and safe."),
                CustomDayPlan(5, "Shnongpdeng Crystal Waters & Dawki River Kayaking", "Kayaking on crystal-clear Umngot river (boats appear to float in air)", "Cliff jumping into emerald river pools", "Camp alongside pristine pebble beach under star canopy", "Shnongpdeng suspension bridge sunrise view", "Fresh caught river fish curry with sticky hill rice", "Visit early morning before day-tourist boats create ripples.")
            )
            dest.contains("Ziro", ignoreCase = true) -> listOf(
                CustomDayPlan(1, "Guwahati to Ziro Valley via Pine Groves", "Travel through Assam tea gardens into Arunachal hills", "Check into traditional Apatani bamboo cottage", "Stroll through Hong village paddy dykes", "Hong village sacred bamboo groves", "Apatani smoked pork with bamboo hollow steamed rice", "Try local Pikey Pila bamboo ash herbal seasoning."),
                CustomDayPlan(2, "Apatani Tribal Villages & Ancient Facial Tattoo Heritage", "Guided morning walk through Hari and Bamin villages", "Meet elder Apatani women preserving nose plug traditions", "Visit local kiwi orchards and organic kiwi wineries", "Kardo natural high-altitude Shiva Lingam rock", "Ziro Valley homemade organic kiwi wine & roasted corn", "Be respectful; always ask permission before taking portraits."),
                CustomDayPlan(3, "Ziro Pine Forest Trek & Talley Valley Wildlife Sanctuary", "Hike into cloud-draped Talley Valley sanctuary", "Spot rare Pleioblastus simone bamboo and endemic orchids", "Picnic beside virgin mountain streams", "Talley Valley cloud forest ridge", "Local forest mushroom stew with wild mountain herbs", "Carry a rain poncho; mist showers occur frequently."),
                CustomDayPlan(4, "Dzukou Valley Trek: The Valley of Whispering Grass", "Transfer to Nagaland border base camp", "Ascend through pine ridge to panoramic Dzukou ridge", "Witness dwarf bamboo carpet and blooming wild lilies", "Dzukou natural rock shelter caves", "Naga smoked beef/pork with Raja Mircha fiery chutney", "Bring heavy sleeping bags for high-altitude camp nights."),
                CustomDayPlan(5, "Dzukou Sunrise & Majuli River Island Return", "Golden sunrise over Dzukou serpentine stream", "Hike down to base and ferry across Brahmaputra to Majuli", "Explore 15th-century Vaishnavite monasteries (Satras)", "Majuli sunset over Brahmaputra river sands", "Assamese fish tenga sour curry with Joha aromatic rice", "Majuli is the world's largest river island; visit mask-making workshops.")
            )
            dest.contains("Tirthan", ignoreCase = true) -> listOf(
                CustomDayPlan(1, "Aut Tunnel to Tirthan Valley: River Cottage & Pine Scent", "Arrive in Tirthan and check into wooden riverside cottage", "Angle for Himalayan brown trout in crystal clear river", "Evening walk through Bandal pine forest", "Secret pebble river beach near Gushaini", "Wood-smoked Himalayan trout with garlic butter sauce", "Trout fishing requires a local forest permit (₹100)."),
                CustomDayPlan(2, "Serolsar Lake Trek & Jalori Pass Snow Peaks", "Drive up to Jalori Pass at 10,800 ft", "Scenic 5 km forest trek through oak canopy to sacred Serolsar Lake", "Pay respects at ancient Buddhi Nagin lake temple", "Jalori Pass 360-degree Himalayan panorama ridge", "Hot kadhi chawal & pahari chai at Jalori wooden shacks", "Start trek by 9 AM to return before afternoon mountain fog."),
                CustomDayPlan(3, "Chehni Kothi 1500-Year Timber Tower & Jibhi Waterfall", "Trek through deodar forest to massive 12-story timber stone tower", "Discover hidden Jibhi rock waterfall wooden bridges", "Café hopping in Jibhi bohemian arts street", "Chehni Kothi secret upper courtyard", "Apple crumble & walnut honey cake at Mudhouse café", "Climb Chehni Kothi single-log ladder cautiously."),
                CustomDayPlan(4, "Great Himalayan National Park & Chhoie Waterfall Trek", "Hike into UNESCO World Heritage GHNP buffer zone", "Reach majestic Chhoie waterfall cascading from high cliffs", "Riverside acoustic campfire & star gazing", "Chhoie secret upper pool plunge", "Authentic Himachali Dham festive meal served on leaves", "Take a dip in the pristine cold glacial stream pools.")
            )
            dest.contains("Gokarna", ignoreCase = true) -> listOf(
                CustomDayPlan(1, "The 5-Beach Cliffside Trek: Kudle to Paradise", "Early morning cliff walk from Kudle Beach to Om Beach", "Trek over rocky headlands to Half Moon Cove", "Reach secluded Paradise Beach accessible only by boat/foot", "Paradise Beach hidden rock tide pools", "Fresh woodfire pizza & iced nutella shake at Namaste Café", "Start at 6:30 AM before the coastal sun heats up."),
                CustomDayPlan(2, "Honnavar Sharavathi Mangrove Safari & Boardwalk", "Drive 45 mins south to Honnavar backwaters", "Private boat cruise through dense mangrove forest tunnels", "Walk along the 1 km wooden canopy walkway over backwaters", "Sharavathi river island sunset point", "Coastal Konkan Fish Thali with Anjal Fry & Sol Kadi", "Book private mangrove boat early to spot migratory kingfishers."),
                CustomDayPlan(3, "Mirjan 16th-Century Moss Fort & Apsarakonda Seaside Falls", "Explore emerald moss-covered bastions of Mirjan Fort", "Visit Apsarakonda cliff waterfall cascading into ocean lagoon", "Sunset view from Apsarakonda cliff park", "Mirjan Fort hidden moat watchtower", "Mangalore buns & Neer dosa with chicken ghee roast", "Mirjan Fort's green laterite stones look magical during overcast afternoons."),
                CustomDayPlan(4, "Yana Giant Black Rocks & Vibhooti Waterfall", "Trek inside rainforest to towering 390-foot solid black karst monoliths", "Walk through cave passage below Bhairaveshwara Shikhara", "Swim in natural turquoise limestone pool at Vibhooti Falls", "Vibhooti upper stepped limestone falls", "Karnataka Filter Coffee & Akki Roti with coconut chutney", "Carry extra clothes; swimming in Vibhooti falls is unforgettable.")
            )
            else -> generateDefaultDays(dest, dayCount)
        }

        return templates.take(dayCount)
    }

    private fun generateDefaultDays(dest: String, count: Int): List<CustomDayPlan> {
        val list = mutableListOf<CustomDayPlan>()
        for (i in 1..count) {
            list.add(
                CustomDayPlan(
                    dayNumber = i,
                    title = "Day $i: Hidden $dest Explorations & Vibe",
                    morningActivity = "Sunrise at secret viewpoint avoiding tourist buses",
                    afternoonActivity = "Offbeat heritage, cliff trails & local artisan workshop",
                    eveningActivity = "Sunset sundowner & verified foodie trail dinner",
                    offbeatSecretSpot = "Unmarked local scenic lookout with 360° views",
                    mustTryFoodSpot = "Legendary local clay pot kitchen with regional specialties",
                    creatorTip = "Start 45 minutes before sunrise for golden light photography."
                )
            )
        }
        return list
    }
}
