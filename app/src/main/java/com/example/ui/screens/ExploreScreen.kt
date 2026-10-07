package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowForward
import androidx.compose.material.icons.filled.Casino
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.FavoriteBorder
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.MenuAnchorType
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.example.data.model.DestinationSpotlight
import com.example.data.model.Trip
import com.example.ui.components.GlassCard
import com.example.ui.components.GoldButton
import com.example.ui.components.GoldPillBadge
import com.example.ui.components.MarqueeTicker
import com.example.ui.components.RatingStars
import com.example.ui.components.VibeBadge
import com.example.ui.theme.AccentGreen
import com.example.ui.theme.BgDark
import com.example.ui.theme.BgDarkCard
import com.example.ui.theme.BgDarkElevated
import com.example.ui.theme.BgDarkSurface
import com.example.ui.theme.GlassBorder
import com.example.ui.theme.GlassBorderGold
import com.example.ui.theme.GlassBorderStrong
import com.example.ui.theme.GlassSurface
import com.example.ui.theme.GoldContainer
import com.example.ui.theme.GoldDark
import com.example.ui.theme.GoldPrimary
import com.example.ui.theme.GoldSecondary
import com.example.ui.theme.TextMuted
import com.example.ui.theme.TextPrimary
import com.example.ui.theme.TextSecondary
import com.example.ui.theme.TextTertiary
import com.example.ui.viewmodel.AppTab
import com.example.ui.viewmodel.MainViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ExploreScreen(
    viewModel: MainViewModel,
    modifier: Modifier = Modifier
) {
    val trips = viewModel.getAllTrips()
    val spotlights = viewModel.getSpotlights()
    val reviews = viewModel.getTravelerReviews()
    val smartMatch by viewModel.smartMatchState.collectAsState()
    val wishlist by viewModel.wishlist.collectAsState()

    var newsletterEmail by remember { mutableStateOf("") }

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .background(BgDark)
            .testTag("explore_screen"),
        verticalArrangement = Arrangement.spacedBy(28.dp)
    ) {
        // 1. Hero Banner
        item {
            HeroHeaderSection(
                onPlanClick = { viewModel.setTab(AppTab.TRIP_PLANNER) },
                onExploreClick = { /* scroll down */ },
                onSurpriseClick = { viewModel.surpriseTrip() }
            )
        }

        // 2. Marquee Ticker
        item {
            MarqueeTicker(
                items = listOf(
                    "No Tourist Traps",
                    "Real Itineraries",
                    "Goa",
                    "Thailand",
                    "Krabi",
                    "Himachal",
                    "Malaysia",
                    "Pondicherry",
                    "Creator-Led Routes",
                    "Bengaluru To The World"
                )
            )
        }

        // 3. Smart Match Trip Finder Card
        item {
            SmartTripFinderCard(
                smartMatchState = smartMatch,
                onDestinationChange = { dest, budget -> viewModel.updateSmartMatch(dest, budget) },
                onTravelersChange = { viewModel.setSmartTravelers(it) },
                onFindTrip = {
                    val target = trips.find { it.id.equals(smartMatch.selectedDestinationId, ignoreCase = true) } ?: trips.first()
                    viewModel.selectTrip(target)
                },
                modifier = Modifier.padding(horizontal = 20.dp)
            )
        }

        // 4. Quick Trending Filter Chips
        item {
            TrendingChipsSection(
                onChipClick = { dest, budget ->
                    viewModel.updateSmartMatch(dest, budget)
                    val target = trips.find { it.id.equals(dest, ignoreCase = true) }
                    target?.let { viewModel.selectTrip(it) }
                },
                modifier = Modifier.padding(horizontal = 20.dp)
            )
        }

        // 5. Curated Itineraries Section Header
        item {
            Column(modifier = Modifier.padding(horizontal = 20.dp)) {
                GoldPillBadge(text = "Curated Itineraries")
                Spacer(modifier = Modifier.height(10.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = "Trips That Actually Slap.",
                            style = MaterialTheme.typography.headlineLarge.copy(
                                fontWeight = FontWeight.ExtraBold,
                                color = TextPrimary
                            )
                        )
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            text = "Every route built from real experience. Not an agency PDF brochure. 100% creator-led.",
                            style = MaterialTheme.typography.bodyMedium.copy(color = TextSecondary)
                        )
                    }

                    // Surprise Me button
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(100.dp))
                            .background(GlassSurface)
                            .border(1.dp, GlassBorderGold, RoundedCornerShape(100.dp))
                            .clickable { viewModel.surpriseTrip() }
                            .padding(horizontal = 14.dp, vertical = 10.dp)
                            .testTag("surprise_button")
                    ) {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(6.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Default.Casino,
                                contentDescription = "Surprise Me",
                                tint = GoldPrimary,
                                modifier = Modifier.size(16.dp)
                            )
                            Text(
                                text = "SURPRISE",
                                style = MaterialTheme.typography.labelSmall.copy(
                                    color = GoldPrimary,
                                    fontWeight = FontWeight.Bold
                                )
                            )
                        }
                    }
                }
            }
        }

        // 6. Itinerary Cards List
        items(trips) { trip ->
            val isWishlisted = wishlist.any { it.tripId == trip.id }
            TripCard(
                trip = trip,
                isWishlisted = isWishlisted,
                onWishlistToggle = { viewModel.toggleWishlist(trip) },
                onViewDetails = { viewModel.selectTrip(trip) },
                onStartGuide = { viewModel.startLivePocketGuide(trip) },
                modifier = Modifier.padding(horizontal = 20.dp)
            )
        }

        // 7. Destination Mosaic Spotlight
        item {
            DestinationSpotlightsSection(
                spotlights = spotlights,
                onSpotlightClick = { spot ->
                    val matchingTrip = trips.find { it.id.contains(spot.id, ignoreCase = true) }
                    matchingTrip?.let { viewModel.selectTrip(it) }
                },
                modifier = Modifier.padding(horizontal = 20.dp)
            )
        }

        // 8. Why Us Grid
        item {
            WhyUsSection(modifier = Modifier.padding(horizontal = 20.dp))
        }

        // 9. Real Traveler Reviews
        item {
            TravelerReviewsSection(reviews = reviews, modifier = Modifier.padding(horizontal = 20.dp))
        }

        // 10. Direct CTA Band
        item {
            CtaBandSection(
                onPlanTrip = { viewModel.setTab(AppTab.TRIP_PLANNER) },
                onWhatsAppClick = { viewModel.openWhatsApp() },
                onCallClick = { viewModel.callPhone() },
                onEmailClick = { viewModel.openEmail() },
                modifier = Modifier.padding(horizontal = 20.dp)
            )
        }

        // 11. Footer with Newsletter
        item {
            FooterSection(
                email = newsletterEmail,
                onEmailChange = { newsletterEmail = it },
                onSubscribe = {
                    viewModel.subscribeNewsletter(newsletterEmail)
                    newsletterEmail = ""
                },
                onInstagramClick = { viewModel.openInstagram() },
                onYouTubeClick = { viewModel.openYouTube() },
                onWhatsAppClick = { viewModel.openWhatsApp() },
                onCallClick = { viewModel.callPhone() },
                onEmailClick = { viewModel.openEmail() },
                modifier = Modifier.padding(horizontal = 20.dp, vertical = 20.dp)
            )
        }
    }
}

