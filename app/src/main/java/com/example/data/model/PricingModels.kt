package com.example.data.model

enum class TravelerType(
    val title: String,
    val subtitle: String,
    val multiplier: Double,
    val accommodationType: String,
    val transportType: String,
    val foodStyle: String,
    val iconEmoji: String,
    val baseGroupRange: String
) {
    SOLO_BACKPACKER(
        title = "Solo Explorer / Backpacker",
        subtitle = "Boutique social hostels, rented scooter / shared transit & authentic local stalls",
        multiplier = 0.80,
        accommodationType = "Curated Boutique Hostel Pod / Scenic Homestay",
        transportType = "Self-Drive Scooty / Shared Scenic Transit",
        foodStyle = "Local street eats, legendary thalis & night market joints",
        iconEmoji = "🎒",
        baseGroupRange = "1 Traveler"
    ),
    COUPLE_DUO(
        title = "Couple / Duo Romantic",
        subtitle = "Private boutique villa/cottage, sunset dinners & private scooty/hatchback",
        multiplier = 1.00,
        accommodationType = "Private Boutique Villa / Seaview Cottage with Balcony",
        transportType = "Private Self-Drive Hatchback / Premium Scooty",
        foodStyle = "Curated café crawls, seaside seafood & romantic sunset dining",
        iconEmoji = "💑",
        baseGroupRange = "2 Travelers"
    ),
    FRIENDS_SQUAD(
        title = "Friends Squad (3 to 6)",
        subtitle = "Private pool villa, split chauffeur SUV & group activity passes (Group discount)",
        multiplier = 0.85,
        accommodationType = "Entire Private 2-3 BHK Pool Villa / Group Luxury Wing",
        transportType = "Private AC Ertiga / Innova Chauffeur Driven",
        foodStyle = "Barbecue nights, sharing food platters & local craft brews",
        iconEmoji = "🎉",
        baseGroupRange = "3-6 Travelers"
    ),
    FAMILY_KIDS_ELDERS(
        title = "Family with Kids & Elders",
        subtitle = "Spacious 4-5★ family suites, smooth AC Innova Crysta, relaxed pace & kid-safe food",
        multiplier = 1.18,
        accommodationType = "4-Star / 5-Star Resort Family Suites with Pool & Elevators",
        transportType = "Dedicated AC Chauffeur Driven Innova Crysta / Tempo Traveller",
        foodStyle = "Curated hygienic family-friendly restaurants & high tea",
        iconEmoji = "👨‍👩‍👧‍👦",
        baseGroupRange = "3-8 Travelers"
    ),
    LUXURY_VIP(
        title = "Luxury Creator / VIP Experience",
        subtitle = "5★ clifftop pool suites, private speedboats, fine dining & personal trip fixer + reel shoot",
        multiplier = 1.75,
        accommodationType = "5-Star Luxury Heritage Palace / Clifftop Plunge Pool Villa",
        transportType = "Private Luxury SUV / Speedboat Charter / Dedicated Chauffeur",
        foodStyle = "Chef's 5-course tasting menu, yacht champagne lunches & VIP access",
        iconEmoji = "👑",
        baseGroupRange = "1-12 Travelers"
    )
}

enum class TravelSeason(val label: String, val priceMultiplier: Double, val badge: String) {
    REGULAR("Standard Season (Best Value)", 1.0, "🌿 Best Rates"),
    PEAK("Peak Holiday / Festival Season", 1.20, "🔥 High Demand"),
    MONSOON_OFFBEAT("Monsoon Offbeat Special", 0.88, "🌧️ Lush & Green (12% Off)")
}

data class BookingAddOn(
    val id: String,
    val name: String,
    val description: String,
    val pricePerPerson: Int = 0,
    val flatPricePerGroup: Int = 0,
    val iconEmoji: String
)

