package com.example.ui.components

import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
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
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.GpsFixed
import androidx.compose.material.icons.filled.Navigation
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.model.StopLocation
import com.example.ui.theme.AccentGreen
import com.example.ui.theme.BgDark
import com.example.ui.theme.BgDarkSurface
import com.example.ui.theme.GlassBorder
import com.example.ui.theme.GoldPrimary
import com.example.ui.theme.GoldSecondary
import com.example.ui.theme.TextPrimary
import com.example.ui.theme.TextSecondary
import com.example.ui.theme.TextTertiary

@Composable
fun RouteMapVisualizer(
    stops: List<StopLocation>,
    currentStopIndex: Int,
    modifier: Modifier = Modifier
) {
    val infiniteTransition = rememberInfiniteTransition(label = "gpsPulse")
    val pulseScale by infiniteTransition.animateFloat(
        initialValue = 1f,
        targetValue = 2.4f,
        animationSpec = infiniteRepeatable(
            animation = tween(1800, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "pulseScale"
    )
    val pulseAlpha by infiniteTransition.animateFloat(
        initialValue = 0.6f,
        targetValue = 0f,
        animationSpec = infiniteRepeatable(
            animation = tween(1800, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "pulseAlpha"
    )

    Box(
        modifier = modifier
            .fillMaxWidth()
            .height(180.dp)
            .clip(RoundedCornerShape(20.dp))
            .background(
                brush = Brush.linearGradient(
                    listOf(Color(0xFF141A28), Color(0xFF0F1420))
                )
            )
            .border(1.dp, GlassBorder, RoundedCornerShape(20.dp))
    ) {
        // Custom Canvas drawing for GPS Route & Waypoints
        Canvas(modifier = Modifier.fillMaxSize()) {
            val canvasW = size.width
            val canvasH = size.height

            // 1. Draw subtle coordinate grid lines
            val gridSpacing = 32.dp.toPx()
            var x = 0f
            while (x < canvasW) {
                drawLine(
                    color = Color(0x12FFFFFF),
                    start = Offset(x, 0f),
                    end = Offset(x, canvasH),
                    strokeWidth = 1f
                )
                x += gridSpacing
            }
            var y = 0f
            while (y < canvasH) {
                drawLine(
                    color = Color(0x12FFFFFF),
                    start = Offset(0f, y),
                    end = Offset(canvasW, y),
                    strokeWidth = 1f
                )
                y += gridSpacing
            }

            // Waypoint positions calculation
            val numStops = stops.size.coerceAtLeast(1)
            val points = mutableListOf<Offset>()

            if (numStops == 1) {
                points.add(Offset(canvasW * 0.5f, canvasH * 0.5f))
            } else {
                stops.forEachIndexed { idx, _ ->
                    val frac = idx.toFloat() / (numStops - 1).coerceAtLeast(1)
                    val ptX = canvasW * 0.15f + frac * (canvasW * 0.7f)
                    val waveY = if (idx % 2 == 0) canvasH * 0.65f else canvasH * 0.35f
                    points.add(Offset(ptX, waveY))
                }
            }

            // 2. Draw curved route line connecting points
            if (points.size > 1) {
                val path = Path().apply {
                    moveTo(points[0].x, points[0].y)
                    for (i in 0 until points.size - 1) {
                        val p0 = points[i]
                        val p1 = points[i + 1]
                        val midX = (p0.x + p1.x) / 2
                        cubicTo(midX, p0.y, midX, p1.y, p1.x, p1.y)
                    }
                }

                // Path shadow glow
                drawPath(
                    path = path,
                    color = GoldPrimary.copy(alpha = 0.25f),
                    style = Stroke(width = 8.dp.toPx())
                )

                // Main route line
                drawPath(
                    path = path,
                    brush = Brush.horizontalGradient(
                        listOf(AccentGreen, GoldPrimary, GoldSecondary)
                    ),
                    style = Stroke(
                        width = 3.dp.toPx(),
                        pathEffect = PathEffect.dashPathEffect(floatArrayOf(20f, 10f), 0f)
                    )
                )
            }

            // 3. Draw Nodes / Waypoints
            points.forEachIndexed { index, pt ->
                val isCompleted = index < currentStopIndex
                val isCurrent = index == currentStopIndex
                val isUpcoming = index > currentStopIndex

                if (isCurrent) {
                    // Pulsing GPS Beacon
                    drawCircle(
                        color = GoldPrimary.copy(alpha = pulseAlpha),
                        radius = 16.dp.toPx() * pulseScale,
                        center = pt
                    )
                    drawCircle(
                        color = GoldPrimary,
                        radius = 8.dp.toPx(),
                        center = pt
                    )
                    drawCircle(
                        color = Color.White,
                        radius = 3.5.dp.toPx(),
                        center = pt
                    )
                } else if (isCompleted) {
                    drawCircle(
                        color = AccentGreen,
                        radius = 6.dp.toPx(),
                        center = pt
                    )
                    drawCircle(
                        color = BgDark,
                        radius = 3.dp.toPx(),
                        center = pt
                    )
                } else {
                    drawCircle(
                        color = GlassBorder,
                        radius = 6.dp.toPx(),
                        center = pt
                    )
                    drawCircle(
                        color = BgDarkSurface,
                        radius = 3.5.dp.toPx(),
                        center = pt
                    )
                }
            }
        }

        // Overlay Navigation Header
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(14.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                modifier = Modifier
                    .background(BgDark.copy(alpha = 0.8f), RoundedCornerShape(100.dp))
                    .padding(horizontal = 10.dp, vertical = 5.dp)
            ) {
                Icon(
                    imageVector = Icons.Default.Navigation,
                    contentDescription = null,
                    tint = GoldPrimary,
                    modifier = Modifier.size(13.dp)
                )
                Text(
                    text = "GPS ROUTE TRACKER",
                    style = MaterialTheme.typography.labelSmall.copy(
                        color = GoldSecondary,
                        fontWeight = FontWeight.Bold,
                        fontSize = 9.sp,
                        letterSpacing = 1.sp
                    )
                )
            }

            // Live distance indicator
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(6.dp),
                modifier = Modifier
                    .background(BgDark.copy(alpha = 0.8f), RoundedCornerShape(100.dp))
                    .padding(horizontal = 10.dp, vertical = 5.dp)
            ) {
                Box(
                    modifier = Modifier
                        .size(6.dp)
                        .clip(CircleShape)
                        .background(AccentGreen)
                )
                Text(
                    text = "NEXT: 450m · 6 min",
                    style = MaterialTheme.typography.labelSmall.copy(
                        color = TextPrimary,
                        fontWeight = FontWeight.Bold,
                        fontSize = 9.sp
                    )
                )
            }
        }

        // Active spot label bottom banner
        val activeStop = stops.getOrNull(currentStopIndex)
        if (activeStop != null) {
            Row(
                modifier = Modifier
                    .align(Alignment.BottomStart)
                    .fillMaxWidth()
                    .background(
                        Brush.verticalGradient(
                            listOf(Color.Transparent, BgDark.copy(alpha = 0.95f))
                        )
                    )
                    .padding(14.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Column {
                    Text(
                        text = "CURRENT TARGET STOP",
                        style = MaterialTheme.typography.labelSmall.copy(
                            color = GoldPrimary,
                            fontWeight = FontWeight.Bold,
                            fontSize = 8.sp,
                            letterSpacing = 1.2.sp
                        )
                    )
                    Text(
                        text = activeStop.name,
                        style = MaterialTheme.typography.labelLarge.copy(
                            color = TextPrimary,
                            fontWeight = FontWeight.Bold
                        )
                    )
                }
                Text(
                    text = activeStop.timing,
                    style = MaterialTheme.typography.labelSmall.copy(color = TextSecondary)
                )
            }
        }
    }
}