@Composable
fun HeroHeaderSection(
    onPlanClick: () -> Unit,
    onExploreClick: () -> Unit,
    onSurpriseClick: () -> Unit
) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(480.dp)
    ) {
        // Hero Background Image with dark gradient overlay
        AsyncImage(
            model = "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&q=80",
            contentDescription = "Mountains Landscape",
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )

        // Gradient layers for dramatic editorial depth
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(
                    Brush.verticalGradient(
                        colors = listOf(
                            Color(0x99080A0F),
                            Color(0xCC080A0F),
                            BgDark
                        )
                    )
                )
        )

        // Content
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(24.dp),
            verticalArrangement = Arrangement.Bottom
        ) {
            GoldPillBadge(text = "India's 1st creator-led tour operator")

            Spacer(modifier = Modifier.height(16.dp))

            Text(
                text = "YOUR NEXT\nTRIP, SORTED.",
                style = MaterialTheme.typography.displayLarge.copy(
                    fontWeight = FontWeight.ExtraBold,
                    color = TextPrimary,
                    lineHeight = 42.sp
                )
            )

            Spacer(modifier = Modifier.height(10.dp))

            Text(
                text = "Real trips. Real places. 100% creator-led.\nNo copy-paste routes. Curated by a Bengaluru creator who's actually been there.",
                style = MaterialTheme.typography.bodyLarge.copy(
                    color = TextSecondary,
                    lineHeight = 22.sp
                )
            )

            Spacer(modifier = Modifier.height(20.dp))

            Row(
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                GoldButton(
                    text = "Plan My Trip",
                    onClick = onPlanClick,
                    icon = Icons.Default.ArrowForward,
                    testTag = "hero_plan_button"
                )

                Button(
                    onClick = onSurpriseClick,
                    colors = ButtonDefaults.buttonColors(
                        containerColor = GlassSurface,
                        contentColor = TextPrimary
                    ),
                    shape = RoundedCornerShape(100.dp),
                    modifier = Modifier
                        .height(48.dp)
                        .border(1.dp, GlassBorderStrong, RoundedCornerShape(100.dp))
                ) {
                    Text(
                        text = "Surprise Me 🎲",
                        style = MaterialTheme.typography.labelLarge.copy(color = TextPrimary)
                    )
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            // Stats bar
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .border(1.dp, GlassBorder, RoundedCornerShape(16.dp))
                    .background(Color(0x33000000), RoundedCornerShape(16.dp))
                    .padding(vertical = 12.dp, horizontal = 16.dp),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                StatItem(number = "50+", label = "Verified spots")
                StatItem(number = "100%", label = "Creator-Led")
                StatItem(number = "0", label = "Tourist traps")
            }
        }
    }
}

