package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
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
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowForward
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.ConfirmationNumber
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.Navigation
import androidx.compose.material.icons.filled.QrCode
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.example.ui.components.GlassCard
import com.example.ui.components.GoldButton
import com.example.ui.components.GoldPillBadge
import com.example.ui.components.LiveStatusBadge
import com.example.ui.theme.AccentEmerald
import com.example.ui.theme.AccentGreen
import com.example.ui.theme.AccentRed
import com.example.ui.theme.BgDark
import com.example.ui.theme.BgDarkCard
import com.example.ui.theme.BgDarkElevated
import com.example.ui.theme.GlassBorder
import com.example.ui.theme.GlassBorderGold
import com.example.ui.theme.GlassSurface
import com.example.ui.theme.GoldPrimary
import com.example.ui.theme.GoldSecondary
import com.example.ui.theme.TextMuted
import com.example.ui.theme.TextPrimary
import com.example.ui.theme.TextSecondary
import com.example.ui.theme.TextTertiary
import com.example.ui.viewmodel.AppTab
import com.example.ui.viewmodel.MainViewModel

@Composable
fun SavedTripsScreen(
    viewModel: MainViewModel,
    modifier: Modifier = Modifier
) {
    val wishlist by viewModel.wishlist.collectAsState()
    val activeTrip by viewModel.activeGuideTrip.collectAsState()
    val roomItineraries by viewModel.roomItineraries.collectAsState()
    val vouchers by viewModel.activeVouchers.collectAsState()
    val allTrips = viewModel.getAllTrips()

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .background(BgDark)
            .padding(horizontal = 16.dp)
            .testTag("saved_trips_screen"),
        verticalArrangement = Arrangement.spacedBy(18.dp)
    ) {
        // 1. Header
        item {
            Spacer(modifier = Modifier.height(10.dp))
            GoldPillBadge(text = "My Travel Vault & Passes")
            Spacer(modifier = Modifier.height(6.dp))
            Text(
                text = "Saved Vault & Passes",
                style = MaterialTheme.typography.headlineLarge.copy(
                    fontWeight = FontWeight.ExtraBold,
                    color = TextPrimary
                )
            )
            Spacer(modifier = Modifier.height(2.dp))
            Text(
                text = "Your confirmed booking vouchers, saved Room itineraries, and live companion.",
                style = MaterialTheme.typography.bodyMedium.copy(color = TextSecondary)
            )
        }

        // 2. Confirmed Vouchers Section
        if (vouchers.isNotEmpty()) {
            item {
                Text(
                    text = "CONFIRMED PASSES & VOUCHERS (${vouchers.size})",
                    style = MaterialTheme.typography.labelSmall.copy(
                        color = GoldPrimary,
                        letterSpacing = 1.2.sp,
                        fontWeight = FontWeight.Bold
                    )
                )
            }

            items(vouchers, key = { it.voucherId }) { voucher ->
                GlassCard(
                    borderColor = GoldPrimary,
                    backgroundColor = BgDarkElevated
                ) {
                    Column(
                        modifier = Modifier.padding(14.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(Icons.Default.ConfirmationNumber, contentDescription = null, tint = GoldPrimary, modifier = Modifier.size(16.dp))
                                Spacer(modifier = Modifier.width(6.dp))
                                Text(
                                    text = voucher.voucherId,
                                    style = MaterialTheme.typography.labelMedium,
                                    fontWeight = FontWeight.Bold,
                                    color = GoldPrimary
                                )
                            }
                            Text(
                                text = "CONFIRMED ✓",
                                style = MaterialTheme.typography.labelSmall,
                                color = AccentEmerald,
                                fontWeight = FontWeight.Bold
                            )
                        }

                        Text(
                            text = voucher.tripTitle,
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold,
                            color = TextPrimary
                        )

                        Text(
                            text = "${voucher.durationText} · Date: ${voucher.travelDate} · ${voucher.travelerTier} (${voucher.groupCount} travelers)",
                            style = MaterialTheme.typography.bodySmall,
                            color = TextSecondary
                        )

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                text = "Total: ${voucher.totalAmountPaid}",
                                style = MaterialTheme.typography.bodyMedium,
                                fontWeight = FontWeight.Bold,
                                color = GoldPrimary
                            )

                            Button(
                                onClick = { viewModel.openWhatsAppForBooking(voucher) },
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF25D366)),
                                shape = RoundedCornerShape(8.dp),
                                modifier = Modifier.height(36.dp)
                            ) {
                                Icon(Icons.Default.Send, contentDescription = null, tint = Color.White, modifier = Modifier.size(14.dp))
                                Spacer(modifier = Modifier.width(4.dp))
                                Text("WhatsApp", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
            }
        }

        // 3. Active Trip Companion Widget
        item {
            GlassCard(
                borderColor = GlassBorderGold,
                backgroundColor = Color(0x1FE8C97A)
            ) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        LiveStatusBadge(label = "ACTIVE ONGOING TRIP")
                        Text(
                            text = activeTrip.duration,
                            style = MaterialTheme.typography.labelSmall.copy(color = GoldSecondary)
                        )
                    }

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(12.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        AsyncImage(
                            model = activeTrip.imageUrl,
                            contentDescription = activeTrip.name,
                            contentScale = ContentScale.Crop,
                            modifier = Modifier
                                .size(60.dp)
                                .clip(RoundedCornerShape(10.dp))
                        )

                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                text = activeTrip.name,
                                style = MaterialTheme.typography.titleMedium.copy(
                                    fontWeight = FontWeight.Bold,
                                    color = TextPrimary
                                )
                            )
                            Text(
                                text = "Live pocket guide, audio stories & packing checklist ready",
                                style = MaterialTheme.typography.bodySmall.copy(
                                    color = TextSecondary,
                                    fontSize = 11.sp
                                )
                            )
                        }
                    }

                    GoldButton(
                        text = "Resume Live Pocket Guide 🧭",
                        onClick = { viewModel.setTab(AppTab.POCKET_GUIDE) },
                        modifier = Modifier.fillMaxWidth(),
                        testTag = "resume_guide_btn"
                    )
                }
            }
        }

        // 4. Room Saved Custom Itineraries
        if (roomItineraries.isNotEmpty()) {
            item {
                Text(
                    text = "SAVED ROOM ITINERARIES & SPOTS (${roomItineraries.size})",
                    style = MaterialTheme.typography.labelSmall.copy(
                        color = TextTertiary,
                        letterSpacing = 1.2.sp,
                        fontWeight = FontWeight.Bold
                    )
                )
            }

            items(roomItineraries, key = { it.itinerary.itineraryId }) { itemWithSpots ->
                val it = itemWithSpots.itinerary
                GlassCard(
                    borderColor = GlassBorder,
                    backgroundColor = BgDarkCard
                ) {
                    Column(
                        modifier = Modifier.padding(14.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                text = it.destinationName,
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.Bold,
                                color = GoldPrimary
                            )
                            GoldPillBadge(text = it.duration)
                        }

                        Text(
                            text = it.title,
                            style = MaterialTheme.typography.bodyMedium,
                            fontWeight = FontWeight.SemiBold,
                            color = TextPrimary
                        )

                        Text(
                            text = it.tagline,
                            style = MaterialTheme.typography.bodySmall,
                            color = TextSecondary
                        )

                        if (itemWithSpots.spotRecommendations.isNotEmpty()) {
                            HorizontalDivider(color = GlassBorder)
                            Text(
                                text = "📍 ${itemWithSpots.spotRecommendations.size} Curated Hidden Spots:",
                                style = MaterialTheme.typography.labelSmall,
                                color = GoldSecondary
                            )
                            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                                itemWithSpots.spotRecommendations.take(3).forEach { spot ->
                                    Text(
                                        text = "• ${spot.spotName} — ${spot.mustTryItem}",
                                        style = MaterialTheme.typography.bodySmall,
                                        color = TextMuted,
                                        fontSize = 11.sp
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }

        // 5. Wishlist Section
        item {
            Text(
                text = "SAVED WISHLIST (${wishlist.size})",
                style = MaterialTheme.typography.labelSmall.copy(
                    color = TextTertiary,
                    letterSpacing = 1.2.sp,
                    fontWeight = FontWeight.Bold
                )
            )
        }

        if (wishlist.isEmpty()) {
            item {
                GlassCard(
                    borderColor = GlassBorder,
                    backgroundColor = BgDarkCard
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(28.dp),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Text(text = "🗺️", fontSize = 32.sp)
                        Text(
                            text = "No saved trips yet",
                            style = MaterialTheme.typography.titleMedium.copy(
                                fontWeight = FontWeight.Bold,
                                color = TextPrimary
                            )
                        )
                        Text(
                            text = "Hit the ♡ icon on any itinerary in the Explore tab to save it here.",
                            style = MaterialTheme.typography.bodyMedium.copy(
                                color = TextSecondary,
                                textAlign = androidx.compose.ui.text.style.TextAlign.Center,
                                fontSize = 12.sp
                            )
                        )
                        Spacer(modifier = Modifier.height(4.dp))
                        GoldButton(
                            text = "Explore Itineraries",
                            onClick = { viewModel.setTab(AppTab.EXPLORE) }
                        )
                    }
                }
            }
        } else {
            items(wishlist) { wish ->
                val fullTrip = allTrips.find { it.id == wish.tripId }

                GlassCard(
                    borderColor = GlassBorder,
                    backgroundColor = BgDarkCard,
                    modifier = Modifier.clickable {
                        fullTrip?.let { viewModel.selectTrip(it) }
                    }
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(12.dp),
                        horizontalArrangement = Arrangement.spacedBy(12.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        AsyncImage(
                            model = wish.imageUrl,
                            contentDescription = wish.name,
                            contentScale = ContentScale.Crop,
                            modifier = Modifier
                                .size(60.dp)
                                .clip(RoundedCornerShape(10.dp))
                        )

                        Column(modifier = Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(2.dp)) {
                            Text(
                                text = wish.name,
                                style = MaterialTheme.typography.titleMedium.copy(
                                    fontWeight = FontWeight.Bold,
                                    color = TextPrimary
                                )
                            )
                            Text(
                                text = "${wish.duration} · ${wish.vibe}",
                                style = MaterialTheme.typography.bodyMedium.copy(
                                    color = TextSecondary,
                                    fontSize = 11.sp
                                )
                            )
                            Text(
                                text = wish.price,
                                style = MaterialTheme.typography.labelMedium.copy(
                                    color = GoldPrimary,
                                    fontWeight = FontWeight.Bold
                                )
                            )
                        }

                        IconButton(
                            onClick = {
                                fullTrip?.let { viewModel.toggleWishlist(it) }
                            },
                            modifier = Modifier.size(36.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Default.Delete,
                                contentDescription = "Remove",
                                tint = TextMuted,
                                modifier = Modifier.size(18.dp)
                            )
                        }
                    }
                }
            }
        }

        item {
            Spacer(modifier = Modifier.height(40.dp))
        }
    }
}
