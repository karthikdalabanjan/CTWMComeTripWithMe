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
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
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
import coil.compose.AsyncImage
import com.example.data.model.ChannelType
import com.example.data.model.InstagramPost
import com.example.data.model.VideoProof
import com.example.ui.components.GlassCard
import com.example.ui.components.GoldButton
import com.example.ui.components.GoldPillBadge
import com.example.ui.components.RatingStars
import com.example.ui.theme.AccentRed
import com.example.ui.theme.BgDark
import com.example.ui.theme.BgDarkCard
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
fun ContentScreen(
    viewModel: MainViewModel,
    modifier: Modifier = Modifier
) {
    val videos = viewModel.getVideoProofs()
    val instagramPosts = viewModel.getInstagramPosts()
    val selectedChannel by viewModel.selectedInstagramChannel.collectAsState()
    val reviews = viewModel.getTravelerReviews()

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .background(BgDark)
            .padding(horizontal = 20.dp)
            .testTag("content_screen"),
        verticalArrangement = Arrangement.spacedBy(24.dp)
    ) {
        // 1. Header
        item {
            Spacer(modifier = Modifier.height(12.dp))
            GoldPillBadge(text = "Watch Before You Book")
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = "Video Proof For Every Destination.",
                style = MaterialTheme.typography.headlineLarge.copy(
                    fontWeight = FontWeight.ExtraBold,
                    color = TextPrimary
                )
            )
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = "Watch the exact streets, food stalls, and viewpoints on my channel before you pay. No other operator can offer that.",
                style = MaterialTheme.typography.bodyMedium.copy(color = TextSecondary)
            )
        }

        // 2. Creator Channel Showcase Card
        item {
            GlassCard(
                borderColor = GlassBorderGold,
                backgroundColor = BgDarkCard
            ) {
                Column(
                    modifier = Modifier.padding(20.dp),
                    verticalArrangement = Arrangement.spacedBy(14.dp)
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(14.dp)
                    ) {
                        AsyncImage(
                            model = "https://images.unsplash.com/photo-1596178060671-7a80dc8059ea?w=200&q=80",
                            contentDescription = "ComeTripWithMe",
                            contentScale = ContentScale.Crop,
                            modifier = Modifier
                                .size(56.dp)
                                .clip(CircleShape)
                                .border(2.dp, GoldPrimary, CircleShape)
                        )

                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                text = "ComeTripWithMe",
                                style = MaterialTheme.typography.titleLarge.copy(
                                    fontWeight = FontWeight.Bold,
                                    color = TextPrimary
                                )
                            )
                            Text(
                                text = "@Cometripwithme · Bengaluru · Travel + Food",
                                style = MaterialTheme.typography.bodyMedium.copy(
                                    color = TextSecondary,
                                    fontSize = 12.sp
                                )
                            )
                        }
                    }

                    Row(
                        horizontalArrangement = Arrangement.spacedBy(10.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        GoldButton(
                            text = "▶ Subscribe On YouTube",
                            onClick = { viewModel.openYouTube() },
                            modifier = Modifier.weight(1f),
                            testTag = "youtube_subscribe_btn"
                        )

                        Button(
                            onClick = { viewModel.openInstagram() },
                            colors = ButtonDefaults.buttonColors(
                                containerColor = GlassSurface,
                                contentColor = TextPrimary
                            ),
                            shape = RoundedCornerShape(100.dp),
                            modifier = Modifier
                                .height(48.dp)
                                .border(1.dp, GlassBorderStrong, RoundedCornerShape(100.dp))
                        ) {
                            Text("📸 Instagram")
                        }
                    }
                }
            }
        }

        // 3. Featured Video Proofs
        item {
            Text(
                text = "DOCUMENTED EPISODES & PROOF",
                style = MaterialTheme.typography.labelSmall.copy(
                    color = TextTertiary,
                    letterSpacing = 1.5.sp,
                    fontWeight = FontWeight.Bold
                )
            )
        }

        items(videos) { video ->
            VideoProofCard(
                video = video,
                onPlayClick = { viewModel.openYouTube() }
            )
        }

        // 4. Subtle Recommendations Section
        item {
            Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                GoldPillBadge(text = "Field Notes & Highlights")

                Text(
                    text = "Travel & Food Reccos",
                    style = MaterialTheme.typography.headlineMedium.copy(
                        fontWeight = FontWeight.Bold,
                        color = TextPrimary
                    )
                )

                Text(
                    text = "Handpicked scenic spots, local café finds, and street recommendations from verified journeys.",
                    style = MaterialTheme.typography.bodyMedium.copy(
                        color = TextSecondary
                    )
                )

                // Filter Buttons
                Row(
                    horizontalArrangement = Arrangement.spacedBy(10.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    val isAll = selectedChannel == null
                    val isTravel = selectedChannel == ChannelType.TRAVEL
                    val isFood = selectedChannel == ChannelType.FOOD

                    ChannelFilterPill(
                        label = "All Reccos",
                        isSelected = isAll,
                        onClick = { viewModel.setInstagramChannel(null) }
                    )

                    ChannelFilterPill(
                        label = "🌊 Scenic & Trails",
                        isSelected = isTravel,
                        onClick = { viewModel.setInstagramChannel(ChannelType.TRAVEL) }
                    )

                    ChannelFilterPill(
                        label = "🍜 Food & Cafés",
                        isSelected = isFood,
                        onClick = { viewModel.setInstagramChannel(ChannelType.FOOD) }
                    )
                }
            }
        }

        // Instagram / Recco Posts
        items(instagramPosts) { post ->
            InstagramPostCard(
                post = post,
                onPostClick = { viewModel.openInstagram(post.handle) }
            )
        }

        // 5. Verified Reviews
        item {
            Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                GoldPillBadge(text = "Community Feedback")
                Text(
                    text = "What Travelers Say",
                    style = MaterialTheme.typography.headlineMedium.copy(
                        fontWeight = FontWeight.Bold,
                        color = TextPrimary
                    )
                )

                reviews.forEach { review ->
                    GlassCard(
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
                                Text(
                                    text = review.authorHandle,
                                    style = MaterialTheme.typography.labelLarge.copy(
                                        color = TextPrimary,
                                        fontWeight = FontWeight.Bold
                                    )
                                )
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
                            Text(
                                text = review.tripTag,
                                style = MaterialTheme.typography.labelSmall.copy(color = GoldSecondary)
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

@Composable
fun VideoProofCard(
    video: VideoProof,
    onPlayClick: () -> Unit
) {
    GlassCard(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onPlayClick() }
            .testTag("video_card_${video.id}"),
        borderColor = GlassBorder,
        backgroundColor = BgDarkCard
    ) {
        Column {
            // Thumbnail with play icon
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(190.dp)
            ) {
                AsyncImage(
                    model = video.thumbnailUrl,
                    contentDescription = video.title,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )

                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(Color(0x44000000))
                )

                // Play Button Center
                Box(
                    modifier = Modifier
                        .size(54.dp)
                        .clip(CircleShape)
                        .background(GoldPrimary)
                        .align(Alignment.Center),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = Icons.Default.PlayArrow,
                        contentDescription = "Play",
                        tint = BgDark,
                        modifier = Modifier.size(32.dp)
                    )
                }

                // Duration badge
                Box(
                    modifier = Modifier
                        .align(Alignment.BottomEnd)
                        .padding(10.dp)
                        .clip(RoundedCornerShape(6.dp))
                        .background(BgDark.copy(alpha = 0.85f))
                        .padding(horizontal = 8.dp, vertical = 4.dp)
                ) {
                    Text(
                        text = video.duration,
                        style = MaterialTheme.typography.labelSmall.copy(
                            color = Color.White,
                            fontWeight = FontWeight.Bold
                        )
                    )
                }
            }

            // Info
            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Text(
                    text = video.destination.uppercase(),
                    style = MaterialTheme.typography.labelSmall.copy(
                        color = GoldPrimary,
                        fontSize = 9.sp,
                        fontWeight = FontWeight.Bold,
                        letterSpacing = 1.sp
                    )
                )

                Text(
                    text = video.title,
                    style = MaterialTheme.typography.titleMedium.copy(
                        fontWeight = FontWeight.Bold,
                        color = TextPrimary
                    )
                )

                // Highlights pills
                Row(
                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    video.highlights.take(3).forEach { hl ->
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(100.dp))
                                .background(GlassSurface)
                                .border(1.dp, GlassBorder, RoundedCornerShape(100.dp))
                                .padding(horizontal = 8.dp, vertical = 4.dp)
                        ) {
                            Text(
                                text = "✦ $hl",
                                style = MaterialTheme.typography.labelSmall.copy(
                                    color = TextSecondary,
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

@Composable
fun InstagramPostCard(
    post: InstagramPost,
    onPostClick: () -> Unit
) {
    GlassCard(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onPostClick() }
            .testTag("ig_post_${post.id}"),
        borderColor = GlassBorder,
        backgroundColor = BgDarkCard
    ) {
        Column {
            // Header
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(14.dp),
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
                        text = if (post.channelType == ChannelType.FOOD) "🍜" else "📸",
                        fontSize = 14.sp
                    )
                }

                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = post.location,
                        style = MaterialTheme.typography.labelMedium.copy(
                            color = TextPrimary,
                            fontWeight = FontWeight.Bold
                        )
                    )
                    Text(
                        text = "Shared via ${post.handle}",
                        style = MaterialTheme.typography.labelSmall.copy(
                            color = TextTertiary,
                            fontSize = 11.sp
                        )
                    )
                }

                // Subtle link button
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(100.dp))
                        .background(GlassSurface)
                        .border(1.dp, GlassBorderStrong, RoundedCornerShape(100.dp))
                        .clickable { onPostClick() }
                        .padding(horizontal = 10.dp, vertical = 5.dp)
                ) {
                    Text(
                        text = "View Recco ↗",
                        style = MaterialTheme.typography.labelSmall.copy(
                            color = GoldPrimary,
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold
                        )
                    )
                }
            }

            // Image
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(260.dp)
            ) {
                AsyncImage(
                    model = post.imageUrl,
                    contentDescription = post.caption,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )
            }

            // Caption & Likes
            Column(
                modifier = Modifier.padding(14.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Default.Favorite,
                            contentDescription = "Likes",
                            tint = AccentRed,
                            modifier = Modifier.size(16.dp)
                        )
                        Text(
                            text = "${post.likesCount} likes",
                            style = MaterialTheme.typography.labelSmall.copy(
                                color = TextPrimary,
                                fontWeight = FontWeight.Bold
                            )
                        )
                    }

                    Text(
                        text = "Tap photo to open link",
                        style = MaterialTheme.typography.labelSmall.copy(
                            color = TextTertiary,
                            fontSize = 10.sp
                        )
                    )
                }

                Text(
                    text = post.caption,
                    style = MaterialTheme.typography.bodyMedium.copy(
                        color = TextSecondary,
                        lineHeight = 18.sp
                    )
                )
            }
        }
    }
}

@Composable
fun ChannelFilterPill(
    label: String,
    isSelected: Boolean,
    onClick: () -> Unit
) {
    Box(
        modifier = Modifier
            .clip(RoundedCornerShape(100.dp))
            .background(if (isSelected) Color(0x33E8C97A) else GlassSurface)
            .border(
                1.dp,
                if (isSelected) GoldPrimary else GlassBorder,
                RoundedCornerShape(100.dp)
            )
            .clickable { onClick() }
            .padding(horizontal = 12.dp, vertical = 6.dp)
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.labelSmall.copy(
                color = if (isSelected) GoldPrimary else TextSecondary,
                fontWeight = FontWeight.Bold
            )
        )
    }
}
