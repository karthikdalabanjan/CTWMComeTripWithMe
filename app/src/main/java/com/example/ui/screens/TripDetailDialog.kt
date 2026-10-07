package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.FavoriteBorder
import androidx.compose.material.icons.filled.Headphones
import androidx.compose.material.icons.filled.LocationOn
import androidx.compose.material.icons.filled.Navigation
import androidx.compose.material.icons.filled.Restaurant
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
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
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import coil.compose.AsyncImage
import com.example.data.model.DayPlan
import com.example.data.model.Trip
import com.example.ui.components.GlassCard
import com.example.ui.components.GoldButton
import com.example.ui.components.GoldPillBadge
import com.example.ui.components.VibeBadge
import com.example.ui.theme.AccentGreen
import com.example.ui.theme.BgDark
import com.example.ui.theme.BgDarkCard
import com.example.ui.theme.BgDarkElevated
import com.example.ui.theme.GlassBorder
import com.example.ui.theme.GlassBorderGold
import com.example.ui.theme.GlassBorderStrong
import com.example.ui.theme.GlassSurface
import com.example.ui.theme.GoldContainer
import com.example.ui.theme.GoldPrimary
import com.example.ui.theme.GoldSecondary
import com.example.ui.theme.TextMuted
import com.example.ui.theme.TextPrimary
import com.example.ui.theme.TextSecondary
import com.example.ui.theme.TextTertiary
import com.example.ui.viewmodel.MainViewModel

