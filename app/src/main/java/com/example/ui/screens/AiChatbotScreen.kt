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
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.BookmarkBorder
import androidx.compose.material.icons.filled.CalendarMonth
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.LocationOn
import androidx.compose.material.icons.filled.Restaurant
import androidx.compose.material.icons.filled.Send
import androidx.compose.material.icons.filled.ShoppingCart
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.CircularProgressIndicator
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
import androidx.compose.runtime.LaunchedEffect
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
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.model.AiChatMessage
import com.example.data.model.CustomItineraryResult
import com.example.data.model.TravelerType
import com.example.ui.components.GlassCard
import com.example.ui.components.GoldButton
import com.example.ui.components.GoldPillBadge
import com.example.ui.theme.AccentEmerald
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
fun AiChatbotScreen(
    viewModel: MainViewModel,
    modifier: Modifier = Modifier
) {
    val messages by viewModel.chatMessages.collectAsState()
    val isAiThinking by viewModel.isAiThinking.collectAsState()
    var inputQuery by remember { mutableStateOf("") }
    val listState = rememberLazyListState()

    // Auto-scroll to latest message
    LaunchedEffect(messages.size, isAiThinking) {
        if (messages.isNotEmpty()) {
            listState.animateScrollToItem(messages.size - 1)
        }
    }

    val quickPrompts = listOf(
        "Plan 5-day offbeat Meghalaya trek for 4 friends under ₹18k",
        "Spiti Valley 7-day road trip for couple with homestays",
        "Ziro Valley secret camping & music route for 6 friends",
        "4-day Tirthan pine retreat for family with kids",
        "Curate luxury 6-day Sri Lanka coastal & food route"
    )

    Column(
        modifier = modifier
            .fillMaxSize()
            .background(BgDark)
    ) {
        // Chat Header
        Surface(
            modifier = Modifier.fillMaxWidth(),
            color = BgDarkCard,
            shadowElevation = 4.dp
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 12.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    Box(
                        modifier = Modifier
                            .size(40.dp)
                            .clip(CircleShape)
                            .background(
                                Brush.linearGradient(
                                    listOf(GoldPrimary, GoldSecondary)
                                )
                            ),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            Icons.Default.AutoAwesome,
                            contentDescription = null,
                            tint = BgDark,
                            modifier = Modifier.size(22.dp)
                        )
                    }

                    Column {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(
                                text = "AI Trip Copilot",
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.Bold,
                                color = TextPrimary
                            )
                            Spacer(modifier = Modifier.width(6.dp))
                            GoldPillBadge(text = "Gemini Flash ✦")
                        }
                        Text(
                            text = "Custom itineraries · Group pricing · Food spots",
                            style = MaterialTheme.typography.bodySmall,
                            color = TextSecondary,
                            fontSize = 11.sp
                        )
                    }
                }
            }
        }

        // Messages List
        LazyColumn(
            state = listState,
            modifier = Modifier
                .weight(1f)
                .fillMaxWidth()
                .padding(horizontal = 14.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            item { Spacer(modifier = Modifier.height(10.dp)) }

            items(messages, key = { it.id }) { msg ->
                ChatMessageItem(
                    message = msg,
                    onSaveToRoom = { customPlan -> viewModel.saveCustomItineraryToRoom(customPlan) },
                    onBookCustom = { customPlan -> viewModel.startBookingForCustom(customPlan) }
                )
            }

            if (isAiThinking) {
                item {
                    AiThinkingBubble()
                }
            }

            item { Spacer(modifier = Modifier.height(12.dp)) }
        }

        // Quick Suggestion Chips
        val chipScrollState = rememberScrollState()
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .background(BgDarkElevated.copy(alpha = 0.6f))
                .horizontalScroll(chipScrollState)
                .padding(horizontal = 12.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            quickPrompts.forEach { prompt ->
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(20.dp))
                        .background(GlassSurface)
                        .border(1.dp, GlassBorder, RoundedCornerShape(20.dp))
                        .clickable {
                            inputQuery = prompt
                            viewModel.sendAiChatMessage(prompt)
                            inputQuery = ""
                        }
                        .padding(horizontal = 12.dp, vertical = 6.dp)
                ) {
                    Text(
                        text = prompt,
                        style = MaterialTheme.typography.bodySmall,
                        color = GoldPrimary,
                        fontSize = 12.sp,
                        maxLines = 1
                    )
                }
            }
        }

        // Input Field
        Surface(
            modifier = Modifier.fillMaxWidth(),
            color = BgDarkCard,
            shadowElevation = 8.dp
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 12.dp, vertical = 10.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                OutlinedTextField(
                    value = inputQuery,
                    onValueChange = { inputQuery = it },
                    placeholder = {
                        Text(
                            "Ask e.g. 5-day Spiti trip for 4 friends under ₹20k...",
                            color = TextTertiary,
                            fontSize = 13.sp
                        )
                    },
                    modifier = Modifier
                        .weight(1f)
                        .testTag("ai_chat_input"),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedTextColor = TextPrimary,
                        unfocusedTextColor = TextPrimary,
                        focusedBorderColor = GoldPrimary,
                        unfocusedBorderColor = GlassBorder,
                        focusedContainerColor = BgDarkElevated,
                        unfocusedContainerColor = BgDarkElevated
                    ),
                    shape = RoundedCornerShape(24.dp),
                    maxLines = 3
                )

                IconButton(
                    onClick = {
                        if (inputQuery.isNotBlank() && !isAiThinking) {
                            val q = inputQuery
                            inputQuery = ""
                            viewModel.sendAiChatMessage(q)
                        }
                    },
                    modifier = Modifier
                        .size(46.dp)
                        .clip(CircleShape)
                        .background(
                            if (inputQuery.isNotBlank()) Brush.linearGradient(
                                listOf(GoldPrimary, GoldSecondary)
                            ) else Brush.linearGradient(listOf(BgDarkElevated, BgDarkElevated))
                        )
                        .testTag("ai_send_button")
                ) {
                    Icon(
                        Icons.Default.Send,
                        contentDescription = "Send",
                        tint = if (inputQuery.isNotBlank()) BgDark else TextMuted,
                        modifier = Modifier.size(20.dp)
                    )
                }
            }
        }
    }
}

