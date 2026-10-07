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
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowForward
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Slider
import androidx.compose.material3.SliderDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.model.TripVibe
import com.example.ui.components.GlassCard
import com.example.ui.components.GoldButton
import com.example.ui.components.GoldPillBadge
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
fun PlannerScreen(
    viewModel: MainViewModel,
    modifier: Modifier = Modifier
) {
    var destination by remember { mutableStateOf("Goa") }
    var selectedVibe by remember { mutableStateOf(TripVibe.PARTY) }
    var durationDays by remember { mutableIntStateOf(4) }
    var squadSize by remember { mutableStateOf("2 of us 👫") }
    var budgetSlider by remember { mutableFloatStateOf(10000f) }
    var customNotes by remember { mutableStateOf("") }

    val estStay = (budgetSlider * 0.40f).toInt()
    val estFood = (budgetSlider * 0.30f).toInt()
    val estTransport = (budgetSlider * 0.18f).toInt()
    val estExperiences = (budgetSlider * 0.12f).toInt()

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .background(BgDark)
            .padding(horizontal = 20.dp)
            .testTag("planner_screen"),
        verticalArrangement = Arrangement.spacedBy(20.dp)
    ) {
        // 1. Header
        item {
            Spacer(modifier = Modifier.height(12.dp))
            GoldPillBadge(text = "Tailored Routes")
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = "Custom Trip Builder",
                style = MaterialTheme.typography.headlineLarge.copy(
                    fontWeight = FontWeight.ExtraBold,
                    color = TextPrimary
                )
            )
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = "Build your custom itinerary. We calculate realistic budget allocations with verified creator spots.",
                style = MaterialTheme.typography.bodyMedium.copy(color = TextSecondary)
            )
        }

        // 2. Destination Selector
        item {
            GlassCard(
                borderColor = GlassBorder,
                backgroundColor = BgDarkCard
            ) {
                Column(modifier = Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    Text(
                        text = "1. CHOOSE DESTINATION",
                        style = MaterialTheme.typography.labelSmall.copy(
                            color = GoldPrimary,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 1.sp
                        )
                    )

                    val destinations = listOf("Goa", "Thailand", "Himachal", "Pondicherry", "Krabi", "Malaysia", "Gokarna", "Coorg", "Hampi")
                    val scrollState = rememberScrollState()

                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .horizontalScroll(scrollState),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        destinations.forEach { dest ->
                            val isSelected = destination == dest
                            Box(
                                modifier = Modifier
                                    .clip(RoundedCornerShape(100.dp))
                                    .background(if (isSelected) GoldPrimary else GlassSurface)
                                    .border(
                                        1.dp,
                                        if (isSelected) GoldPrimary else GlassBorder,
                                        RoundedCornerShape(100.dp)
                                    )
                                    .clickable { destination = dest }
                                    .padding(horizontal = 16.dp, vertical = 8.dp)
                            ) {
                                Text(
                                    text = dest,
                                    style = MaterialTheme.typography.labelMedium.copy(
                                        color = if (isSelected) BgDark else TextPrimary,
                                        fontWeight = FontWeight.Bold
                                    )
                                )
                            }
                        }
                    }
                }
            }
        }

        // 3. Vibe Selector
        item {
            GlassCard(
                borderColor = GlassBorder,
                backgroundColor = BgDarkCard
            ) {
                Column(modifier = Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    Text(
                        text = "2. SELECT TRIP VIBE",
                        style = MaterialTheme.typography.labelSmall.copy(
                            color = GoldPrimary,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 1.sp
                        )
                    )

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        TripVibe.values().forEach { vibe ->
                            val isSelected = selectedVibe == vibe
                            Box(
                                modifier = Modifier
                                    .weight(1f)
                                    .clip(RoundedCornerShape(12.dp))
                                    .background(if (isSelected) Color(vibe.badgeColorHex) else GlassSurface)
                                    .border(
                                        1.dp,
                                        if (isSelected) Color(vibe.badgeColorHex) else GlassBorder,
                                        RoundedCornerShape(12.dp)
                                    )
                                    .clickable { selectedVibe = vibe }
                                    .padding(vertical = 12.dp),
                                contentAlignment = Alignment.Center
                            ) {
                                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                    Text(text = vibe.emoji, fontSize = 18.sp)
                                    Spacer(modifier = Modifier.height(4.dp))
                                    Text(
                                        text = vibe.label,
                                        style = MaterialTheme.typography.labelSmall.copy(
                                            color = if (isSelected && vibe == TripVibe.LUXURY) BgDark else TextPrimary,
                                            fontWeight = FontWeight.Bold,
                                            fontSize = 9.sp
                                        )
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }

        // 4. Duration & Squad Size
        item {
            GlassCard(
                borderColor = GlassBorder,
                backgroundColor = BgDarkCard
            ) {
                Column(modifier = Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
                    // Duration
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "3. DURATION",
                            style = MaterialTheme.typography.labelSmall.copy(
                                color = GoldPrimary,
                                fontWeight = FontWeight.Bold,
                                letterSpacing = 1.sp
                            )
                        )
                        Text(
                            text = "$durationDays Days / ${durationDays - 1} Nights",
                            style = MaterialTheme.typography.labelMedium.copy(
                                color = GoldSecondary,
                                fontWeight = FontWeight.Bold
                            )
                        )
                    }

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        listOf(3, 4, 5, 7, 10).forEach { days ->
                            val isSelected = durationDays == days
                            Box(
                                modifier = Modifier
                                    .weight(1f)
                                    .clip(RoundedCornerShape(8.dp))
                                    .background(if (isSelected) GoldPrimary else GlassSurface)
                                    .border(
                                        1.dp,
                                        if (isSelected) GoldPrimary else GlassBorder,
                                        RoundedCornerShape(8.dp)
                                    )
                                    .clickable { durationDays = days }
                                    .padding(vertical = 8.dp),
                                contentAlignment = Alignment.Center
                            ) {
                                Text(
                                    text = "${days}D",
                                    style = MaterialTheme.typography.labelMedium.copy(
                                        color = if (isSelected) BgDark else TextPrimary,
                                        fontWeight = FontWeight.Bold
                                    )
                                )
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(6.dp))

                    // Squad size
                    Text(
                        text = "4. TRAVELERS / SQUAD",
                        style = MaterialTheme.typography.labelSmall.copy(
                            color = GoldPrimary,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 1.sp
                        )
                    )

                    val squads = listOf("Solo 🙋", "2 of us 👫", "Small squad (3-5) 🫂", "Big group (6+) 🎉")
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        squads.forEach { sq ->
                            val isSelected = squadSize == sq
                            Box(
                                modifier = Modifier
                                    .weight(1f)
                                    .clip(RoundedCornerShape(8.dp))
                                    .background(if (isSelected) Color(0x33E8C97A) else GlassSurface)
                                    .border(
                                        1.dp,
                                        if (isSelected) GoldPrimary else GlassBorder,
                                        RoundedCornerShape(8.dp)
                                    )
                                    .clickable { squadSize = sq }
                                    .padding(vertical = 8.dp),
                                contentAlignment = Alignment.Center
                            ) {
                                Text(
                                    text = sq.split(" ").first(),
                                    style = MaterialTheme.typography.labelSmall.copy(
                                        color = if (isSelected) GoldPrimary else TextSecondary,
                                        fontWeight = FontWeight.Bold,
                                        fontSize = 11.sp
                                    )
                                )
                            }
                        }
                    }
                }
            }
        }

        // 5. Budget Allocation Calculator
        item {
            GlassCard(
                borderColor = GlassBorderGold,
                backgroundColor = BgDarkCard
            ) {
                Column(modifier = Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "5. TARGET BUDGET (₹/PERSON)",
                            style = MaterialTheme.typography.labelSmall.copy(
                                color = GoldPrimary,
                                fontWeight = FontWeight.Bold,
                                letterSpacing = 1.sp
                            )
                        )
                        Text(
                            text = "₹${budgetSlider.toInt()}",
                            style = MaterialTheme.typography.titleLarge.copy(
                                color = GoldPrimary,
                                fontWeight = FontWeight.ExtraBold
                            )
                        )
                    }

                    Slider(
                        value = budgetSlider,
                        onValueChange = { budgetSlider = it },
                        valueRange = 4000f..60000f,
                        steps = 55,
                        colors = SliderDefaults.colors(
                            thumbColor = GoldPrimary,
                            activeTrackColor = GoldPrimary,
                            inactiveTrackColor = GlassBorder
                        ),
                        modifier = Modifier.testTag("budget_slider")
                    )

                    // Breakdown bars
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text(
                            text = "ESTIMATED ALLOCATION BREAKDOWN",
                            style = MaterialTheme.typography.labelSmall.copy(
                                color = TextTertiary,
                                fontSize = 9.sp,
                                letterSpacing = 1.sp
                            )
                        )

                        BudgetItemRow("🏨 Verified Stays / Huts", "₹$estStay", "40%")
                        BudgetItemRow("🍜 Food & Cafés (@beyondbenaglurufoods)", "₹$estFood", "30%")
                        BudgetItemRow("🛵 Scooty / Ferries / Local Transport", "₹$estTransport", "18%")
                        BudgetItemRow("🎟️ Kayaking, Guide & Experiences", "₹$estExperiences", "12%")
                    }
                }
            }
        }

        // 6. Direct WhatsApp Inquiry Export
        item {
            GlassCard(
                borderColor = GlassBorderGold,
                backgroundColor = Color(0x1FE8C97A)
            ) {
                Column(
                    modifier = Modifier.padding(20.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    Text(
                        text = "READY TO SORT YOUR ITINERARY?",
                        style = MaterialTheme.typography.labelSmall.copy(
                            color = GoldPrimary,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 1.sp
                        )
                    )

                    Text(
                        text = "I personally review your vibe & budget requirements and send the complete Day-by-Day route on WhatsApp within a few hours.",
                        style = MaterialTheme.typography.bodyMedium.copy(
                            color = TextPrimary,
                            lineHeight = 20.sp
                        )
                    )

                    GoldButton(
                        text = "Send Request On WhatsApp 💬",
                        onClick = {
                            val msg = "Hey ComeTripWithMe! Please sort a custom trip for me:\n" +
                                    "📍 Destination: $destination\n" +
                                    "✨ Vibe: ${selectedVibe.label}\n" +
                                    "📅 Duration: $durationDays Days\n" +
                                    "🫂 Travelers: $squadSize\n" +
                                    "💰 Target Budget: ₹${budgetSlider.toInt()}/person\n" +
                                    (if (customNotes.isNotBlank()) "📝 Notes: $customNotes" else "")
                            viewModel.openWhatsApp(msg)
                        },
                        modifier = Modifier.fillMaxWidth(),
                        testTag = "send_whatsapp_custom_plan_btn"
                    )

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        Button(
                            onClick = { viewModel.callPhone() },
                            colors = ButtonDefaults.buttonColors(
                                containerColor = GlassSurface,
                                contentColor = TextPrimary
                            ),
                            shape = RoundedCornerShape(100.dp),
                            modifier = Modifier
                                .weight(1f)
                                .height(44.dp)
                                .border(1.dp, GlassBorder, RoundedCornerShape(100.dp))
                        ) {
                            Text("📞 9742311023", style = MaterialTheme.typography.labelSmall.copy(color = GoldPrimary, fontWeight = FontWeight.Bold))
                        }

                        Button(
                            onClick = {
                                val body = "Custom Trip Request Details:\n\n" +
                                        "Destination: $destination\n" +
                                        "Vibe: ${selectedVibe.label}\n" +
                                        "Duration: $durationDays Days\n" +
                                        "Travelers: $squadSize\n" +
                                        "Budget: ₹${budgetSlider.toInt()}/person\n" +
                                        "Notes: $customNotes"
                                viewModel.openEmail(subject = "Custom Trip Request - $destination", body = body)
                            },
                            colors = ButtonDefaults.buttonColors(
                                containerColor = GlassSurface,
                                contentColor = TextPrimary
                            ),
                            shape = RoundedCornerShape(100.dp),
                            modifier = Modifier
                                .weight(1f)
                                .height(44.dp)
                                .border(1.dp, GlassBorder, RoundedCornerShape(100.dp))
                        ) {
                            Text("✉️ Email Plan", style = MaterialTheme.typography.labelSmall.copy(color = TextPrimary))
                        }
                    }
                }
            }
        }

        item {
            Spacer(modifier = Modifier.height(30.dp))
        }
    }
}

@Composable
fun BudgetItemRow(title: String, amount: String, percentage: String) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(8.dp))
            .background(GlassSurface)
            .padding(horizontal = 12.dp, vertical = 8.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(text = title, style = MaterialTheme.typography.bodyMedium.copy(color = TextPrimary, fontSize = 12.sp))
        Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
            Text(text = amount, style = MaterialTheme.typography.labelMedium.copy(color = GoldPrimary, fontWeight = FontWeight.Bold))
            Text(text = "($percentage)", style = MaterialTheme.typography.labelSmall.copy(color = TextTertiary, fontSize = 10.sp))
        }
    }
}