@Composable
fun TripDetailDialog(
    trip: Trip,
    viewModel: MainViewModel,
    onDismiss: () -> Unit
) {
    val wishlist by viewModel.wishlist.collectAsState()
    val isWishlisted = wishlist.any { it.tripId == trip.id }

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Surface(
            modifier = Modifier
                .fillMaxSize()
                .background(BgDark)
                .testTag("trip_detail_dialog"),
            color = BgDark
        ) {
            Box(modifier = Modifier.fillMaxSize()) {
                LazyColumn(
                    modifier = Modifier.fillMaxSize(),
                    verticalArrangement = Arrangement.spacedBy(20.dp)
                ) {
                    // 1. Hero Header
                    item {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(320.dp)
                        ) {
                            AsyncImage(
                                model = trip.imageUrl,
                                contentDescription = trip.name,
                                contentScale = ContentScale.Crop,
                                modifier = Modifier.fillMaxSize()
                            )

                            Box(
                                modifier = Modifier
                                    .fillMaxSize()
                                    .background(
                                        Brush.verticalGradient(
                                            colors = listOf(
                                                Color(0x66080A0F),
                                                Color(0xAA080A0F),
                                                BgDark
                                            )
                                        )
                                    )
                            )

                            // Top Action bar
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(horizontal = 20.dp, vertical = 20.dp),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Box(
                                    modifier = Modifier
                                        .size(42.dp)
                                        .clip(CircleShape)
                                        .background(Color(0x99080A0F))
                                        .border(1.dp, GlassBorderStrong, CircleShape)
                                        .clickable { onDismiss() }
                                        .testTag("close_detail_btn"),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.Close,
                                        contentDescription = "Close",
                                        tint = TextPrimary
                                    )
                                }

                                Box(
                                    modifier = Modifier
                                        .size(42.dp)
                                        .clip(CircleShape)
                                        .background(Color(0x99080A0F))
                                        .border(1.dp, GlassBorderStrong, CircleShape)
                                        .clickable { viewModel.toggleWishlist(trip) }
                                        .testTag("toggle_wishlist_detail_btn"),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Icon(
                                        imageVector = if (isWishlisted) Icons.Default.Favorite else Icons.Default.FavoriteBorder,
                                        contentDescription = "Wishlist",
                                        tint = if (isWishlisted) GoldPrimary else TextSecondary
                                    )
                                }
                            }

                            // Hero Bottom Content
                            Column(
                                modifier = Modifier
                                    .align(Alignment.BottomStart)
                                    .padding(20.dp),
                                verticalArrangement = Arrangement.spacedBy(8.dp)
                            ) {
                                Row(
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                                ) {
                                    VibeBadge(vibe = trip.vibe)
                                    GoldPillBadge(text = trip.duration)
                                }

                                Text(
                                    text = trip.name,
                                    style = MaterialTheme.typography.displayMedium.copy(
                                        fontWeight = FontWeight.ExtraBold,
                                        color = TextPrimary
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
                        }
                    }

                    // 2. Creator Note Card
                    item {
                        GlassCard(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(horizontal = 20.dp),
                            borderColor = GlassBorderGold,
                            backgroundColor = Color(0x1FE8C97A)
                        ) {
                            Column(
                                modifier = Modifier.padding(18.dp),
                                verticalArrangement = Arrangement.spacedBy(8.dp)
                            ) {
                                Row(
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                                ) {
                                    Text(text = "✍️", fontSize = 16.sp)
                                    Text(
                                        text = "CREATOR INTEL & BACKSTORY",
                                        style = MaterialTheme.typography.labelSmall.copy(
                                            color = GoldPrimary,
                                            fontWeight = FontWeight.Bold,
                                            letterSpacing = 1.sp
                                        )
                                    )
                                }
                                Text(
                                    text = "“${trip.creatorNote}”",
                                    style = MaterialTheme.typography.bodyLarge.copy(
                                        fontStyle = FontStyle.Italic,
                                        color = TextPrimary,
                                        lineHeight = 22.sp
                                    )
                                )
                            }
                        }
                    }

                    // 3. Day-By-Day Breakdown Header
                    item {
                        Column(
                            modifier = Modifier.padding(horizontal = 20.dp),
                            verticalArrangement = Arrangement.spacedBy(4.dp)
                        ) {
                            GoldPillBadge(text = "Day-By-Day Breakdown")
                            Text(
                                text = "The Exact Route",
                                style = MaterialTheme.typography.headlineSmall.copy(
                                    fontWeight = FontWeight.Bold,
                                    color = TextPrimary
                                )
                            )
                        }
                    }

                    // 4. Day Plans
                    itemsIndexed(trip.days) { index, day ->
                        DayPlanCard(
                            day = day,
                            onWatchReel = { reelUrl -> viewModel.openReel(reelUrl) },
                            modifier = Modifier.padding(horizontal = 20.dp)
                        )
                    }

                    // 5. Total Estimate Breakdown & Booking Info
                    item {
                        GlassCard(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(horizontal = 20.dp),
                            borderColor = GlassBorder,
                            backgroundColor = BgDarkCard
                        ) {
                            Column(
                                modifier = Modifier.padding(20.dp),
                                verticalArrangement = Arrangement.spacedBy(10.dp)
                            ) {
                                Text(
                                    text = "ESTIMATED BUDGET BREAKDOWN",
                                    style = MaterialTheme.typography.labelSmall.copy(
                                        color = GoldPrimary,
                                        letterSpacing = 1.sp,
                                        fontWeight = FontWeight.Bold
                                    )
                                )
                                Text(
                                    text = trip.totalEstimateDetails,
                                    style = MaterialTheme.typography.bodyMedium.copy(
                                        color = TextPrimary,
                                        lineHeight = 20.sp
                                    )
                                )
                                Text(
                                    text = "✦ No hidden markups. We share direct local vendor contacts and verified routes.",
                                    style = MaterialTheme.typography.bodyMedium.copy(
                                        color = TextTertiary,
                                        fontSize = 12.sp
                                    )
                                )
                            }
                        }
                    }

                    // Padding for bottom action bar
                    item {
                        Spacer(modifier = Modifier.height(80.dp))
                    }
                }

                // Fixed Bottom Action Bar
                Row(
                    modifier = Modifier
                        .align(Alignment.BottomCenter)
                        .fillMaxWidth()
                        .background(BgDarkElevated.copy(alpha = 0.95f))
                        .border(1.dp, GlassBorder, RoundedCornerShape(topStart = 20.dp, topEnd = 20.dp))
                        .padding(horizontal = 20.dp, vertical = 14.dp),
                    horizontalArrangement = Arrangement.spacedBy(10.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    // Start live companion guide
                    Button(
                        onClick = {
                            viewModel.startLivePocketGuide(trip)
                            onDismiss()
                        },
                        colors = ButtonDefaults.buttonColors(
                            containerColor = Color(0x22E8C97A),
                            contentColor = GoldPrimary
                        ),
                        shape = RoundedCornerShape(100.dp),
                        modifier = Modifier
                            .weight(1f)
                            .height(48.dp)
                            .border(1.dp, GlassBorderGold, RoundedCornerShape(100.dp))
                            .testTag("launch_pocket_guide_btn")
                    ) {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(6.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Default.Navigation,
                                contentDescription = null,
                                modifier = Modifier.size(16.dp),
                                tint = GoldPrimary
                            )
                            Text(
                                text = "POCKET GUIDE",
                                style = MaterialTheme.typography.labelSmall.copy(fontWeight = FontWeight.Bold)
                            )
                        }
                    }

                    // Book via WhatsApp
                    GoldButton(
                        text = "Book Trip ✦",
                        onClick = {
                            viewModel.openWhatsApp("Hey ComeTripWithMe! I want to book the ${trip.name} (${trip.duration}) trip.")
                            onDismiss()
                        },
                        modifier = Modifier.weight(1f),
                        testTag = "book_trip_btn"
                    )
                }
            }
        }
    }
}