@Composable
fun ChatMessageItem(
    message: AiChatMessage,
    onSaveToRoom: (CustomItineraryResult) -> Unit,
    onBookCustom: (CustomItineraryResult) -> Unit
) {
    if (message.isFromUser) {
        // User message bubble
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.End
        ) {
            Box(
                modifier = Modifier
                    .fillMaxWidth(0.85f)
                    .clip(RoundedCornerShape(topStart = 16.dp, topEnd = 4.dp, bottomStart = 16.dp, bottomEnd = 16.dp))
                    .background(
                        Brush.linearGradient(
                            listOf(Color(0xFF2A2315), Color(0xFF3B2F18))
                        )
                    )
                    .border(1.dp, GoldPrimary.copy(alpha = 0.5f), RoundedCornerShape(topStart = 16.dp, topEnd = 4.dp, bottomStart = 16.dp, bottomEnd = 16.dp))
                    .padding(14.dp)
            ) {
                Text(
                    text = message.text,
                    style = MaterialTheme.typography.bodyMedium,
                    color = TextPrimary,
                    lineHeight = 20.sp
                )
            }
        }
    } else {
        // Assistant message bubble
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.Start
        ) {
            Column(
                modifier = Modifier.fillMaxWidth(),
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(topStart = 4.dp, topEnd = 16.dp, bottomStart = 16.dp, bottomEnd = 16.dp))
                        .background(BgDarkElevated)
                        .border(1.dp, GlassBorder, RoundedCornerShape(topStart = 4.dp, topEnd = 16.dp, bottomStart = 16.dp, bottomEnd = 16.dp))
                        .padding(14.dp)
                ) {
                    Text(
                        text = message.text,
                        style = MaterialTheme.typography.bodyMedium,
                        color = TextPrimary,
                        lineHeight = 22.sp
                    )
                }

                // If message has generated custom itinerary, render rich interactive card
                message.customItinerary?.let { custom ->
                    CustomItineraryCard(
                        itinerary = custom,
                        onSaveToRoom = { onSaveToRoom(custom) },
                        onBookCustom = { onBookCustom(custom) }
                    )
                }
            }
        }
    }
}

