package com.example.ui.screens

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
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
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.CalendarMonth
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.ConfirmationNumber
import androidx.compose.material.icons.filled.Group
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Phone
import androidx.compose.material.icons.filled.QrCode
import androidx.compose.material.icons.filled.Remove
import androidx.compose.material.icons.filled.Send
import androidx.compose.material.icons.filled.VerifiedUser
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Divider
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Surface
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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import coil.compose.AsyncImage
import com.example.data.model.AVAILABLE_ADD_ONS
import com.example.data.model.TravelSeason
import com.example.data.model.TravelVoucher
import com.example.data.model.TravelerType
import com.example.data.model.Trip
import com.example.ui.components.GlassCard
import com.example.ui.components.GoldButton
import com.example.ui.components.GoldPillBadge
import com.example.ui.theme.AccentEmerald
import com.example.ui.theme.AccentRed
import com.example.ui.theme.BgDark
import com.example.ui.theme.BgDarkCard
import com.example.ui.theme.BgDarkElevated
import com.example.ui.theme.GlassBorder
import com.example.ui.theme.GlassBorderGold
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
fun BookingScreen(
    viewModel: MainViewModel,
    modifier: Modifier = Modifier
) {
    val allTrips = viewModel.getAllTrips()
    val selectedTripId by viewModel.selectedBookingTripId.collectAsState()
    val selectedTravelerType by viewModel.selectedTravelerType.collectAsState()
    val groupSize by viewModel.selectedGroupSize.collectAsState()
    val season by viewModel.selectedTravelSeason.collectAsState()
    val selectedAddOns by viewModel.selectedAddOnIds.collectAsState()

    val contactName by viewModel.bookingContactName.collectAsState()
    val contactPhone by viewModel.bookingContactPhone.collectAsState()
    val contactEmail by viewModel.bookingContactEmail.collectAsState()
    val travelDate by viewModel.bookingTravelDate.collectAsState()
    val specialNotes by viewModel.bookingSpecialNotes.collectAsState()

    val activeVoucherModal by viewModel.selectedVoucherForModal.collectAsState()

    val currentTrip = allTrips.find { it.id == selectedTripId } ?: allTrips.first()
    val pricing = viewModel.calculateCurrentBookingPricing()

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = 16.dp),
        verticalArrangement = Arrangement.spacedBy(18.dp)
    ) {
        item { Spacer(modifier = Modifier.height(6.dp)) }

        // Section Title
        item {
            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        text = "Book Curated Itineraries",
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.Bold,
                        color = TextPrimary
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    GoldPillBadge(text = "Zero Markup ✦")
                }
                Text(
                    text = "Transparent dynamic pricing calculated for every traveler group, stay style & transport setup.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = TextSecondary
                )
            }
        }

        // 1. SELECT EXISTING ITINERARY
        item {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text(
                    text = "1. CHOOSE ITINERARY",
                    style = MaterialTheme.typography.labelMedium,
                    fontWeight = FontWeight.Bold,
                    color = GoldPrimary,
                    letterSpacing = 1.sp
                )

                val scrollState = rememberScrollState()
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .horizontalScroll(scrollState),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    allTrips.forEach { trip ->
                        val isSelected = trip.id == selectedTripId
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(12.dp))
                                .background(if (isSelected) GoldContainer else GlassSurface)
                                .border(
                                    1.dp,
                                    if (isSelected) GoldPrimary else GlassBorder,
                                    RoundedCornerShape(12.dp)
                                )
                                .clickable { viewModel.setBookingTrip(trip.id) }
                                .padding(horizontal = 14.dp, vertical = 10.dp)
                        ) {
                            Column {
                                Text(
                                    text = trip.name,
                                    style = MaterialTheme.typography.titleSmall,
                                    fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Medium,
                                    color = if (isSelected) GoldPrimary else TextPrimary
                                )
                                Text(
                                    text = "${trip.duration} · ${trip.price}",
                                    style = MaterialTheme.typography.bodySmall,
                                    color = if (isSelected) TextSecondary else TextMuted
                                )
                            }
                        }
                    }
                }
            }
        }

        // Trip Preview Card
        item {
            GlassCard(
                modifier = Modifier.fillMaxWidth(),
                borderColor = GlassBorderGold
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(12.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    AsyncImage(
                        model = currentTrip.imageUrl,
                        contentDescription = currentTrip.name,
                        modifier = Modifier
                            .size(80.dp)
                            .clip(RoundedCornerShape(10.dp)),
                        contentScale = ContentScale.Crop
                    )
                    Column(
                        modifier = Modifier.weight(1f),
                        verticalArrangement = Arrangement.spacedBy(4.dp)
                    ) {
                        Text(
                            text = currentTrip.name,
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold,
                            color = TextPrimary
                        )
                        Text(
                            text = currentTrip.headline,
                            style = MaterialTheme.typography.bodySmall,
                            color = TextSecondary,
                            maxLines = 2
                        )
                        Row(
                            horizontalArrangement = Arrangement.spacedBy(8.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                text = "Base: ₹${String.format("%,d", currentTrip.budgetValue)}",
                                style = MaterialTheme.typography.bodySmall,
                                color = GoldPrimary,
                                fontWeight = FontWeight.SemiBold
                            )
                            Text(
                                text = "•  ${currentTrip.duration}",
                                style = MaterialTheme.typography.bodySmall,
                                color = TextMuted
                            )
                        }
                    }
                }
            }
        }

        // 2. TRAVELER TYPE & GROUP SETUP
        item {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "2. SQUAD & TRAVELER TYPE",
                        style = MaterialTheme.typography.labelMedium,
                        fontWeight = FontWeight.Bold,
                        color = GoldPrimary,
                        letterSpacing = 1.sp
                    )
                    Text(
                        text = "${selectedTravelerType.iconEmoji} ${selectedTravelerType.baseGroupRange}",
                        style = MaterialTheme.typography.bodySmall,
                        color = TextSecondary
                    )
                }

                // Traveler Type Cards
                TravelerType.values().forEach { type ->
                    val isSelected = type == selectedTravelerType
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp))
                            .background(if (isSelected) BgDarkElevated else GlassSurface)
                            .border(
                                1.5.dp,
                                if (isSelected) GoldPrimary else GlassBorder,
                                RoundedCornerShape(12.dp)
                            )
                            .clickable { viewModel.setBookingTravelerType(type) }
                            .padding(14.dp)
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(12.dp),
                            verticalAlignment = Alignment.Top
                        ) {
                            Text(
                                text = type.iconEmoji,
                                fontSize = 24.sp
                            )
                            Column(modifier = Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(2.dp)) {
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(
                                        text = type.title,
                                        style = MaterialTheme.typography.titleSmall,
                                        fontWeight = FontWeight.Bold,
                                        color = if (isSelected) GoldPrimary else TextPrimary
                                    )
                                    if (type == TravelerType.FRIENDS_SQUAD) {
                                        Text(
                                            text = "Best Value ✨",
                                            style = MaterialTheme.typography.labelSmall,
                                            color = AccentEmerald,
                                            fontWeight = FontWeight.Bold
                                        )
                                    }
                                }
                                Text(
                                    text = type.subtitle,
                                    style = MaterialTheme.typography.bodySmall,
                                    color = TextSecondary
                                )
                                Spacer(modifier = Modifier.height(4.dp))
                                Row(
                                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(
                                        text = "🏨 ${type.accommodationType}",
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

        // Group Size Stepper
        item {
            GlassCard(modifier = Modifier.fillMaxWidth()) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column {
                        Text(
                            text = "Number of Travelers",
                            style = MaterialTheme.typography.titleSmall,
                            fontWeight = FontWeight.Bold,
                            color = TextPrimary
                        )
                        Text(
                            text = if (groupSize >= 4 && selectedTravelerType == TravelerType.FRIENDS_SQUAD) {
                                "🎉 8% Group discount auto-applied"
                            } else {
                                "Vehicles & private suites scaled dynamically"
                            },
                            style = MaterialTheme.typography.bodySmall,
                            color = if (groupSize >= 4 && selectedTravelerType == TravelerType.FRIENDS_SQUAD) AccentEmerald else TextMuted
                        )
                    }

                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        IconButton(
                            onClick = { viewModel.setBookingGroupSize(groupSize - 1) },
                            modifier = Modifier
                                .size(36.dp)
                                .clip(CircleShape)
                                .background(BgDarkElevated)
                                .border(1.dp, GlassBorder, CircleShape)
                        ) {
                            Icon(Icons.Default.Remove, contentDescription = "Decrease", tint = TextPrimary, modifier = Modifier.size(16.dp))
                        }

                        Text(
                            text = "$groupSize",
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold,
                            color = GoldPrimary
                        )

                        IconButton(
                            onClick = { viewModel.setBookingGroupSize(groupSize + 1) },
                            modifier = Modifier
                                .size(36.dp)
                                .clip(CircleShape)
                                .background(BgDarkElevated)
                                .border(1.dp, GlassBorder, CircleShape)
                        ) {
                            Icon(Icons.Default.Add, contentDescription = "Increase", tint = TextPrimary, modifier = Modifier.size(16.dp))
                        }
                    }
                }
            }
        }

        // 3. SEASON & DATES
        item {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text(
                    text = "3. TRAVEL SEASON & DATE",
                    style = MaterialTheme.typography.labelMedium,
                    fontWeight = FontWeight.Bold,
                    color = GoldPrimary,
                    letterSpacing = 1.sp
                )

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    TravelSeason.values().forEach { s ->
                        val isSel = s == season
                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(10.dp))
                                .background(if (isSel) GoldContainer else GlassSurface)
                                .border(1.dp, if (isSel) GoldPrimary else GlassBorder, RoundedCornerShape(10.dp))
                                .clickable { viewModel.setBookingSeason(s) }
                                .padding(vertical = 10.dp, horizontal = 6.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                Text(
                                    text = s.badge,
                                    style = MaterialTheme.typography.bodySmall,
                                    fontSize = 11.sp,
                                    fontWeight = if (isSel) FontWeight.Bold else FontWeight.Normal,
                                    color = if (isSel) GoldPrimary else TextSecondary
                                )
                            }
                        }
                    }
                }

                OutlinedTextField(
                    value = travelDate,
                    onValueChange = { viewModel.updateBookingContact(date = it) },
                    label = { Text("Departure Date / Month", color = TextSecondary) },
                    leadingIcon = { Icon(Icons.Default.CalendarMonth, contentDescription = null, tint = GoldPrimary) },
                    modifier = Modifier
                        .fillMaxWidth()
                        .testTag("booking_date_input"),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedTextColor = TextPrimary,
                        unfocusedTextColor = TextPrimary,
                        focusedBorderColor = GoldPrimary,
                        unfocusedBorderColor = GlassBorder,
                        focusedContainerColor = BgDarkElevated,
                        unfocusedContainerColor = GlassSurface
                    ),
                    shape = RoundedCornerShape(12.dp)
                )
            }
        }

        // 4. CUSTOMIZABLE ADD-ONS
        item {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text(
                    text = "4. CREATOR UPGRADES & ADD-ONS",
                    style = MaterialTheme.typography.labelMedium,
                    fontWeight = FontWeight.Bold,
                    color = GoldPrimary,
                    letterSpacing = 1.sp
                )

                AVAILABLE_ADD_ONS.forEach { addon ->
                    val isChecked = selectedAddOns.contains(addon.id)
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp))
                            .background(if (isChecked) BgDarkElevated else GlassSurface)
                            .border(1.dp, if (isChecked) GoldPrimary else GlassBorder, RoundedCornerShape(12.dp))
                            .clickable { viewModel.toggleBookingAddOn(addon.id) }
                            .padding(12.dp)
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(10.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Box(
                                modifier = Modifier
                                    .size(24.dp)
                                    .clip(RoundedCornerShape(6.dp))
                                    .background(if (isChecked) GoldPrimary else BgDarkCard)
                                    .border(1.dp, if (isChecked) GoldPrimary else GlassBorder, RoundedCornerShape(6.dp)),
                                contentAlignment = Alignment.Center
                            ) {
                                if (isChecked) {
                                    Icon(Icons.Default.Check, contentDescription = "Selected", tint = BgDark, modifier = Modifier.size(16.dp))
                                }
                            }

                            Text(text = addon.iconEmoji, fontSize = 20.sp)

                            Column(modifier = Modifier.weight(1f)) {
                                Text(
                                    text = addon.name,
                                    style = MaterialTheme.typography.titleSmall,
                                    fontWeight = FontWeight.SemiBold,
                                    color = TextPrimary
                                )
                                Text(
                                    text = addon.description,
                                    style = MaterialTheme.typography.bodySmall,
                                    color = TextSecondary,
                                    fontSize = 11.sp
                                )
                            }

                            Text(
                                text = if (addon.pricePerPerson > 0) "+₹${String.format("%,d", addon.pricePerPerson)}/p" else "+₹${String.format("%,d", addon.flatPricePerGroup)} flat",
                                style = MaterialTheme.typography.bodySmall,
                                fontWeight = FontWeight.Bold,
                                color = GoldPrimary
                            )
                        }
                    }
                }
            }
        }

        // 5. DYNAMIC PRICING BREAKDOWN CARD
        item {
            GlassCard(
                modifier = Modifier.fillMaxWidth(),
                borderColor = GoldPrimary
            ) {
                Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column {
                            Text(
                                text = "TOTAL PACKAGE PRICE",
                                style = MaterialTheme.typography.labelSmall,
                                color = TextMuted,
                                letterSpacing = 1.sp
                            )
                            Text(
                                text = "₹${String.format("%,d", pricing.totalGroupPrice)}",
                                style = MaterialTheme.typography.headlineMedium,
                                fontWeight = FontWeight.Bold,
                                color = GoldPrimary
                            )
                        }

                        Column(horizontalAlignment = Alignment.End) {
                            Text(
                                text = "₹${String.format("%,d", pricing.perPersonFinalPrice)} / person",
                                style = MaterialTheme.typography.titleSmall,
                                fontWeight = FontWeight.Bold,
                                color = TextPrimary
                            )
                            Text(
                                text = "for $groupSize traveler${if (groupSize > 1) "s" else ""}",
                                style = MaterialTheme.typography.bodySmall,
                                color = TextSecondary
                            )
                        }
                    }

                    HorizontalDivider(color = GlassBorder)

                    // Itemized table
                    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                        PricingRow(label = "🏨 Stays & Accommodation (${selectedTravelerType.accommodationType.take(28)}...)", value = "₹${String.format("%,d", pricing.staysCostTotal)}")
                        PricingRow(label = "🚙 Transit & Logistics (${selectedTravelerType.transportType.take(28)}...)", value = "₹${String.format("%,d", pricing.transportCostTotal)}")
                        PricingRow(label = "🍲 Curated Food Tastings (@beyondbengalurufoods spots)", value = "₹${String.format("%,d", pricing.foodCostTotal)}")
                        PricingRow(label = "🎫 Permits, Passes & Local Fixer Assistance", value = "₹${String.format("%,d", pricing.activitiesAndPassesTotal)}")
                        if (pricing.groupFlatAddOns > 0 || pricing.perPersonAddOns > 0) {
                            PricingRow(label = "✨ Custom Selected Add-Ons", value = "₹${String.format("%,d", (pricing.perPersonAddOns * groupSize) + pricing.groupFlatAddOns)}")
                        }
                    }
                }
            }
        }

        // 6. CONTACT DETAILS
        item {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text(
                    text = "6. LEAD TRAVELER DETAILS",
                    style = MaterialTheme.typography.labelMedium,
                    fontWeight = FontWeight.Bold,
                    color = GoldPrimary,
                    letterSpacing = 1.sp
                )

                OutlinedTextField(
                    value = contactName,
                    onValueChange = { viewModel.updateBookingContact(name = it) },
                    label = { Text("Lead Traveler Name", color = TextSecondary) },
                    leadingIcon = { Icon(Icons.Default.Person, contentDescription = null, tint = GoldPrimary) },
                    modifier = Modifier.fillMaxWidth(),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedTextColor = TextPrimary,
                        unfocusedTextColor = TextPrimary,
                        focusedBorderColor = GoldPrimary,
                        unfocusedBorderColor = GlassBorder,
                        focusedContainerColor = BgDarkElevated,
                        unfocusedContainerColor = GlassSurface
                    ),
                    shape = RoundedCornerShape(12.dp)
                )

                OutlinedTextField(
                    value = contactPhone,
                    onValueChange = { viewModel.updateBookingContact(phone = it) },
                    label = { Text("WhatsApp Phone Number", color = TextSecondary) },
                    leadingIcon = { Icon(Icons.Default.Phone, contentDescription = null, tint = GoldPrimary) },
                    modifier = Modifier.fillMaxWidth(),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedTextColor = TextPrimary,
                        unfocusedTextColor = TextPrimary,
                        focusedBorderColor = GoldPrimary,
                        unfocusedBorderColor = GlassBorder,
                        focusedContainerColor = BgDarkElevated,
                        unfocusedContainerColor = GlassSurface
                    ),
                    shape = RoundedCornerShape(12.dp)
                )

                OutlinedTextField(
                    value = specialNotes,
                    onValueChange = { viewModel.updateBookingContact(notes = it) },
                    label = { Text("Special Requests / Dietary Preferences", color = TextSecondary) },
                    modifier = Modifier.fillMaxWidth(),
                    maxLines = 3,
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedTextColor = TextPrimary,
                        unfocusedTextColor = TextPrimary,
                        focusedBorderColor = GoldPrimary,
                        unfocusedBorderColor = GlassBorder,
                        focusedContainerColor = BgDarkElevated,
                        unfocusedContainerColor = GlassSurface
                    ),
                    shape = RoundedCornerShape(12.dp)
                )
            }
        }

        // 7. INSTANT ACTIONS
        item {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                GoldButton(
                    text = "Generate Official Travel Voucher & Pass 🎫",
                    onClick = { viewModel.confirmBookingAndGenerateVoucher() },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(52.dp)
                        .testTag("generate_voucher_btn")
                )

                Button(
                    onClick = {
                        val v = viewModel.confirmBookingAndGenerateVoucher()
                        viewModel.openWhatsAppForBooking(v)
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(50.dp)
                        .testTag("whatsapp_booking_btn"),
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF25D366)),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Icon(Icons.Default.Send, contentDescription = null, tint = Color.White, modifier = Modifier.size(18.dp))
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = "Instant Confirm via WhatsApp 💬",
                        style = MaterialTheme.typography.labelLarge,
                        fontWeight = FontWeight.Bold,
                        color = Color.White
                    )
                }
            }
        }

        item { Spacer(modifier = Modifier.height(40.dp)) }
    }

    // Voucher Modal Popup
    activeVoucherModal?.let { voucher ->
        VoucherDialog(
            voucher = voucher,
            onWhatsAppSend = { viewModel.openWhatsAppForBooking(voucher) },
            onDismiss = { viewModel.dismissVoucherModal() }
        )
    }
}

