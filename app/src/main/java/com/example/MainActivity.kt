package com.example

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.togetherWith
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
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.ConfirmationNumber
import androidx.compose.material.icons.filled.Explore
import androidx.compose.material.icons.filled.Headphones
import androidx.compose.material.icons.filled.ShoppingBag
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
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
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.ui.screens.AiChatbotScreen
import com.example.ui.screens.BookingScreen
import com.example.ui.screens.ExploreScreen
import com.example.ui.screens.PocketGuideScreen
import com.example.ui.screens.SavedTripsScreen
import com.example.ui.screens.TripDetailDialog
import com.example.ui.theme.*
import com.example.ui.viewmodel.AppTab
import com.example.ui.viewmodel.MainViewModel

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyApplicationTheme {
                ComeTripWithMeApp()
            }
        }
    }
}

@Composable
fun ComeTripWithMeApp(
    viewModel: MainViewModel = viewModel()
) {
    val currentTab by viewModel.currentTab.collectAsState()
    val selectedTrip by viewModel.selectedTrip.collectAsState()

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = BgDark
    ) {
        Scaffold(
            modifier = Modifier.fillMaxSize(),
            containerColor = BgDark,
            topBar = {
                LuxuryTopAppBar(
                    onWhatsAppClick = { viewModel.openWhatsApp() },
                    onInstagramClick = { viewModel.openInstagram() }
                )
            },
            bottomBar = {
                LuxuryBottomNavBar(
                    selectedTab = currentTab,
                    onTabSelected = { viewModel.setTab(it) }
                )
            }
        ) { innerPadding ->
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(innerPadding)
            ) {
                AnimatedContent(
                    targetState = currentTab,
                    transitionSpec = { fadeIn() togetherWith fadeOut() },
                    label = "tabTransition"
                ) { tab ->
                    when (tab) {
                        AppTab.EXPLORE -> ExploreScreen(viewModel = viewModel)
                        AppTab.BOOK_ITINERARY -> BookingScreen(viewModel = viewModel)
                        AppTab.AI_CHAT_PLANNER -> AiChatbotScreen(viewModel = viewModel)
                        AppTab.POCKET_GUIDE -> PocketGuideScreen(viewModel = viewModel)
                        AppTab.SAVED_TRIPS -> SavedTripsScreen(viewModel = viewModel)
                    }
                }
            }
        }

        // Trip Detail Popup Modal
        selectedTrip?.let { trip ->
            TripDetailDialog(
                trip = trip,
                viewModel = viewModel,
                onDismiss = { viewModel.selectTrip(null) }
            )
        }
    }
}

@Composable
fun LuxuryTopAppBar(
    onWhatsAppClick: () -> Unit,
    onInstagramClick: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .statusBarsPadding()
            .background(BgDark.copy(alpha = 0.96f))
            .border(0.5.dp, GlassBorder)
            .padding(horizontal = 20.dp, vertical = 14.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Minimalist Brand Monogram + Typography
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Box(
                modifier = Modifier
                    .size(32.dp)
                    .clip(RoundedCornerShape(8.dp))
                    .background(
                        Brush.linearGradient(
                            listOf(GoldPrimary, GoldDark)
                        )
                    ),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = "✦",
                    color = BgDark,
                    fontSize = 15.sp,
                    fontWeight = FontWeight.Black
                )
            }

            Column(verticalArrangement = Arrangement.spacedBy(1.dp)) {
                Text(
                    text = "COMETRIPWITHME",
                    style = MaterialTheme.typography.labelLarge.copy(
                        color = TextPrimary,
                        fontWeight = FontWeight.Bold,
                        letterSpacing = 2.sp,
                        fontSize = 13.sp
                    )
                )
                Text(
                    text = "Curated Offbeat Journeys",
                    style = MaterialTheme.typography.labelSmall.copy(
                        color = GoldPrimary,
                        fontSize = 9.sp,
                        letterSpacing = 0.8.sp,
                        fontWeight = FontWeight.Medium
                    )
                )
            }
        }

        // Minimalist Circular Action Icons
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            Box(
                modifier = Modifier
                    .size(36.dp)
                    .clip(CircleShape)
                    .background(BgDarkSurface)
                    .border(0.8.dp, GlassBorder, CircleShape)
                    .clickable { onInstagramClick() }
                    .testTag("top_instagram_btn"),
                contentAlignment = Alignment.Center
            ) {
                Text(text = "📸", fontSize = 13.sp)
            }

            Box(
                modifier = Modifier
                    .size(36.dp)
                    .clip(CircleShape)
                    .background(GoldPrimary.copy(alpha = 0.12f))
                    .border(0.8.dp, GlassBorderGold, CircleShape)
                    .clickable { onWhatsAppClick() }
                    .testTag("top_whatsapp_btn"),
                contentAlignment = Alignment.Center
            ) {
                Text(text = "💬", fontSize = 13.sp)
            }
        }
    }
}

@Composable
fun LuxuryBottomNavBar(
    selectedTab: AppTab,
    onTabSelected: (AppTab) -> Unit
) {
    val items = listOf(
        Triple(AppTab.EXPLORE, "Explore", Icons.Default.Explore),
        Triple(AppTab.BOOK_ITINERARY, "Book", Icons.Default.ShoppingBag),
        Triple(AppTab.AI_CHAT_PLANNER, "Copilot", Icons.Default.AutoAwesome),
        Triple(AppTab.POCKET_GUIDE, "Guide", Icons.Default.Headphones),
        Triple(AppTab.SAVED_TRIPS, "Saved", Icons.Default.Bookmark)
    )

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .navigationBarsPadding()
            .padding(horizontal = 16.dp, vertical = 10.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(24.dp))
                .background(BgDarkElevated.copy(alpha = 0.95f))
                .border(1.dp, GlassBorder, RoundedCornerShape(24.dp))
                .padding(horizontal = 6.dp, vertical = 6.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            items.forEach { (tab, label, icon) ->
                val isSelected = selectedTab == tab
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(18.dp))
                        .background(if (isSelected) GoldPrimary.copy(alpha = 0.14f) else Color.Transparent)
                        .border(
                            width = if (isSelected) 0.8.dp else 0.dp,
                            color = if (isSelected) GlassBorderGold else Color.Transparent,
                            shape = RoundedCornerShape(18.dp)
                        )
                        .clickable { onTabSelected(tab) }
                        .padding(horizontal = 14.dp, vertical = 8.dp)
                        .testTag("nav_tab_${tab.name.lowercase()}"),
                    contentAlignment = Alignment.Center
                ) {
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.spacedBy(3.dp)
                    ) {
                        Icon(
                            imageVector = icon,
                            contentDescription = label,
                            tint = if (isSelected) GoldPrimary else TextSecondary.copy(alpha = 0.5f),
                            modifier = Modifier.size(20.dp)
                        )
                        Text(
                            text = label,
                            style = MaterialTheme.typography.labelSmall.copy(
                                color = if (isSelected) GoldPrimary else TextSecondary.copy(alpha = 0.5f),
                                fontWeight = if (isSelected) FontWeight.SemiBold else FontWeight.Normal,
                                fontSize = 10.sp,
                                letterSpacing = 0.3.sp
                            )
                        )
                    }
                }
            }
        }
    }
}