@Composable
fun DayPlanCard(
    day: DayPlan,
    onWatchReel: (String) -> Unit = {},
    modifier: Modifier = Modifier
) {
    GlassCard(
        modifier = modifier.fillMaxWidth(),
        borderColor = GlassBorder,
        backgroundColor = BgDarkCard
    ) {
        Column(
            modifier = Modifier.padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            // Day Header
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                Box(
                    modifier = Modifier
                        .size(32.dp)
                        .clip(CircleShape)
                        .background(GoldPrimary),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = "${day.dayNumber}",
                        style = MaterialTheme.typography.labelMedium.copy(
                            color = BgDark,
                            fontWeight = FontWeight.ExtraBold
                        )
                    )
                }

                Column {
                    Text(
                        text = "DAY ${day.dayNumber}",
                        style = MaterialTheme.typography.labelSmall.copy(
                            color = GoldPrimary,
                            letterSpacing = 1.sp,
                            fontWeight = FontWeight.Bold
                        )
                    )
                    Text(
                        text = day.title,
                        style = MaterialTheme.typography.titleMedium.copy(
                            fontWeight = FontWeight.Bold,
                            color = TextPrimary
                        )
                    )
                }
            }

            Text(
                text = day.summary,
                style = MaterialTheme.typography.bodyMedium.copy(
                    color = TextSecondary,
                    lineHeight = 19.sp
                )
            )

            // Stops Timeline
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                day.stops.forEach { stop ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp))
                            .background(GlassSurface)
                            .padding(12.dp),
                        horizontalArrangement = Arrangement.spacedBy(10.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            imageVector = Icons.Default.LocationOn,
                            contentDescription = null,
                            tint = GoldPrimary,
                            modifier = Modifier.size(18.dp)
                        )
                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                text = stop.name,
                                style = MaterialTheme.typography.labelLarge.copy(
                                    color = TextPrimary,
                                    fontWeight = FontWeight.Bold
                                )
                            )
                            Text(
                                text = stop.category,
                                style = MaterialTheme.typography.labelSmall.copy(color = TextTertiary)
                            )
                        }
                        Text(
                            text = stop.timing,
                            style = MaterialTheme.typography.labelSmall.copy(
                                color = GoldSecondary,
                                fontWeight = FontWeight.SemiBold
                            )
                        )
                    }
                }
            }

            // Food Stops with Insta Reel previews
            if (day.foodSpots.isNotEmpty()) {
                Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        Text(
                            text = "🍜 FOOD & CAFÉ RECCOS",
                            style = MaterialTheme.typography.labelSmall.copy(
                                color = GoldPrimary,
                                fontSize = 9.sp,
                                fontWeight = FontWeight.Bold,
                                letterSpacing = 1.sp
                            )
                        )
                        Text(
                            text = "• by @beyondbengalurufoods",
                            style = MaterialTheme.typography.labelSmall.copy(
                                color = TextTertiary,
                                fontSize = 9.sp
                            )
                        )
                    }

                    day.foodSpots.forEach { food ->
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(12.dp))
                                .background(Color(0x2A1A1F2B))
                                .border(1.dp, GlassBorderGold, RoundedCornerShape(12.dp))
                                .clickable { onWatchReel(food.reelUrl) }
                                .padding(10.dp)
                        ) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.spacedBy(10.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                // Thumbnail with Reel badge
                                if (food.reelThumbnailUrl.isNotBlank()) {
                                    Box(
                                        modifier = Modifier
                                            .size(width = 72.dp, height = 72.dp)
                                            .clip(RoundedCornerShape(8.dp))
                                    ) {
                                        AsyncImage(
                                            model = food.reelThumbnailUrl,
                                            contentDescription = food.name,
                                            contentScale = ContentScale.Crop,
                                            modifier = Modifier.fillMaxSize()
                                        )
                                        Box(
                                            modifier = Modifier
                                                .fillMaxSize()
                                                .background(
                                                    Brush.verticalGradient(
                                                        listOf(Color.Transparent, Color(0x99000000))
                                                    )
                                                )
                                        )
                                        Box(
                                            modifier = Modifier
                                                .align(Alignment.BottomStart)
                                                .padding(3.dp)
                                                .clip(RoundedCornerShape(3.dp))
                                                .background(Color(0xCC000000))
                                                .padding(horizontal = 4.dp, vertical = 1.dp)
                                        ) {
                                            Text(
                                                text = "▶ Reel",
                                                style = MaterialTheme.typography.labelSmall.copy(
                                                    color = GoldPrimary,
                                                    fontSize = 8.sp,
                                                    fontWeight = FontWeight.Bold
                                                )
                                            )
                                        }
                                    }
                                }

                                Column(
                                    modifier = Modifier.weight(1f),
                                    verticalArrangement = Arrangement.spacedBy(2.dp)
                                ) {
                                    Text(
                                        text = food.name,
                                        style = MaterialTheme.typography.labelMedium.copy(
                                            color = TextPrimary,
                                            fontWeight = FontWeight.Bold
                                        ),
                                        maxLines = 1,
                                        overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
                                    )
                                    Text(
                                        text = food.specialty,
                                        style = MaterialTheme.typography.labelSmall.copy(
                                            color = TextTertiary,
                                            fontSize = 11.sp
                                        ),
                                        maxLines = 1,
                                        overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
                                    )
                                    Text(
                                        text = "Must order: ${food.mustTryDish}",
                                        style = MaterialTheme.typography.bodySmall.copy(
                                            color = GoldSecondary,
                                            fontSize = 11.sp,
                                            fontWeight = FontWeight.Medium
                                        ),
                                        maxLines = 1,
                                        overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
                                    )
                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween,
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Text(
                                            text = food.approxCostForTwo,
                                            style = MaterialTheme.typography.labelSmall.copy(
                                                color = TextTertiary,
                                                fontSize = 10.sp
                                            )
                                        )
                                        Text(
                                            text = "Watch Reel ↗",
                                            style = MaterialTheme.typography.labelSmall.copy(
                                                color = GoldPrimary,
                                                fontSize = 10.sp,
                                                fontWeight = FontWeight.Bold
                                            )
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
            }

            // Secret Tip
            if (day.creatorSecretTip.isNotBlank()) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(10.dp))
                        .background(Color(0x33000000))
                        .padding(10.dp)
                ) {
                    Text(
                        text = "💡 Secret Tip: ${day.creatorSecretTip}",
                        style = MaterialTheme.typography.bodyMedium.copy(
                            color = TextSecondary,
                            fontSize = 12.sp
                        )
                    )
                }
            }
        }
    }
}