@Composable
fun StatItem(number: String, label: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(
            text = number,
            style = MaterialTheme.typography.titleLarge.copy(
                color = GoldPrimary,
                fontWeight = FontWeight.ExtraBold
            )
        )
        Text(
            text = label.uppercase(),
            style = MaterialTheme.typography.labelSmall.copy(
                color = TextTertiary,
                fontSize = 9.sp,
                letterSpacing = 1.sp
            )
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SmartTripFinderCard(
    smartMatchState: com.example.ui.viewmodel.SmartMatchState,
    onDestinationChange: (String, Int) -> Unit,
    onTravelersChange: (String) -> Unit,
    onFindTrip: () -> Unit,
    modifier: Modifier = Modifier
) {
    val destinations = listOf(
        "goa" to "Goa 🎉",
        "thailand" to "Thailand 🌴",
        "himachal" to "Himachal 🏔️",
        "pondicherry" to "Pondicherry 🛕",
        "malaysia" to "Malaysia 🌆",
        "krabi" to "Krabi 🏝️",
        "gokarna" to "Gokarna 🏖️"
    )

    val budgetTiers = listOf(
        5000 to "Under ₹5k",
        15000 to "₹5k – ₹15k",
        30000 to "₹15k – ₹30k",
        50000 to "₹30k – ₹50k"
    )

    var destExpanded by remember { mutableStateOf(false) }
    var budgetExpanded by remember { mutableStateOf(false) }

    var selectedDestKey by remember { mutableStateOf(smartMatchState.selectedDestinationId ?: "goa") }
    var selectedBudgetKey by remember { mutableStateOf(smartMatchState.selectedBudgetTier ?: 15000) }

    GlassCard(
        modifier = modifier.fillMaxWidth(),
        borderColor = GlassBorderGold,
        backgroundColor = BgDarkCard
    ) {
        Column(
            modifier = Modifier.padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Text(
                    text = "Find Your Perfect Trip",
                    style = MaterialTheme.typography.titleLarge.copy(
                        fontWeight = FontWeight.Bold,
                        color = TextPrimary
                    )
                )
                Text(text = "✦", color = GoldPrimary)
            }

            Text(
                text = "Tell me your vibe and budget. I'll match you instantly.",
                style = MaterialTheme.typography.bodyMedium.copy(color = TextSecondary)
            )

            // Selectors Row
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                // Destination Dropdown
                ExposedDropdownMenuBox(
                    expanded = destExpanded,
                    onExpandedChange = { destExpanded = !destExpanded },
                    modifier = Modifier.weight(1f)
                ) {
                    val label = destinations.find { it.first == selectedDestKey }?.second ?: "Destination"
                    OutlinedTextField(
                        value = label,
                        onValueChange = {},
                        readOnly = true,
                        label = { Text("WHERE TO?", fontSize = 10.sp, color = GoldPrimary) },
                        trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = destExpanded) },
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = GoldPrimary,
                            unfocusedBorderColor = GlassBorder,
                            focusedTextColor = TextPrimary,
                            unfocusedTextColor = TextPrimary
                        ),
                        modifier = Modifier.menuAnchor(MenuAnchorType.PrimaryNotEditable)
                    )
                    ExposedDropdownMenu(
                        expanded = destExpanded,
                        onDismissRequest = { destExpanded = false },
                        modifier = Modifier.background(BgDarkElevated)
                    ) {
                        destinations.forEach { (key, display) ->
                            DropdownMenuItem(
                                text = { Text(display, color = TextPrimary) },
                                onClick = {
                                    selectedDestKey = key
                                    destExpanded = false
                                    onDestinationChange(key, selectedBudgetKey)
                                }
                            )
                        }
                    }
                }

                // Budget Dropdown
                ExposedDropdownMenuBox(
                    expanded = budgetExpanded,
                    onExpandedChange = { budgetExpanded = !budgetExpanded },
                    modifier = Modifier.weight(1f)
                ) {
                    val label = budgetTiers.find { it.first == selectedBudgetKey }?.second ?: "Budget"
                    OutlinedTextField(
                        value = label,
                        onValueChange = {},
                        readOnly = true,
                        label = { Text("BUDGET (₹/PERSON)", fontSize = 10.sp, color = GoldPrimary) },
                        trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = budgetExpanded) },
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = GoldPrimary,
                            unfocusedBorderColor = GlassBorder,
                            focusedTextColor = TextPrimary,
                            unfocusedTextColor = TextPrimary
                        ),
                        modifier = Modifier.menuAnchor(MenuAnchorType.PrimaryNotEditable)
                    )
                    ExposedDropdownMenu(
                        expanded = budgetExpanded,
                        onDismissRequest = { budgetExpanded = false },
                        modifier = Modifier.background(BgDarkElevated)
                    ) {
                        budgetTiers.forEach { (bVal, bLabel) ->
                            DropdownMenuItem(
                                text = { Text(bLabel, color = TextPrimary) },
                                onClick = {
                                    selectedBudgetKey = bVal
                                    budgetExpanded = false
                                    onDestinationChange(selectedDestKey, bVal)
                                }
                            )
                        }
                    }
                }
            }

            // Recommendation result banner
            if (!smartMatchState.recommendationTitle.isNullOrBlank()) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(14.dp))
                        .background(Color(0x1FE8C97A))
                        .border(1.dp, GlassBorderGold, RoundedCornerShape(14.dp))
                        .padding(14.dp)
                ) {
                    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(6.dp)
                        ) {
                            Text(
                                text = "✦ SMART MATCH",
                                style = MaterialTheme.typography.labelSmall.copy(
                                    color = GoldPrimary,
                                    fontWeight = FontWeight.Bold,
                                    letterSpacing = 1.sp
                                )
                            )
                        }
                        Text(
                            text = smartMatchState.recommendationTitle ?: "",
                            style = MaterialTheme.typography.titleMedium.copy(
                                color = TextPrimary,
                                fontWeight = FontWeight.Bold
                            )
                        )
                        Text(
                            text = smartMatchState.recommendationSub ?: "",
                            style = MaterialTheme.typography.bodyMedium.copy(
                                color = TextSecondary,
                                lineHeight = 18.sp
                            )
                        )
                    }
                }
            }

            // Find Button
            GoldButton(
                text = "View Matching Itinerary →",
                onClick = onFindTrip,
                modifier = Modifier.fillMaxWidth(),
                testTag = "smart_find_button"
            )
        }
    }
}