@Composable
fun CustomItineraryCard(
    itinerary: CustomItineraryResult,
    onSaveToRoom: () -> Unit,
    onBookCustom: () -> Unit
) {
    GlassCard(
        modifier = Modifier.fillMaxWidth(),
        borderColor = GoldPrimary
    ) {
        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
            // Header
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = itinerary.title,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold,
                        color = GoldPrimary
                    )
                    Text(
                        text = itinerary.tagline,
                        style = MaterialTheme.typography.bodySmall,
                        color = TextSecondary
                    )
                }
                GoldPillBadge(text = "${itinerary.duration} ✦")
            }

            HorizontalDivider(color = GlassBorder)

            // Day-wise Highlights
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text(
                    text = "DAY-BY-DAY CURATED SPOTS & FOOD",
                    style = MaterialTheme.typography.labelSmall,
                    fontWeight = FontWeight.Bold,
                    color = GoldPrimary,
                    letterSpacing = 1.sp
                )

                itinerary.dayWisePlans.forEach { day ->
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(10.dp))
                            .background(BgDarkCard)
                            .border(1.dp, GlassBorder, RoundedCornerShape(10.dp))
                            .padding(10.dp)
                    ) {
                        Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween
                            ) {
                                Text(
                                    text = "Day ${day.dayNumber}: ${day.title}",
                                    style = MaterialTheme.typography.titleSmall,
                                    fontWeight = FontWeight.Bold,
                                    color = TextPrimary
                                )
                            }
                            Text(
                                text = "🌅 ${day.morningActivity}",
                                style = MaterialTheme.typography.bodySmall,
                                color = TextSecondary,
                                fontSize = 12.sp
                            )
                            Text(
                                text = "✨ Offbeat Gem: ${day.offbeatSecretSpot}",
                                style = MaterialTheme.typography.bodySmall,
                                color = AccentEmerald,
                                fontSize = 12.sp,
                                fontWeight = FontWeight.SemiBold
                            )
                            Text(
                                text = "🍲 Must-Try: ${day.mustTryFoodSpot}",
                                style = MaterialTheme.typography.bodySmall,
                                color = GoldSecondary,
                                fontSize = 12.sp
                            )
                            Text(
                                text = "💡 Insider Tip: ${day.creatorTip}",
                                style = MaterialTheme.typography.bodySmall,
                                color = TextMuted,
                                fontSize = 11.sp
                            )
                        }
                    }
                }
            }

            HorizontalDivider(color = GlassBorder)

            // Dynamic Group Pricing Section
            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                Text(
                    text = "DYNAMIC PRICING BY SQUAD TYPE",
                    style = MaterialTheme.typography.labelSmall,
                    fontWeight = FontWeight.Bold,
                    color = GoldPrimary,
                    letterSpacing = 1.sp
                )

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    GroupPriceBadge(title = "🎒 Solo", price = "₹${String.format("%,d", (itinerary.basePerPersonBudget * 0.80).toInt())}")
                    GroupPriceBadge(title = "💑 Couple", price = "₹${String.format("%,d", (itinerary.basePerPersonBudget * 1.0).toInt())}")
                    GroupPriceBadge(title = "🎉 Friends (4+)", price = "₹${String.format("%,d", (itinerary.basePerPersonBudget * 0.78).toInt())}")
                }
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    GroupPriceBadge(title = "👨‍👩‍👧 Family", price = "₹${String.format("%,d", (itinerary.basePerPersonBudget * 1.18).toInt())}")
                    GroupPriceBadge(title = "👑 VIP Suite", price = "₹${String.format("%,d", (itinerary.basePerPersonBudget * 1.75).toInt())}")
                }
            }

            // Creator Verdict
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(8.dp))
                    .background(BgDarkElevated)
                    .padding(10.dp)
            ) {
                Text(
                    text = "🎬 Creator Verdict: ${itinerary.creatorVerdict}",
                    style = MaterialTheme.typography.bodySmall,
                    color = TextSecondary,
                    fontSize = 11.sp
                )
            }

            // Action Buttons (Save to Room & Book)
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Box(
                    modifier = Modifier
                        .weight(1f)
                        .clip(RoundedCornerShape(10.dp))
                        .background(if (itinerary.isSavedToRoom) GoldContainer else GlassSurface)
                        .border(1.dp, if (itinerary.isSavedToRoom) GoldPrimary else GlassBorder, RoundedCornerShape(10.dp))
                        .clickable { onSaveToRoom() }
                        .padding(vertical = 10.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        Icon(
                            if (itinerary.isSavedToRoom) Icons.Default.Bookmark else Icons.Default.BookmarkBorder,
                            contentDescription = null,
                            tint = if (itinerary.isSavedToRoom) GoldPrimary else TextPrimary,
                            modifier = Modifier.size(16.dp)
                        )
                        Text(
                            text = if (itinerary.isSavedToRoom) "Saved in Room ✓" else "Save Itinerary",
                            style = MaterialTheme.typography.bodySmall,
                            fontWeight = FontWeight.Bold,
                            color = if (itinerary.isSavedToRoom) GoldPrimary else TextPrimary
                        )
                    }
                }

                Box(
                    modifier = Modifier
                        .weight(1f)
                        .clip(RoundedCornerShape(10.dp))
                        .background(Brush.linearGradient(listOf(GoldPrimary, GoldSecondary)))
                        .clickable { onBookCustom() }
                        .padding(vertical = 10.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        Icon(Icons.Default.ShoppingCart, contentDescription = null, tint = BgDark, modifier = Modifier.size(16.dp))
                        Text(
                            text = "Book This Route ➔",
                            style = MaterialTheme.typography.bodySmall,
                            fontWeight = FontWeight.Bold,
                            color = BgDark
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun GroupPriceBadge(title: String, price: String) {
    Box(
        modifier = Modifier
            .clip(RoundedCornerShape(8.dp))
            .background(BgDarkCard)
            .border(1.dp, GlassBorder, RoundedCornerShape(8.dp))
            .padding(horizontal = 10.dp, vertical = 6.dp)
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Text(text = title, style = MaterialTheme.typography.labelSmall, color = TextMuted, fontSize = 10.sp)
            Text(text = price, style = MaterialTheme.typography.bodySmall, fontWeight = FontWeight.Bold, color = GoldPrimary, fontSize = 11.sp)
        }
    }
}

@Composable
fun AiThinkingBubble() {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.Start
    ) {
        Box(
            modifier = Modifier
                .clip(RoundedCornerShape(16.dp))
                .background(BgDarkElevated)
                .border(1.dp, GlassBorderGold, RoundedCornerShape(16.dp))
                .padding(horizontal = 14.dp, vertical = 10.dp)
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                CircularProgressIndicator(
                    modifier = Modifier.size(16.dp),
                    color = GoldPrimary,
                    strokeWidth = 2.dp
                )
                Text(
                    text = "Searching offbeat secret routes & calculating group rates...",
                    style = MaterialTheme.typography.bodySmall,
                    color = GoldPrimary,
                    fontSize = 12.sp
                )
            }
        }
    }
}