val AVAILABLE_ADD_ONS = listOf(
    BookingAddOn(
        id = "food_tour",
        name = "Creator Secret Food Crawl",
        description = "Guided food trail featuring 4 hidden street stalls & verified @beyondbengalurufoods spots",
        pricePerPerson = 1499,
        iconEmoji = "🍲"
    ),
    BookingAddOn(
        id = "drone_shoot",
        name = "Cinematic Drone & Reel Package",
        description = "Professional 4K drone shots + 2 edited 60s Instagram/TikTok reels of your trip",
        flatPricePerGroup = 3999,
        iconEmoji = "🎬"
    ),
    BookingAddOn(
        id = "flight_assist",
        name = "Flight / Train Coordination & Transfers",
        description = "End-to-end airport pickup, luggage assistance and zero-layover route booking",
        pricePerPerson = 4999,
        iconEmoji = "✈️"
    ),
    BookingAddOn(
        id = "travel_insurance",
        name = "Comprehensive Travel & Medical Cover",
        description = "24/7 medical evacuation, trek injury insurance & instant luggage loss protection",
        pricePerPerson = 499,
        iconEmoji = "🛡️"
    )
)

data class PricingCalculation(
    val baseTripPrice: Int,
    val travelerType: TravelerType,
    val groupSize: Int,
    val season: TravelSeason,
    val perPersonBasePrice: Int,
    val perPersonAfterTravelerType: Int,
    val perPersonAddOns: Int,
    val groupFlatAddOns: Int,
    val perPersonFinalPrice: Int,
    val totalGroupPrice: Int,
    val staysCostTotal: Int,
    val transportCostTotal: Int,
    val foodCostTotal: Int,
    val activitiesAndPassesTotal: Int,
    val creatorPerksTotal: Int
)

object PricingEngine {
    fun calculate(
        tripBudgetValue: Int,
        travelerType: TravelerType,
        groupSize: Int,
        season: TravelSeason = TravelSeason.REGULAR,
        selectedAddOnIds: Set<String> = emptySet()
    ): PricingCalculation {
        val baseBudgetValue = if (tripBudgetValue > 0) tripBudgetValue else 9999
        val effectiveGroup = groupSize.coerceAtLeast(1)

        // Traveler type multiplier
        val perPersonAdjusted = (baseBudgetValue * travelerType.multiplier * season.priceMultiplier).toInt()

        // Additional group volume discount for friends groups >= 4
        val groupVolumeDiscount = if (travelerType == TravelerType.FRIENDS_SQUAD && effectiveGroup >= 4) {
            (perPersonAdjusted * 0.08).toInt() // 8% extra group discount
        } else 0

        val perPersonDiscounted = (perPersonAdjusted - groupVolumeDiscount).coerceAtLeast(1999)

        // Calculate add-ons
        val activeAddOns = AVAILABLE_ADD_ONS.filter { selectedAddOnIds.contains(it.id) }
        val perPersonAddOnsTotal = activeAddOns.sumOf { it.pricePerPerson }
        val groupFlatAddOnsTotal = activeAddOns.sumOf { it.flatPricePerGroup }

        val perPersonFinal = perPersonDiscounted + perPersonAddOnsTotal + (groupFlatAddOnsTotal / effectiveGroup)
        val totalGroup = (perPersonDiscounted + perPersonAddOnsTotal) * effectiveGroup + groupFlatAddOnsTotal

        // Itemized breakdown percentages
        val staysTotal = (totalGroup * 0.38).toInt()
        val transportTotal = (totalGroup * 0.24).toInt()
        val foodTotal = (totalGroup * 0.20).toInt()
        val activitiesTotal = (totalGroup * 0.12).toInt()
        val creatorPerksTotal = totalGroup - (staysTotal + transportTotal + foodTotal + activitiesTotal)

        return PricingCalculation(
            baseTripPrice = baseBudgetValue,
            travelerType = travelerType,
            groupSize = effectiveGroup,
            season = season,
            perPersonBasePrice = baseBudgetValue,
            perPersonAfterTravelerType = perPersonDiscounted,
            perPersonAddOns = perPersonAddOnsTotal,
            groupFlatAddOns = groupFlatAddOnsTotal,
            perPersonFinalPrice = perPersonFinal,
            totalGroupPrice = totalGroup,
            staysCostTotal = staysTotal,
            transportCostTotal = transportTotal,
            foodCostTotal = foodTotal,
            activitiesAndPassesTotal = activitiesTotal,
            creatorPerksTotal = creatorPerksTotal.coerceAtLeast(0)
        )
    }
}