@Composable
fun TrendingChipsSection(
    onChipClick: (String, Int) -> Unit,
    modifier: Modifier = Modifier
) {
    val scrollState = rememberScrollState()
    val chips = listOf(
        Triple("thailand", 15000, "🌴 Thailand <₹15k"),
        Triple("goa", 5000, "🎉 Goa weekend"),
        Triple("himachal", 15000, "🏔️ Himachal vibes"),
        Triple("krabi", 30000, "🏝️ Krabi escape"),
        Triple("pondicherry", 5000, "🛕 Pondicherry chill"),
        Triple("gokarna", 5000, "🏖️ Gokarna coves"),
        Triple("malaysia", 30000, "🌆 Malaysia+Penang")
    )

    Column(modifier = modifier, verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Text(
            text = "TRENDING ITINERARIES",
            style = MaterialTheme.typography.labelSmall.copy(
                color = TextTertiary,
                letterSpacing = 1.5.sp,
                fontWeight = FontWeight.Bold
            )
        )

        Row(
            modifier = Modifier.horizontalScroll(scrollState),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            chips.forEach { (dest, budget, label) ->
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(100.dp))
                        .background(GlassSurface)
                        .border(1.dp, GlassBorder, RoundedCornerShape(100.dp))
                        .clickable { onChipClick(dest, budget) }
                        .padding(horizontal = 14.dp, vertical = 8.dp)
                ) {
                    Text(
                        text = label,
                        style = MaterialTheme.typography.labelMedium.copy(
                            color = TextPrimary,
                            fontWeight = FontWeight.Medium
                        )
                    )
                }
            }
        }
    }
}