@Composable
private fun PricingRow(label: String, value: String) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.bodySmall,
            color = TextSecondary,
            fontSize = 12.sp
        )
        Text(
            text = value,
            style = MaterialTheme.typography.bodySmall,
            fontWeight = FontWeight.SemiBold,
            color = TextPrimary,
            fontSize = 12.sp
        )
    }
}

@Composable
fun VoucherDialog(
    voucher: TravelVoucher,
    onWhatsAppSend: () -> Unit,
    onDismiss: () -> Unit
) {
    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Color.Black.copy(alpha = 0.85f))
                .padding(20.dp),
            contentAlignment = Alignment.Center
        ) {
            GlassCard(
                modifier = Modifier.fillMaxWidth(),
                borderColor = GoldPrimary
            ) {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    verticalArrangement = Arrangement.spacedBy(14.dp)
                ) {
                    // Header
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.ConfirmationNumber, contentDescription = null, tint = GoldPrimary)
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(
                                text = "OFFICIAL TRAVEL PASS",
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.Bold,
                                color = GoldPrimary,
                                letterSpacing = 1.sp
                            )
                        }
                        IconButton(onClick = onDismiss) {
                            Icon(Icons.Default.Close, contentDescription = "Close", tint = TextMuted)
                        }
                    }

                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(8.dp))
                            .background(BgDarkElevated)
                            .padding(10.dp)
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Text(text = "PASS ID: ${voucher.voucherId}", style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.Bold, color = TextPrimary)
                            Text(text = "STATUS: CONFIRMED ✓", style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.Bold, color = AccentEmerald)
                        }
                    }

                    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                        Text(text = voucher.tripTitle, style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold, color = TextPrimary)
                        Text(text = "${voucher.durationText} · Departure: ${voucher.travelDate}", style = MaterialTheme.typography.bodyMedium, color = TextSecondary)
                    }

                    HorizontalDivider(color = GlassBorder)

                    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                        Text(text = "Lead Traveler: ${voucher.travelerName}", style = MaterialTheme.typography.bodyMedium, color = TextPrimary)
                        Text(text = "Squad Type: ${voucher.travelerTier} (${voucher.groupCount} travelers)", style = MaterialTheme.typography.bodySmall, color = TextSecondary)
                        Text(text = "Total Paid/Locked: ${voucher.totalAmountPaid} (${voucher.perPersonRate})", style = MaterialTheme.typography.bodySmall, fontWeight = FontWeight.Bold, color = GoldPrimary)
                        if (voucher.includedAddOns.isNotEmpty()) {
                            Text(text = "Inclusions: ${voucher.includedAddOns.joinToString(", ")}", style = MaterialTheme.typography.bodySmall, color = TextMuted)
                        }
                    }

                    // QR representation
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(8.dp))
                            .background(Color.White)
                            .padding(12.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Icon(Icons.Default.QrCode, contentDescription = "QR Code", tint = Color.Black, modifier = Modifier.size(70.dp))
                            Text(text = voucher.qrCodePayload, style = MaterialTheme.typography.labelSmall, color = Color.DarkGray)
                        }
                    }

                    Text(
                        text = "Emergency 24/7 Coordinator: ${voucher.emergencyCoordinator}",
                        style = MaterialTheme.typography.bodySmall,
                        color = TextSecondary,
                        fontSize = 11.sp
                    )

                    Button(
                        onClick = onWhatsAppSend,
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(48.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF25D366)),
                        shape = RoundedCornerShape(10.dp)
                    ) {
                        Text("Share Voucher on WhatsApp 🚀", fontWeight = FontWeight.Bold, color = Color.White)
                    }
                }
            }
        }
    }
}
