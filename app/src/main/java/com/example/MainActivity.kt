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
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.EditCalendar
import androidx.compose.material.icons.filled.Explore
import androidx.compose.material.icons.filled.Headphones
import androidx.compose.material.icons.filled.PlayCircle
import androidx.compose.material.icons.filled.Send
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
import com.example.ui.screens.ContentScreen
import com.example.ui.screens.ExploreScreen
import com.example.ui.screens.PlannerScreen
import com.example.ui.screens.PocketGuideScreen
import com.example.ui.screens.SavedTripsScreen
import com.example.ui.screens.TripDetailDialog
import com.example.ui.theme.BgDark
import com.example.ui.theme.BgDarkCard
import com.example.ui.theme.BgDarkElevated
import com.example.ui.theme.GlassBorder
import com.example.ui.theme.GlassBorderGold
import com.example.ui.theme.GlassSurface
import com.example.ui.theme.GoldContainer
import com.example.ui.theme.GoldPrimary
import com.example.ui.theme.GoldSecondary
import com.example.ui.theme.MyApplicationTheme
import com.example.ui.theme.TextMuted
import com.example.ui.theme.TextPrimary
import com.example.ui.theme.TextSecondary
import com.example.ui.theme.TextTertiary
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
                        AppTab.POCKET_GUIDE -> PocketGuideScreen(viewModel = viewModel)
                        AppTab.CREATOR_HUB -> ContentScreen(viewModel = viewModel)
                        AppTab.TRIP_PLANNER -> PlannerScreen(viewModel = viewModel)
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
            .background(BgDark.copy(alpha = 0.95f))
            .border(0.5.dp, GlassBorder)
            .padding(horizontal = 20.dp, vertical = 12.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Brand Logo + Title
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            Box(
                modifier = Modifier
                    .size(34.dp)
                    .clip(CircleShape)
                    .background(
                        Brush.radialGradient(
                            listOf(GoldPrimary, GoldSecondary)
                        )
                    ),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = "✦",
                    color = BgDark,
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold
                )
            }

            Column {
                Text(
                    text = "COMETRIPWITHME",
                    style = MaterialTheme.typography.labelLarge.copy(
                        color = GoldPrimary,
                        fontWeight = FontWeight.ExtraBold,
                        letterSpacing = 1.6.sp
                    )
                )
                Text(
                    text = "India's 1st Creator Tour Operator",
                    style = MaterialTheme.typography.labelSmall.copy(
                        color = TextTertiary,
                        fontSize = 8.sp,
                        letterSpacing = 0.8.sp
                    )
                )
            }
        }

        // Action icons (Direct WhatsApp inquiry & Instagram)
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Box(
                modifier = Modifier
                    .size(36.dp)
                    .clip(CircleShape)
                    .background(GlassSurface)
                    .border(1.dp, GlassBorder, CircleShape)
                    .clickable { onInstagramClick() }
                    .testTag("top_instagram_btn"),
                contentAlignment = Alignment.Center
            ) {
                Text(text = "📸", fontSize = 14.sp)
            }

            Box(
                modifier = Modifier
                    .size(36.dp)
                    .clip(CircleShape)
                    .background(Color(0x33E8C97A))
                    .border(1.dp, GlassBorderGold, CircleShape)
                    .clickable { onWhatsAppClick() }
                    .testTag("top_whatsapp_btn"),
                contentAlignment = Alignment.Center
            ) {
                Text(text = "💬", fontSize = 14.sp)
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
        Triple(AppTab.POCKET_GUIDE, "Guide", Icons.Default.Headphones),
        Triple(AppTab.CREATOR_HUB, "Proof", Icons.Default.PlayCircle),
        Triple(AppTab.TRIP_PLANNER, "Custom", Icons.Default.EditCalendar),
        Triple(AppTab.SAVED_TRIPS, "Saved", Icons.Default.Bookmark)
    )

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .navigationBarsPadding()
            .background(BgDarkElevated.copy(alpha = 0.98f))
            .border(1.dp, GlassBorder, RoundedCornerShape(topStart = 20.dp, topEnd = 20.dp))
            .padding(horizontal = 8.dp, vertical = 8.dp),
        horizontalArrangement = Arrangement.SpaceAround,
        verticalAlignment = Alignment.CenterVertically
    ) {
        items.forEach { (tab, label, icon) ->
            val isSelected = selectedTab == tab
            Column(
                modifier = Modifier
                    .clip(RoundedCornerShape(12.dp))
                    .clickable { onTabSelected(tab) }
                    .padding(horizontal = 10.dp, vertical = 6.dp)
                    .testTag("nav_tab_${tab.name.lowercase()}"),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(3.dp)
            ) {
                Icon(
                    imageVector = icon,
                    contentDescription = label,
                    tint = if (isSelected) GoldPrimary else TextMuted,
                    modifier = Modifier.size(22.dp)
                )
                Text(
                    text = label,
                    style = MaterialTheme.typography.labelSmall.copy(
                        color = if (isSelected) GoldPrimary else TextMuted,
                        fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal,
                        fontSize = 10.sp
                    )
                )
            }
        }
    }
}