@Composable
fun TripCard(
    trip: Trip,
    isWishlisted: Boolean,
    onWishlistToggle: () -> Unit,
    onViewDetails: () -> Unit,
    onStartGuide: () -> Unit,
    modifier: Modifier = Modifier
) {
    GlassCard(
        modifier = modifier
            .fillMaxWidth()
            .clickable { onViewDetails() }
            .testTag("trip_card_${trip.id}"),
        borderColor = GlassBorder,
        backgroundColor = BgDarkCard
    ) {
        Column {
            // Image Box
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(200.dp)
            ) {
                AsyncImage(
                    model = trip.imageUrl,
                    contentDescription = trip.name,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )

                // Gradient shadow
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(
                            Brush.verticalGradient(
                                listOf(Color(0x55000000), Color.Transparent, BgDarkCard)
                            )
                        )
                )

                // Top badges
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(14.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    VibeBadge(vibe = trip.vibe)

                    // Wishlist Button
                    Box(
                        modifier = Modifier
                            .size(36.dp)
                            .clip(CircleShape)
                            .background(Color(0x99080A0F))
                            .border(1.dp, GlassBorderStrong, CircleShape)
                            .clickable { onWishlistToggle() }
                            .testTag("wishlist_btn_${trip.id}"),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = if (isWishlisted) Icons.Default.Favorite else Icons.Default.FavoriteBorder,
                            contentDescription = "Save Trip",
                            tint = if (isWishlisted) GoldPrimary else TextSecondary,
                            modifier = Modifier.size(18.dp)
                        )
                    }
                }
            }

            // Body
            Column(
                modifier = Modifier.padding(18.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = trip.name,
                        style = MaterialTheme.typography.titleLarge.copy(
                            fontWeight = FontWeight.Bold,
                            color = TextPrimary,
                            fontSize = 22.sp
                        )
                    )

                    Text(
                        text = trip.duration,
                        style = MaterialTheme.typography.labelSmall.copy(
                            color = GoldSecondary,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 1.sp
                        )
                    )
                }

                Text(
                    text = trip.headline,
                    style = MaterialTheme.typography.bodyMedium.copy(
                        color = TextSecondary,
                        lineHeight = 19.sp
                    )
                )

                // Price Row
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 6.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column {
                        Text(
                            text = "ESTIMATED EXPENSE",
                            style = MaterialTheme.typography.labelSmall.copy(
                                color = TextTertiary,
                                fontSize = 9.sp
                            )
                        )
                        Text(
                            text = "${trip.price} / person",
                            style = MaterialTheme.typography.titleMedium.copy(
                                color = GoldPrimary,
                                fontWeight = FontWeight.ExtraBold
                            )
                        )
                    }

                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Button(
                            onClick = onStartGuide,
                            colors = ButtonDefaults.buttonColors(
                                containerColor = Color(0x22E8C97A),
                                contentColor = GoldPrimary
                            ),
                            shape = RoundedCornerShape(100.dp),
                            modifier = Modifier
                                .height(38.dp)
                                .border(1.dp, GlassBorderGold, RoundedCornerShape(100.dp))
                        ) {
                            Text("Guide 🧭", style = MaterialTheme.typography.labelSmall)
                        }

                        Button(
                            onClick = onViewDetails,
                            colors = ButtonDefaults.buttonColors(
                                containerColor = GoldPrimary,
                                contentColor = BgDark
                            ),
                            shape = RoundedCornerShape(100.dp),
                            modifier = Modifier.height(38.dp)
                        ) {
                            Text("View Plan →", style = MaterialTheme.typography.labelSmall.copy(fontWeight = FontWeight.Bold))
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun DestinationSpotlightsSection(
    spotlights: List<DestinationSpotlight>,
    onSpotlightClick: (DestinationSpotlight) -> Unit,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier, verticalArrangement = Arrangement.spacedBy(14.dp)) {
        GoldPillBadge(text = "Where I've Been")

        Text(
            text = "Documented. Not imagined.",
            style = MaterialTheme.typography.headlineMedium.copy(
                fontWeight = FontWeight.Bold,
                color = TextPrimary
            )
        )

        spotlights.forEach { spot ->
            GlassCard(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { onSpotlightClick(spot) },
                borderColor = GlassBorder,
                backgroundColor = BgDarkCard
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(14.dp),
                    horizontalArrangement = Arrangement.spacedBy(14.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    AsyncImage(
                        model = spot.imageUrl,
                        contentDescription = spot.title,
                        contentScale = ContentScale.Crop,
                        modifier = Modifier
                            .size(76.dp)
                            .clip(RoundedCornerShape(12.dp))
                    )

                    Column(modifier = Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(3.dp)) {
                        Text(
                            text = spot.region.uppercase(),
                            style = MaterialTheme.typography.labelSmall.copy(
                                color = GoldPrimary,
                                fontSize = 8.sp,
                                letterSpacing = 1.sp
                            )
                        )
                        Text(
                            text = spot.title,
                            style = MaterialTheme.typography.titleMedium.copy(
                                fontWeight = FontWeight.Bold,
                                color = TextPrimary
                            )
                        )
                        Text(
                            text = spot.documentedSpotsCount,
                            style = MaterialTheme.typography.bodyMedium.copy(
                                color = TextSecondary,
                                fontSize = 12.sp
                            )
                        )
                    }

                    Icon(
                        imageVector = Icons.Default.ArrowForward,
                        contentDescription = null,
                        tint = GoldPrimary,
                        modifier = Modifier.size(18.dp)
                    )
                }
            }
        }
    }
}

@Composable
fun WhyUsSection(modifier: Modifier = Modifier) {
    val items = listOf(
        Triple("📍", "Creator-Verified Routes", "Every destination has real video proof from my channel. Watch where you're going before you book."),
        Triple("🍛", "Food-Led Everything", "@beyondbenaglurufoods powers every food stop. Years of real local research — zero paid placements."),
        Triple("🧭", "Off the Beaten Path", "If it's on TripAdvisor's generic front page, I'm probably not taking you there. We go deeper."),
        Triple("⚡", "Zero Agency BS", "No 40-page PDF brochures. No 48hr turnaround. Direct WhatsApp & real human conversation.")
    )

    Column(modifier = modifier, verticalArrangement = Arrangement.spacedBy(14.dp)) {
        GoldPillBadge(text = "Why Us")

        Text(
            text = "Planning trips with a friend, not an agency.",
            style = MaterialTheme.typography.headlineMedium.copy(
                fontWeight = FontWeight.Bold,
                color = TextPrimary
            )
        )

        items.forEach { (emoji, title, desc) ->
            GlassCard(
                modifier = Modifier.fillMaxWidth(),
                borderColor = GlassBorder,
                backgroundColor = BgDarkCard
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(18.dp),
                    horizontalArrangement = Arrangement.spacedBy(14.dp),
                    verticalAlignment = Alignment.Top
                ) {
                    Text(text = emoji, fontSize = 24.sp)
                    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                        Text(
                            text = title,
                            style = MaterialTheme.typography.titleMedium.copy(
                                fontWeight = FontWeight.Bold,
                                color = TextPrimary
                            )
                        )
                        Text(
                            text = desc,
                            style = MaterialTheme.typography.bodyMedium.copy(
                                color = TextSecondary,
                                lineHeight = 19.sp
                            )
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun TravelerReviewsSection(
    reviews: List<com.example.data.model.TravelerReview>,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier, verticalArrangement = Arrangement.spacedBy(14.dp)) {
        GoldPillBadge(text = "Real People. Real Trips.")

        Text(
            text = "They went. They loved it.",
            style = MaterialTheme.typography.headlineMedium.copy(
                fontWeight = FontWeight.Bold,
                color = TextPrimary
            )
        )

        reviews.forEach { review ->
            GlassCard(
                modifier = Modifier.fillMaxWidth(),
                borderColor = GlassBorder,
                backgroundColor = BgDarkCard
            ) {
                Column(
                    modifier = Modifier.padding(18.dp),
                    verticalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(10.dp)
                        ) {
                            Box(
                                modifier = Modifier
                                    .size(34.dp)
                                    .clip(CircleShape)
                                    .background(GoldContainer),
                                contentAlignment = Alignment.Center
                            ) {
                                Text(
                                    text = review.authorHandle.take(2).uppercase().replace("@", ""),
                                    style = MaterialTheme.typography.labelSmall.copy(
                                        color = GoldPrimary,
                                        fontWeight = FontWeight.Bold
                                    )
                                )
                            }
                            Column {
                                Text(
                                    text = review.authorHandle,
                                    style = MaterialTheme.typography.labelMedium.copy(
                                        color = TextPrimary,
                                        fontWeight = FontWeight.Bold
                                    )
                                )
                                Text(
                                    text = review.city,
                                    style = MaterialTheme.typography.labelSmall.copy(color = TextTertiary)
                                )
                            }
                        }

                        RatingStars(rating = review.rating)
                    }

                    Text(
                        text = "“${review.reviewQuote}”",
                        style = MaterialTheme.typography.bodyMedium.copy(
                            fontStyle = FontStyle.Italic,
                            color = TextPrimary,
                            lineHeight = 20.sp
                        )
                    )

                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(100.dp))
                            .background(GlassSurface)
                            .padding(horizontal = 10.dp, vertical = 4.dp)
                    ) {
                        Text(
                            text = review.tripTag,
                            style = MaterialTheme.typography.labelSmall.copy(color = TextSecondary)
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun CtaBandSection(
    onPlanTrip: () -> Unit,
    onWhatsAppClick: () -> Unit,
    onCallClick: () -> Unit,
    onEmailClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    GlassCard(
        modifier = modifier.fillMaxWidth(),
        borderColor = GlassBorderGold,
        backgroundColor = Color(0xFF141926)
    ) {
        Column(
            modifier = Modifier.padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            GoldPillBadge(text = "Direct Creator Access")

            Text(
                text = "Let's go somewhere real.",
                style = MaterialTheme.typography.headlineMedium.copy(
                    fontWeight = FontWeight.Bold,
                    color = TextPrimary
                )
            )

            Text(
                text = "No brochure. No BS. Directly reach out on WhatsApp, Phone or Email to plan your personalized route.",
                style = MaterialTheme.typography.bodyMedium.copy(
                    color = TextSecondary,
                    textAlign = androidx.compose.ui.text.style.TextAlign.Center
                )
            )

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                GoldButton(
                    text = "Plan My Trip",
                    onClick = onPlanTrip,
                    modifier = Modifier.weight(1f)
                )

                Button(
                    onClick = onWhatsAppClick,
                    colors = ButtonDefaults.buttonColors(
                        containerColor = GlassSurface,
                        contentColor = TextPrimary
                    ),
                    shape = RoundedCornerShape(100.dp),
                    modifier = Modifier
                        .height(48.dp)
                        .border(1.dp, GlassBorderStrong, RoundedCornerShape(100.dp))
                ) {
                    Text("WhatsApp 💬")
                }
            }

            // Direct Call & Email quick row
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                Button(
                    onClick = onCallClick,
                    colors = ButtonDefaults.buttonColors(
                        containerColor = GlassSurface,
                        contentColor = TextPrimary
                    ),
                    shape = RoundedCornerShape(100.dp),
                    modifier = Modifier
                        .weight(1f)
                        .height(40.dp)
                        .border(1.dp, GlassBorder, RoundedCornerShape(100.dp))
                ) {
                    Text("📞 +91 9742311023", style = MaterialTheme.typography.labelSmall.copy(color = GoldPrimary, fontWeight = FontWeight.Bold))
                }

                Button(
                    onClick = onEmailClick,
                    colors = ButtonDefaults.buttonColors(
                        containerColor = GlassSurface,
                        contentColor = TextPrimary
                    ),
                    shape = RoundedCornerShape(100.dp),
                    modifier = Modifier
                        .weight(1f)
                        .height(40.dp)
                        .border(1.dp, GlassBorder, RoundedCornerShape(100.dp))
                ) {
                    Text("✉️ Email Us", style = MaterialTheme.typography.labelSmall.copy(color = TextPrimary))
                }
            }
        }
    }
}

@Composable
fun FooterSection(
    email: String,
    onEmailChange: (String) -> Unit,
    onSubscribe: () -> Unit,
    onInstagramClick: () -> Unit,
    onYouTubeClick: () -> Unit,
    onWhatsAppClick: () -> Unit,
    onCallClick: () -> Unit,
    onEmailClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier, verticalArrangement = Arrangement.spacedBy(16.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Text(
                text = "COMETRIPWITHME",
                style = MaterialTheme.typography.titleLarge.copy(
                    fontWeight = FontWeight.ExtraBold,
                    color = GoldPrimary,
                    letterSpacing = 1.sp
                )
            )
        }

        Text(
            text = "India's first creator-led tour operator. Real trips, real places — curated with verified route proof. Based in Bengaluru ☕.",
            style = MaterialTheme.typography.bodyMedium.copy(color = TextSecondary)
        )

        // Contact info pill box
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(12.dp))
                .background(GlassSurface)
                .border(1.dp, GlassBorder, RoundedCornerShape(12.dp))
                .padding(14.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { onCallClick() },
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Text("📞", fontSize = 14.sp)
                Text(
                    text = "+91 97423 11023",
                    style = MaterialTheme.typography.bodyMedium.copy(color = GoldPrimary, fontWeight = FontWeight.Bold)
                )
                Text(
                    text = "(Tap to Call / WhatsApp)",
                    style = MaterialTheme.typography.labelSmall.copy(color = TextTertiary, fontSize = 10.sp)
                )
            }

            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { onEmailClick() },
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Text("✉️", fontSize = 14.sp)
                Text(
                    text = "bengalurufoodss@gmail.com",
                    style = MaterialTheme.typography.bodyMedium.copy(color = TextPrimary)
                )
            }
        }

        // Newsletter input
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            OutlinedTextField(
                value = email,
                onValueChange = onEmailChange,
                placeholder = { Text("your@email.com", color = TextTertiary) },
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = GoldPrimary,
                    unfocusedBorderColor = GlassBorder,
                    focusedTextColor = TextPrimary,
                    unfocusedTextColor = TextPrimary
                ),
                modifier = Modifier.weight(1f)
            )

            Button(
                onClick = onSubscribe,
                colors = ButtonDefaults.buttonColors(
                    containerColor = GoldPrimary,
                    contentColor = BgDark
                ),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier.height(56.dp)
            ) {
                Text("Join ✦", style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.Bold))
            }
        }

        // Social handles
        Row(
            modifier = Modifier.horizontalScroll(rememberScrollState()),
            horizontalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            SocialChip(iconText = "📸", label = "@cometriipwme", onClick = onInstagramClick)
            SocialChip(iconText = "▶", label = "YouTube", onClick = onYouTubeClick)
            SocialChip(iconText = "💬", label = "WhatsApp", onClick = onWhatsAppClick)
            SocialChip(iconText = "📞", label = "Call", onClick = onCallClick)
            SocialChip(iconText = "✉️", label = "Email", onClick = onEmailClick)
        }

        Text(
            text = "© 2025 ComeTripWithMe · Handcrafted in Bengaluru",
            style = MaterialTheme.typography.labelSmall.copy(color = TextTertiary, fontSize = 10.sp)
        )
    }
}

@Composable
fun SocialChip(iconText: String, label: String, onClick: () -> Unit) {
    Row(
        modifier = Modifier
            .clip(RoundedCornerShape(100.dp))
            .background(GlassSurface)
            .border(1.dp, GlassBorder, RoundedCornerShape(100.dp))
            .clickable { onClick() }
            .padding(horizontal = 12.dp, vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        Text(text = iconText, fontSize = 12.sp)
        Text(text = label, style = MaterialTheme.typography.labelSmall.copy(color = TextSecondary))
    }
}
