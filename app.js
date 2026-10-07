// ComeTripWithMe - Core Web Application Controller

// Safe LocalStorage Helpers
function safeGetStorage(key, fallback) {
  try {
    const val = localStorage.getItem(key);
    return val ? JSON.parse(val) : fallback;
  } catch (e) {
    return fallback;
  }
}

function safeSetStorage(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch (e) {
    console.warn("Storage write skipped:", e);
  }
}

// State
const AppState = {
  currentTab: "explore", // explore, guide, proof, planner, saved
  selectedTrip: null,
  activeGuideTripId: "goa",
  activeGuideDayIndex: 0,
  activeAudioStory: null, // { story, spotName }
  inspectedSpot: null,
  instagramFilter: "ALL", // ALL, TRAVEL, FOOD
  smartMatch: {
    destinationId: "goa",
    budget: 15000,
    travelers: "2 of us 👫",
    date: ""
  },
  planner: {
    destination: "Goa",
    vibe: "PARTY",
    duration: 4,
    squad: "2 of us 👫",
    budget: 10000,
    notes: ""
  },
  wishlist: safeGetStorage("ctwm_wishlist", []),
  packingList: safeGetStorage("ctwm_packing", typeof DEFAULT_PACKING_LIST !== "undefined" ? DEFAULT_PACKING_LIST : [])
};

// Web Speech / Audio Controller
const VoiceGuide = {
  synth: window.speechSynthesis,
  utterance: null,
  isPlaying: false,
  timerInterval: null,
  secondsElapsed: 0,

  play: function(text, onEnd) {
    this.stop();
    if (!this.synth) return;

    this.utterance = new SpeechSynthesisUtterance(text);
    this.utterance.rate = 0.95;
    this.utterance.pitch = 1.0;
    
    // Pick an English voice if available
    const voices = this.synth.getVoices();
    const englishVoice = voices.find(v => v.lang.includes("en-IN") || v.lang.includes("en-GB") || v.lang.includes("en-US"));
    if (englishVoice) this.utterance.voice = englishVoice;

    this.isPlaying = true;
    this.secondsElapsed = 0;
    
    this.utterance.onend = () => {
      this.isPlaying = false;
      this.clearInterval();
      if (onEnd) onEnd();
      updateAudioPlayerUI();
    };

    this.utterance.onerror = () => {
      this.isPlaying = false;
      this.clearInterval();
      updateAudioPlayerUI();
    };

    this.synth.speak(this.utterance);
    this.startInterval();
    updateAudioPlayerUI();
  },

  pause: function() {
    if (this.synth && this.isPlaying) {
      this.synth.pause();
      this.isPlaying = false;
      this.clearInterval();
      updateAudioPlayerUI();
    }
  },

  resume: function() {
    if (this.synth && !this.isPlaying && this.utterance) {
      this.synth.resume();
      this.isPlaying = true;
      this.startInterval();
      updateAudioPlayerUI();
    }
  },

  stop: function() {
    if (this.synth) {
      this.synth.cancel();
      this.isPlaying = false;
      this.clearInterval();
      this.secondsElapsed = 0;
      updateAudioPlayerUI();
    }
  },

  startInterval: function() {
    this.clearInterval();
    this.timerInterval = setInterval(() => {
      if (this.isPlaying) {
        this.secondsElapsed++;
        updateAudioPlayerUI();
      }
    }, 1000);
  },

  clearInterval: function() {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }
  }
};

// Initializer
document.addEventListener("DOMContentLoaded", () => {
  initNavigation();
  renderApp();
  renderSmartMatchRecommendation();
});

// Navigation Controller
function initNavigation() {
  const desktopButtons = document.querySelectorAll(".nav-tab-btn");
  const mobileButtons = document.querySelectorAll(".mobile-nav-item");

  desktopButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      setTab(btn.dataset.tab);
    });
  });

  mobileButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      setTab(btn.dataset.tab);
    });
  });
}

function setTab(tabName) {
  AppState.currentTab = tabName;

  // Update Nav UI
  document.querySelectorAll(".nav-tab-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.tab === tabName);
  });
  document.querySelectorAll(".mobile-nav-item").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.tab === tabName);
  });

  // Render Target Screen
  renderApp();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// Master Render
function renderApp() {
  const container = document.getElementById("main-content");
  if (!container) return;

  switch (AppState.currentTab) {
    case "explore":
      container.innerHTML = renderExploreScreen();
      attachExploreEvents();
      break;
    case "guide":
      container.innerHTML = renderPocketGuideScreen();
      attachGuideEvents();
      break;
    case "proof":
      container.innerHTML = renderProofScreen();
      attachProofEvents();
      break;
    case "planner":
      container.innerHTML = renderPlannerScreen();
      attachPlannerEvents();
      break;
    case "saved":
      container.innerHTML = renderSavedScreen();
      attachSavedEvents();
      break;
  }

  // Refresh lucide icons if loaded
  if (window.lucide) {
    lucide.createIcons();
  }
}

// ==========================================================================
// 1. EXPLORE SCREEN
// ==========================================================================
function renderExploreScreen() {
  const tripsHtml = CURATED_TRIPS.map(trip => {
    const isSaved = AppState.wishlist.includes(trip.id);
    const vibe = TRIP_VIBES[trip.vibe] || TRIP_VIBES.CHILL;
    return `
      <div class="glass-card trip-card" onclick="openTripDetail('${trip.id}')">
        <div class="trip-img-wrap">
          <img src="${trip.imageUrl}" alt="${trip.name}" class="trip-img" loading="lazy" />
          <div class="trip-img-overlay"></div>
          <div class="trip-top-badges">
            <span class="pill-badge" style="background: ${vibe.color}22; border-color: ${vibe.color}66; color: ${vibe.color}">
              ${vibe.emoji} ${vibe.label}
            </span>
            <button class="wishlist-btn ${isSaved ? 'active' : ''}" onclick="event.stopPropagation(); toggleWishlist('${trip.id}')" title="Save Trip">
              <i data-lucide="${isSaved ? 'heart' : 'heart'}" style="${isSaved ? 'fill: #DC503C' : ''}"></i>
            </button>
          </div>
        </div>
        <div class="trip-body">
          <div style="display: flex; justify-content: space-between; align-items: baseline;">
            <h3 class="trip-title">${trip.name}</h3>
            <span style="font-size: 0.8rem; font-weight: 700; color: var(--gold-secondary)">${trip.duration}</span>
          </div>
          <p class="trip-headline">${trip.headline}</p>
          <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px;">
            ${trip.heroTags.map(tag => `<span style="font-size: 0.72rem; padding: 3px 8px; border-radius: 6px; background: rgba(255,255,255,0.05); color: var(--text-secondary);">${tag}</span>`).join('')}
          </div>
          <div class="trip-footer">
            <div>
              <div class="trip-price-sub">Est. Expense</div>
              <div class="trip-price">${trip.price} <span style="font-size: 0.8rem; font-weight: 400; color: var(--text-tertiary)">/ person</span></div>
            </div>
            <button class="btn-gold" style="padding: 8px 16px; font-size: 0.85rem;" onclick="event.stopPropagation(); startGuide('${trip.id}')">
              Live Guide <i data-lucide="compass" style="width: 16px; height: 16px;"></i>
            </button>
          </div>
        </div>
      </div>
    `;
  }).join("");

  const spotlightsHtml = SPOTLIGHTS.map(spot => `
    <div class="glass-card" style="padding: 20px; display: flex; flex-direction: column; gap: 12px; cursor: pointer;" onclick="openSpotlight('${spot.id}')">
      <div style="height: 160px; border-radius: 12px; overflow: hidden; position: relative;">
        <img src="${spot.imageUrl}" alt="${spot.title}" style="width: 100%; height: 100%; object-fit: cover;" loading="lazy" />
        <div style="position: absolute; bottom: 10px; left: 10px; background: rgba(0,0,0,0.7); padding: 3px 10px; border-radius: 9999px; font-size: 0.75rem; color: var(--gold-primary); font-weight: 700;">
          ${spot.documentedSpotsCount}
        </div>
      </div>
      <div>
        <div style="font-size: 0.75rem; color: var(--text-tertiary); text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em;">${spot.region}</div>
        <h4 style="font-size: 1.15rem; margin: 4px 0 2px;">${spot.title}</h4>
        <p style="font-size: 0.85rem; color: var(--text-secondary);">${spot.subtitle}</p>
      </div>
      <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: auto;">
        ${spot.tags.map(t => `<span style="font-size: 0.7rem; background: var(--glass-surface); border: 1px solid var(--glass-border); padding: 2px 8px; border-radius: 4px; color: var(--text-secondary);">${t}</span>`).join('')}
      </div>
    </div>
  `).join("");

  const reviewsHtml = TRAVELER_REVIEWS.map(r => `
    <div class="glass-card" style="padding: 24px;">
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
        <div>
          <div style="font-weight: 700; color: var(--text-primary); font-size: 0.95rem;">${r.authorHandle}</div>
          <div style="font-size: 0.75rem; color: var(--text-tertiary);">${r.city} · <span style="color: var(--gold-secondary)">${r.tripTag}</span></div>
        </div>
        <div style="color: #F59E0B; font-size: 0.9rem;">★★★★★</div>
      </div>
      <p style="font-size: 0.9rem; color: var(--text-secondary); font-style: italic; line-height: 1.5;">"${r.reviewQuote}"</p>
    </div>
  `).join("");

  return `
    <!-- Hero Section -->
    <div class="hero-card">
      <img src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1400&q=80" alt="Hero" class="hero-bg" />
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <span class="pill-badge">✦ India's 1st Creator-Led Tour Operator</span>
        <h1 class="hero-title">YOUR NEXT TRIP, SORTED.</h1>
        <p class="hero-sub">
          Real trips. Real places. 100% creator-led. No copy-paste agency fluff. Curated by Bengaluru creators who've actually been there.
        </p>
        <div style="display: flex; gap: 14px; flex-wrap: wrap;">
          <button class="btn-gold" onclick="setTab('planner')">
            Plan My Trip <i data-lucide="arrow-right" style="width: 18px; height: 18px;"></i>
          </button>
          <button class="btn-secondary" onclick="surpriseMe()">
            Surprise Me 🎲
          </button>
        </div>
        <div class="hero-stats">
          <div>
            <div class="hero-stat-num">50+</div>
            <div class="hero-stat-lbl">Verified Spots</div>
          </div>
          <div>
            <div class="hero-stat-num">100%</div>
            <div class="hero-stat-lbl">Creator-Led</div>
          </div>
          <div>
            <div class="hero-stat-num">0</div>
            <div class="hero-stat-lbl">Tourist Traps</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Live Marquee Ticker -->
    <div class="marquee-container">
      <div class="marquee-track">
        <div class="marquee-item">No Tourist Traps <span class="dot">✦</span></div>
        <div class="marquee-item">Goa Secret Shacks <span class="dot">✦</span></div>
        <div class="marquee-item">Thailand Street Food <span class="dot">✦</span></div>
        <div class="marquee-item">Krabi Emerald Caves <span class="dot">✦</span></div>
        <div class="marquee-item">Himachal Riverside Cafés <span class="dot">✦</span></div>
        <div class="marquee-item">Malaysia & Penang Food Trail <span class="dot">✦</span></div>
        <div class="marquee-item">Pondicherry Heritage Cycle <span class="dot">✦</span></div>
        <div class="marquee-item">Gokarna Cliff Hikes <span class="dot">✦</span></div>
        <div class="marquee-item">Bengaluru To The World <span class="dot">✦</span></div>
      </div>
    </div>

    <!-- Smart Trip Matcher Card -->
    <div class="glass-card-gold" style="padding: 28px; margin-bottom: 36px;">
      <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; margin-bottom: 18px;">
        <div>
          <span class="pill-badge" style="margin-bottom: 6px;">✦ Instant Match</span>
          <h2 style="font-size: 1.6rem; color: var(--text-primary);">Find Your Perfect Route</h2>
        </div>
        <span style="font-size: 0.85rem; color: var(--text-secondary);">Tell me your vibe & budget. I'll match you instantly.</span>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 20px;">
        <div>
          <label style="display: block; font-size: 0.75rem; font-weight: 700; color: var(--gold-primary); text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.05em;">Where To?</label>
          <select id="smart-dest-select" style="width: 100%; background: var(--bg-dark-elevated); color: var(--text-primary); border: 1px solid var(--glass-border); padding: 12px 16px; border-radius: 12px; font-weight: 600; outline: none;">
            <option value="goa" ${AppState.smartMatch.destinationId === 'goa' ? 'selected' : ''}>🎉 Goa (Beaches & Shacks)</option>
            <option value="thailand" ${AppState.smartMatch.destinationId === 'thailand' ? 'selected' : ''}>🌴 Thailand (Bangkok & Krabi)</option>
            <option value="himachal" ${AppState.smartMatch.destinationId === 'himachal' ? 'selected' : ''}>🏔️ Himachal (Kasol & Kheerganga)</option>
            <option value="pondicherry" ${AppState.smartMatch.destinationId === 'pondicherry' ? 'selected' : ''}>🛕 Pondicherry (French Quarter)</option>
            <option value="malaysia" ${AppState.smartMatch.destinationId === 'malaysia' ? 'selected' : ''}>🌆 Malaysia (KL & Penang)</option>
            <option value="krabi" ${AppState.smartMatch.destinationId === 'krabi' ? 'selected' : ''}>🏝️ Krabi (Limestone Lagoons)</option>
            <option value="gokarna" ${AppState.smartMatch.destinationId === 'gokarna' ? 'selected' : ''}>🏖️ Gokarna (5-Beach Trek)</option>
          </select>
        </div>

        <div>
          <label style="display: block; font-size: 0.75rem; font-weight: 700; color: var(--gold-primary); text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.05em;">Budget (₹/person)</label>
          <select id="smart-budget-select" style="width: 100%; background: var(--bg-dark-elevated); color: var(--text-primary); border: 1px solid var(--glass-border); padding: 12px 16px; border-radius: 12px; font-weight: 600; outline: none;">
            <option value="5000" ${AppState.smartMatch.budget === 5000 ? 'selected' : ''}>Under ₹5,000</option>
            <option value="15000" ${AppState.smartMatch.budget === 15000 ? 'selected' : ''}>₹5,000 – ₹15,000</option>
            <option value="30000" ${AppState.smartMatch.budget === 30000 ? 'selected' : ''}>₹15,000 – ₹30,000</option>
            <option value="50000" ${AppState.smartMatch.budget === 50000 ? 'selected' : ''}>₹30,000 – ₹50,000+</option>
          </select>
        </div>
      </div>

      <!-- Recommendation Display Banner -->
      <div id="smart-rec-banner" style="background: rgba(232, 201, 122, 0.1); border: 1px solid var(--glass-border-gold); border-radius: 16px; padding: 18px; margin-bottom: 20px;">
        <div style="font-size: 0.75rem; font-weight: 700; color: var(--gold-primary); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px;">✦ Smart Recommendation</div>
        <div id="smart-rec-title" style="font-size: 1.15rem; font-weight: 700; color: var(--text-primary);">Goa Long Weekend — ₹8,999/person</div>
        <div id="smart-rec-sub" style="font-size: 0.9rem; color: var(--text-secondary); margin-top: 2px;">4 nights, North + South Goa blend. Thalassa sunset, Chapora cliff views, and pristine Palolem silence.</div>
      </div>

      <button class="btn-gold" style="width: 100%;" onclick="viewMatchedTrip()">
        View Matching Itinerary →
      </button>
    </div>

    <!-- Curated Itineraries Section -->
    <div style="margin-bottom: 40px;">
      <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 24px;">
        <div>
          <span class="pill-badge">Curated Itineraries</span>
          <h2 style="font-size: 2rem; margin-top: 8px;">Trips That Actually Slap.</h2>
          <p style="color: var(--text-secondary); font-size: 0.95rem;">Every route built from real experience. Not an agency brochure.</p>
        </div>
      </div>
      <div class="trips-grid">
        ${tripsHtml}
      </div>
    </div>

    <!-- Destination Spotlights -->
    <div style="margin-bottom: 40px;">
      <div style="margin-bottom: 20px;">
        <span class="pill-badge">Spotlights</span>
        <h2 style="font-size: 1.8rem; margin-top: 6px;">Region Deep Dives</h2>
      </div>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px;">
        ${spotlightsHtml}
      </div>
    </div>

    <!-- Why Us Section -->
    <div class="glass-card" style="padding: 36px 28px; margin-bottom: 40px;">
      <div style="text-align: center; max-width: 600px; margin: 0 auto 32px;">
        <span class="pill-badge">Why ComeTripWithMe</span>
        <h2 style="font-size: 1.8rem; margin-top: 8px;">The Anti-Tourist Operator</h2>
        <p style="color: var(--text-secondary); font-size: 0.9rem;">We don't send you to 4-star buffets with bus tour crowds.</p>
      </div>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 24px;">
        <div style="display: flex; flex-direction: column; gap: 8px;">
          <div style="font-size: 1.8rem;">🎥</div>
          <h3 style="font-size: 1.1rem; color: var(--gold-primary);">Real Video Proof</h3>
          <p style="font-size: 0.85rem; color: var(--text-secondary);">Over 800GB of 4K drone & POV footage verifying every single cliff, café and shack.</p>
        </div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
          <div style="font-size: 1.8rem;">🚫</div>
          <h3 style="font-size: 1.1rem; color: var(--gold-primary);">Zero Agency Markups</h3>
          <p style="font-size: 0.85rem; color: var(--text-secondary);">Direct scooty rentals, local ferry ticket booths, and authentic street food prices.</p>
        </div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
          <div style="font-size: 1.8rem;">📱</div>
          <h3 style="font-size: 1.1rem; color: var(--gold-primary);">Live Pocket Guide</h3>
          <p style="font-size: 0.85rem; color: var(--text-secondary);">GPS stops, real audio stories, and instant WhatsApp support right in your pocket.</p>
        </div>
      </div>
    </div>

    <!-- Traveler Reviews -->
    <div style="margin-bottom: 40px;">
      <div style="margin-bottom: 20px;">
        <span class="pill-badge">Verified Reviews</span>
        <h2 style="font-size: 1.8rem; margin-top: 6px;">Travelers Who Walked The Route</h2>
      </div>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
        ${reviewsHtml}
      </div>
    </div>

    <!-- CTA Band -->
    <div class="glass-card-gold" style="padding: 40px 32px; text-align: center; margin-bottom: 40px;">
      <h2 style="font-size: 2rem; margin-bottom: 12px;">Ready To Experience Travel Differently?</h2>
      <p style="color: var(--text-secondary); max-width: 600px; margin: 0 auto 24px; font-size: 1rem;">
        Get your custom itinerary sorted over WhatsApp within a few hours. Tell us where you want to go.
      </p>
      <div style="display: flex; justify-content: center; gap: 14px; flex-wrap: wrap;">
        <button class="btn-gold" onclick="openWhatsApp('Hey ComeTripWithMe! I want to plan an epic trip.')">
          Chat On WhatsApp 💬
        </button>
        <button class="btn-secondary" onclick="openPhone()">
          Call 9742311023 📞
        </button>
      </div>
    </div>

    <!-- Footer -->
    <footer style="border-top: 1px solid var(--glass-border); padding-top: 32px; display: flex; flex-direction: column; gap: 24px;">
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px;">
        <div>
          <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
            <div class="brand-symbol" style="width: 30px; height: 30px; font-size: 1rem;">✦</div>
            <span style="font-weight: 800; color: var(--gold-primary); letter-spacing: 0.1em;">COMETRIPWITHME</span>
          </div>
          <p style="font-size: 0.8rem; color: var(--text-tertiary);">Curated by @beyondbengalurufoods & @cometriipwme</p>
        </div>
        <div style="display: flex; gap: 12px;">
          <button class="btn-secondary" style="padding: 8px 16px; font-size: 0.85rem;" onclick="openInstagram('cometriipwme')">📸 @cometriipwme</button>
          <button class="btn-secondary" style="padding: 8px 16px; font-size: 0.85rem;" onclick="openInstagram('beyondbengalurufoods')">🍜 @beyondbengalurufoods</button>
        </div>
      </div>
      <div style="text-align: center; font-size: 0.8rem; color: var(--text-tertiary); padding-bottom: 20px;">
        © 2026 ComeTripWithMe. All rights reserved. India's 1st Creator Tour Operator.
      </div>
    </footer>
  `;
}

function attachExploreEvents() {
  const destSelect = document.getElementById("smart-dest-select");
  const budgetSelect = document.getElementById("smart-budget-select");

  if (destSelect) {
    destSelect.addEventListener("change", (e) => {
      AppState.smartMatch.destinationId = e.target.value;
      renderSmartMatchRecommendation();
    });
  }

  if (budgetSelect) {
    budgetSelect.addEventListener("change", (e) => {
      AppState.smartMatch.budget = parseInt(e.target.value);
      renderSmartMatchRecommendation();
    });
  }
}

function renderSmartMatchRecommendation() {
  const rec = getSmartMatchRecommendation(AppState.smartMatch.destinationId, AppState.smartMatch.budget);
  const titleEl = document.getElementById("smart-rec-title");
  const subEl = document.getElementById("smart-rec-sub");

  if (rec && titleEl && subEl) {
    titleEl.innerText = rec.title;
    subEl.innerText = rec.sub;
  }
}

function viewMatchedTrip() {
  const target = CURATED_TRIPS.find(t => t.id === AppState.smartMatch.destinationId) || CURATED_TRIPS[0];
  openTripDetail(target.id);
}

// ==========================================================================
// 2. POCKET GUIDE SCREEN
// ==========================================================================
function renderPocketGuideScreen() {
  const trip = CURATED_TRIPS.find(t => t.id === AppState.activeGuideTripId) || CURATED_TRIPS[0];
  const dayIndex = Math.min(AppState.activeGuideDayIndex, trip.days.length - 1);
  const dayPlan = trip.days[dayIndex] || trip.days[0];

  const dayPillsHtml = trip.days.map((d, i) => `
    <button class="day-pill ${i === dayIndex ? 'active' : ''}" onclick="setGuideDay(${i})">
      Day ${d.dayNumber}: ${d.title.split(' ')[0]}
    </button>
  `).join("");

  const stopsHtml = dayPlan.stops.map((stop, sIdx) => {
    return `
      <div class="glass-card" style="padding: 18px; margin-bottom: 14px; cursor: pointer;" onclick="inspectSpot('${stop.id}')">
        <div style="display: flex; align-items: center; justify-content: space-between; gap: 14px;">
          <div style="display: flex; align-items: center; gap: 14px;">
            <div style="width: 36px; height: 36px; border-radius: 50%; background: var(--gold-container); border: 1px solid var(--glass-border-gold); color: var(--gold-primary); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.9rem;">
              ${sIdx + 1}
            </div>
            <div>
              <h4 style="font-size: 1.05rem; font-weight: 700;">${stop.name}</h4>
              <div style="font-size: 0.8rem; color: var(--text-tertiary);">${stop.timing} · <span style="color: var(--gold-secondary)">${stop.category}</span></div>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            ${stop.audioStory ? `
              <button class="wishlist-btn" onclick="event.stopPropagation(); playAudioStory('${stop.id}')" title="Listen to Audio Story">
                <i data-lucide="headphones" style="color: var(--gold-primary);"></i>
              </button>
            ` : ''}
            <i data-lucide="chevron-right" style="color: var(--text-tertiary);"></i>
          </div>
        </div>
      </div>
    `;
  }).join("");

  const foodHtml = dayPlan.foodSpots ? dayPlan.foodSpots.map(f => `
    <div class="glass-card" style="padding: 16px; margin-bottom: 12px; cursor: pointer;" onclick="openInstagramReel('${f.reelUrl}')">
      <div style="display: flex; gap: 14px; align-items: center;">
        <img src="${f.reelThumbnailUrl}" alt="${f.name}" style="width: 76px; height: 76px; object-fit: cover; border-radius: 12px;" loading="lazy" />
        <div style="flex: 1;">
          <div style="display: flex; justify-content: space-between; align-items: baseline;">
            <h4 style="font-size: 1rem;">${f.name}</h4>
            <span style="font-size: 0.75rem; color: var(--gold-primary); font-weight: 700;">▶ Reel</span>
          </div>
          <div style="font-size: 0.8rem; color: var(--text-secondary); margin: 2px 0;">Must Try: <strong style="color: var(--text-primary);">${f.mustTryDish}</strong></div>
          <div style="font-size: 0.75rem; color: var(--text-tertiary);">${f.approxCostForTwo} · by ${f.recommendedBy}</div>
        </div>
      </div>
    </div>
  `).join("") : "";

  const packingItemsHtml = AppState.packingList.map(item => `
    <div style="display: flex; align-items: center; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--glass-border);">
      <label style="display: flex; align-items: center; gap: 12px; cursor: pointer; flex: 1;">
        <input type="checkbox" ${item.checked ? 'checked' : ''} onchange="togglePacking('${item.id}')" style="accent-color: var(--gold-primary); width: 18px; height: 18px;" />
        <span style="font-size: 0.9rem; color: ${item.checked ? 'var(--text-muted)' : 'var(--text-primary)'}; text-decoration: ${item.checked ? 'line-through' : 'none'};">${item.title}</span>
      </label>
      <span style="font-size: 0.75rem; color: var(--text-tertiary);">${item.category}</span>
    </div>
  `).join("");

  return `
    <div style="margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
      <div>
        <span class="live-badge">GPS Guide Live</span>
        <h1 style="font-size: 2rem; margin-top: 6px;">${trip.name} Pocket Companion</h1>
      </div>
      <button class="btn-secondary" onclick="openTripSelectorModal()">
        Switch Destination (${trip.name}) ▾
      </button>
    </div>

    <!-- Day Pills -->
    <div class="day-pills-scroll">
      ${dayPillsHtml}
    </div>

    <!-- Active Audio Tour Player -->
    <div id="audio-player-mount">
      ${renderAudioPlayerHtml()}
    </div>

    <!-- SVG Route Map Visualizer -->
    <div class="route-map-container">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
        <span style="font-size: 0.8rem; font-weight: 700; color: var(--gold-primary); text-transform: uppercase;">✦ Day ${dayPlan.dayNumber} Route Map</span>
        <span style="font-size: 0.8rem; color: var(--text-secondary);">${dayPlan.stops.length} Stops Sequence</span>
      </div>
      <div id="route-svg-mount">
        ${renderRouteSvg(dayPlan.stops)}
      </div>
    </div>

    <!-- Day Summary Card -->
    <div class="glass-card-gold" style="padding: 20px; margin-bottom: 24px;">
      <div style="font-size: 0.75rem; font-weight: 700; color: var(--gold-primary); text-transform: uppercase; margin-bottom: 4px;">Day ${dayPlan.dayNumber}: ${dayPlan.title}</div>
      <p style="font-size: 0.95rem; color: var(--text-primary); line-height: 1.5;">${dayPlan.summary}</p>
      ${dayPlan.creatorSecretTip ? `
        <div style="margin-top: 12px; padding: 10px 14px; background: rgba(0,0,0,0.3); border-radius: 10px; font-size: 0.85rem; color: var(--gold-secondary);">
          ⚡ Creator Secret Tip: ${dayPlan.creatorSecretTip}
        </div>
      ` : ''}
    </div>

    <!-- Timeline of Stops -->
    <div style="margin-bottom: 32px;">
      <div style="font-size: 0.8rem; font-weight: 700; color: var(--text-tertiary); text-transform: uppercase; margin-bottom: 14px; letter-spacing: 0.05em;">Today's Stops</div>
      ${stopsHtml}
    </div>

    <!-- Inspected Spot Deep Dive Mount -->
    <div id="inspected-spot-mount">
      ${renderInspectedSpotHtml()}
    </div>

    <!-- Food Recommendations with Reels -->
    ${foodHtml ? `
      <div style="margin-bottom: 32px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
          <span style="font-size: 0.8rem; font-weight: 700; color: var(--gold-primary); text-transform: uppercase;">Food & Cafés (@beyondbengalurufoods)</span>
          <span style="font-size: 0.8rem; color: var(--gold-secondary);">Watch Reel ↗</span>
        </div>
        ${foodHtml}
      </div>
    ` : ''}

    <!-- Packing Checklist -->
    <div class="glass-card" style="padding: 24px; margin-bottom: 40px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <div>
          <span style="font-size: 0.8rem; font-weight: 700; color: var(--gold-primary); text-transform: uppercase;">🎒 Packing Essentials</span>
          <div style="font-size: 0.85rem; color: var(--text-tertiary);">${AppState.packingList.filter(p => p.checked).length}/${AppState.packingList.length} Items Packed</div>
        </div>
        <button class="btn-secondary" style="padding: 6px 14px; font-size: 0.8rem;" onclick="addPackingPrompt()">+ Add Item</button>
      </div>
      <div>
        ${packingItemsHtml}
      </div>
    </div>
  `;
}

function attachGuideEvents() {}

function renderAudioPlayerHtml() {
  if (!AppState.activeAudioStory) return "";
  const { story, spotName } = AppState.activeAudioStory;

  return `
    <div class="audio-player-card">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
        <div>
          <span class="live-badge" style="margin-bottom: 4px;">Audio Tour Guide</span>
          <h3 style="font-size: 1.15rem; color: var(--gold-primary); margin-top: 4px;">${story.title}</h3>
          <div style="font-size: 0.8rem; color: var(--text-tertiary);">📍 ${spotName} · Narrated by ${story.narrator}</div>
        </div>
        <button class="wishlist-btn" onclick="dismissAudioStory()" title="Close Player">
          <i data-lucide="x"></i>
        </button>
      </div>

      <div style="background: rgba(0,0,0,0.4); padding: 14px; border-radius: 12px; margin-bottom: 14px; font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5; max-height: 120px; overflow-y: auto;">
        "${story.scriptText}"
      </div>

      <div style="display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 14px;">
          <button class="btn-gold" style="width: 44px; height: 44px; padding: 0; border-radius: 50%;" onclick="toggleAudioVoice()">
            <i data-lucide="${VoiceGuide.isPlaying ? 'pause' : 'play'}"></i>
          </button>
          <div class="audio-waveform ${VoiceGuide.isPlaying ? 'playing' : ''}">
            <div class="waveform-bar"></div>
            <div class="waveform-bar"></div>
            <div class="waveform-bar"></div>
            <div class="waveform-bar"></div>
            <div class="waveform-bar"></div>
            <div class="waveform-bar"></div>
          </div>
        </div>
        <span style="font-size: 0.8rem; color: var(--text-tertiary);">${VoiceGuide.secondsElapsed}s / ${story.durationSeconds}s</span>
      </div>
    </div>
  `;
}

function updateAudioPlayerUI() {
  const mount = document.getElementById("audio-player-mount");
  if (mount) {
    mount.innerHTML = renderAudioPlayerHtml();
    if (window.lucide) lucide.createIcons();
  }
}

function renderRouteSvg(stops) {
  if (!stops || stops.length === 0) return "";

  const width = 800;
  const height = 140;
  const paddingX = 60;
  const stepX = (width - paddingX * 2) / Math.max(stops.length - 1, 1);

  let pathD = "";
  const points = stops.map((s, i) => {
    const x = paddingX + i * stepX;
    const y = 70 + (i % 2 === 0 ? -25 : 25);
    return { x, y, name: s.name, category: s.category };
  });

  points.forEach((p, i) => {
    if (i === 0) pathD += `M ${p.x} ${p.y}`;
    else pathD += ` L ${p.x} ${p.y}`;
  });

  return `
    <svg viewBox="0 0 ${width} ${height}" class="route-svg" style="background: rgba(0,0,0,0.3); border-radius: 12px; width: 100%;">
      <!-- Background Connecting Line -->
      <path d="${pathD}" fill="none" stroke="rgba(232, 201, 122, 0.3)" stroke-width="3" stroke-dasharray="6,6" />
      
      <!-- Nodes -->
      ${points.map((p, i) => `
        <g style="cursor: pointer;" onclick="inspectSpot('${stops[i].id}')">
          <circle cx="${p.x}" cy="${p.y}" r="16" fill="#10141E" stroke="#E8C97A" stroke-width="2" />
          <text x="${p.x}" y="${p.y + 4}" text-anchor="middle" fill="#E8C97A" font-size="11" font-weight="bold">${i + 1}</text>
          <text x="${p.x}" y="${p.y > 70 ? p.y + 24 : p.y - 18}" text-anchor="middle" fill="#F3F4F6" font-size="10" font-weight="600">${p.name.length > 14 ? p.name.substring(0, 14) + '...' : p.name}</text>
        </g>
      `).join("")}
    </svg>
  `;
}

function renderInspectedSpotHtml() {
  if (!AppState.inspectedSpot) return "";
  const spot = AppState.inspectedSpot;

  return `
    <div class="glass-card-gold" style="padding: 24px; margin-bottom: 24px; animation: slide-down 0.25s ease;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
        <div>
          <span style="font-size: 0.75rem; font-weight: 700; color: var(--gold-primary); text-transform: uppercase;">📍 Deep Dive Intel</span>
          <h3 style="font-size: 1.4rem; color: var(--text-primary); margin-top: 4px;">${spot.name}</h3>
          <div style="font-size: 0.85rem; color: var(--text-tertiary);">${spot.timing} · ${spot.category}</div>
        </div>
        <button class="wishlist-btn" onclick="dismissInspectedSpot()">
          <i data-lucide="x"></i>
        </button>
      </div>
      <p style="font-size: 0.95rem; color: var(--text-secondary); line-height: 1.5; margin-bottom: 14px;">${spot.description}</p>
      ${spot.insiderTip ? `
        <div style="background: rgba(0,0,0,0.4); border-left: 3px solid var(--gold-primary); padding: 12px; border-radius: 0 8px 8px 0; font-size: 0.9rem; color: var(--gold-secondary); margin-bottom: 16px;">
          ⚡ Insider Advice: ${spot.insiderTip}
        </div>
      ` : ''}
      <div style="display: flex; gap: 10px; flex-wrap: wrap;">
        ${spot.audioStory ? `
          <button class="btn-gold" onclick="playAudioStory('${spot.id}')">
            Listen To Audio Story <i data-lucide="headphones" style="width: 16px; height: 16px;"></i>
          </button>
        ` : ''}
        <button class="btn-secondary" onclick="openGoogleMaps('${spot.name}')">
          Open In Google Maps ↗
        </button>
      </div>
    </div>
  `;
}

function inspectSpot(spotId) {
  const trip = CURATED_TRIPS.find(t => t.id === AppState.activeGuideTripId) || CURATED_TRIPS[0];
  let found = null;
  trip.days.forEach(d => {
    const s = d.stops.find(st => st.id === spotId);
    if (s) found = s;
  });

  AppState.inspectedSpot = found;
  const mount = document.getElementById("inspected-spot-mount");
  if (mount) {
    mount.innerHTML = renderInspectedSpotHtml();
    if (window.lucide) lucide.createIcons();
    mount.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }
}

function dismissInspectedSpot() {
  AppState.inspectedSpot = null;
  const mount = document.getElementById("inspected-spot-mount");
  if (mount) mount.innerHTML = "";
}

function setGuideDay(index) {
  AppState.activeGuideDayIndex = index;
  renderApp();
}

function playAudioStory(spotId) {
  const trip = CURATED_TRIPS.find(t => t.id === AppState.activeGuideTripId) || CURATED_TRIPS[0];
  let found = null;
  trip.days.forEach(d => {
    const s = d.stops.find(st => st.id === spotId);
    if (s && s.audioStory) found = { story: s.audioStory, spotName: s.name };
  });

  if (found) {
    AppState.activeAudioStory = found;
    updateAudioPlayerUI();
    VoiceGuide.play(found.story.scriptText);
    showToast(`Playing Audio Story: ${found.story.title}`);
  }
}

function toggleAudioVoice() {
  if (VoiceGuide.isPlaying) {
    VoiceGuide.pause();
  } else {
    if (VoiceGuide.utterance) {
      VoiceGuide.resume();
    } else if (AppState.activeAudioStory) {
      VoiceGuide.play(AppState.activeAudioStory.story.scriptText);
    }
  }
}

function dismissAudioStory() {
  VoiceGuide.stop();
  AppState.activeAudioStory = null;
  updateAudioPlayerUI();
}

function startGuide(tripId) {
  AppState.activeGuideTripId = tripId;
  AppState.activeGuideDayIndex = 0;
  setTab("guide");
  showToast(`Live Pocket Guide Active for ${tripId.toUpperCase()} ✦`);
}

// ==========================================================================
// 3. PROOF & VIDEOS SCREEN
// ==========================================================================
function renderProofScreen() {
  const videosHtml = VIDEOS.map(v => `
    <div class="glass-card" style="padding: 18px; display: flex; flex-direction: column; gap: 12px; cursor: pointer;" onclick="openYouTube('${v.videoUrl}')">
      <div style="position: relative; height: 180px; border-radius: 12px; overflow: hidden;">
        <img src="${v.thumbnailUrl}" alt="${v.title}" style="width: 100%; height: 100%; object-fit: cover;" loading="lazy" />
        <div style="position: absolute; inset: 0; background: rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center;">
          <div style="width: 48px; height: 48px; border-radius: 50%; background: rgba(232, 201, 122, 0.9); color: var(--bg-dark); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; box-shadow: 0 0 20px rgba(0,0,0,0.6);">
            ▶
          </div>
        </div>
        <div style="position: absolute; bottom: 8px; right: 8px; background: rgba(0,0,0,0.8); padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; color: #fff;">
          ${v.duration}
        </div>
      </div>
      <div>
        <div style="font-size: 0.75rem; color: var(--gold-secondary); font-weight: 700; text-transform: uppercase;">${v.destination} · ${v.views}</div>
        <h3 style="font-size: 1.05rem; margin: 4px 0 6px;">${v.title}</h3>
        <ul style="list-style: none; font-size: 0.8rem; color: var(--text-secondary); display: flex; flex-direction: column; gap: 4px;">
          ${v.highlights.map(h => `<li>✦ ${h}</li>`).join('')}
        </ul>
      </div>
    </div>
  `).join("");

  const filteredPosts = INSTAGRAM_POSTS.filter(p => {
    if (AppState.instagramFilter === "TRAVEL") return p.channelType === "TRAVEL";
    if (AppState.instagramFilter === "FOOD") return p.channelType === "FOOD";
    return true;
  });

  const postsHtml = filteredPosts.map(post => `
    <div class="glass-card" style="overflow: hidden; cursor: pointer;" onclick="openInstagram('${post.handle}')">
      <div style="height: 220px; overflow: hidden; position: relative;">
        <img src="${post.imageUrl}" alt="Instagram Post" style="width: 100%; height: 100%; object-fit: cover;" loading="lazy" />
        <div style="position: absolute; top: 10px; left: 10px; background: rgba(0,0,0,0.7); padding: 4px 10px; border-radius: 9999px; font-size: 0.75rem; color: var(--gold-primary); font-weight: 700;">
          ${post.handle}
        </div>
      </div>
      <div style="padding: 16px;">
        <div style="font-size: 0.75rem; color: var(--text-tertiary); margin-bottom: 4px;">📍 ${post.location} · ❤️ ${post.likesCount}</div>
        <p style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.4;">${post.caption}</p>
      </div>
    </div>
  `).join("");

  return `
    <div style="margin-bottom: 32px;">
      <span class="pill-badge">Proof & Receipts</span>
      <h1 style="font-size: 2rem; margin-top: 6px;">800GB of 4K Footage Behind Every Route</h1>
      <p style="color: var(--text-secondary); font-size: 0.95rem;">We document every street, shack, and sunrise before recommending it.</p>
    </div>

    <!-- YouTube Creator Vlogs -->
    <div style="margin-bottom: 40px;">
      <div style="margin-bottom: 16px;">
        <h2 style="font-size: 1.4rem;">Creator YouTube Vlogs</h2>
      </div>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px;">
        ${videosHtml}
      </div>
    </div>

    <!-- Instagram Proof Feeds -->
    <div style="margin-bottom: 40px;">
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 20px;">
        <h2 style="font-size: 1.4rem;">Instagram Live Logs</h2>
        <div style="display: flex; gap: 8px;">
          <button class="btn-secondary ${AppState.instagramFilter === 'ALL' ? 'border-gold text-gold' : ''}" style="padding: 6px 14px; font-size: 0.8rem;" onclick="setInstaFilter('ALL')">All Feeds</button>
          <button class="btn-secondary ${AppState.instagramFilter === 'TRAVEL' ? 'border-gold text-gold' : ''}" style="padding: 6px 14px; font-size: 0.8rem;" onclick="setInstaFilter('TRAVEL')">📸 @cometriipwme</button>
          <button class="btn-secondary ${AppState.instagramFilter === 'FOOD' ? 'border-gold text-gold' : ''}" style="padding: 6px 14px; font-size: 0.8rem;" onclick="setInstaFilter('FOOD')">🍜 @beyondbengalurufoods</button>
        </div>
      </div>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px;">
        ${postsHtml}
      </div>
    </div>
  `;
}

function attachProofEvents() {}

function setInstaFilter(filter) {
  AppState.instagramFilter = filter;
  renderApp();
}

// ==========================================================================
// 4. CUSTOM PLANNER SCREEN
// ==========================================================================
function renderPlannerScreen() {
  const p = AppState.planner;
  const estStay = Math.round(p.budget * 0.40);
  const estFood = Math.round(p.budget * 0.30);
  const estTransport = Math.round(p.budget * 0.18);
  const estExperiences = Math.round(p.budget * 0.12);

  const destinations = ["Goa", "Thailand", "Himachal", "Pondicherry", "Krabi", "Malaysia", "Gokarna", "Coorg", "Hampi", "Bengaluru"];
  const vibes = Object.keys(TRIP_VIBES);
  const durations = [3, 4, 5, 7, 10];
  const squads = ["Solo 🙋", "2 of us 👫", "Small squad (3-5) 🫂", "Big group (6+) 🎉"];

  return `
    <div style="margin-bottom: 28px;">
      <span class="pill-badge">Tailored Routes</span>
      <h1 style="font-size: 2rem; margin-top: 6px;">Custom Trip Builder</h1>
      <p style="color: var(--text-secondary); font-size: 0.95rem;">Build your custom route. We calculate realistic budget allocations with verified creator spots.</p>
    </div>

    <!-- Step 1: Destination -->
    <div class="glass-card" style="padding: 24px; margin-bottom: 20px;">
      <div style="font-size: 0.75rem; font-weight: 700; color: var(--gold-primary); text-transform: uppercase; margin-bottom: 12px; letter-spacing: 0.05em;">1. Choose Destination</div>
      <div style="display: flex; gap: 8px; flex-wrap: wrap;">
        ${destinations.map(d => `
          <button class="btn-secondary ${p.destination === d ? 'border-gold text-gold' : ''}" style="padding: 8px 16px; font-size: 0.85rem;" onclick="setPlannerProp('destination', '${d}')">
            ${d}
          </button>
        `).join('')}
      </div>
    </div>

    <!-- Step 2: Vibe -->
    <div class="glass-card" style="padding: 24px; margin-bottom: 20px;">
      <div style="font-size: 0.75rem; font-weight: 700; color: var(--gold-primary); text-transform: uppercase; margin-bottom: 12px; letter-spacing: 0.05em;">2. Select Trip Vibe</div>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px;">
        ${vibes.map(vKey => {
          const v = TRIP_VIBES[vKey];
          const isSelected = p.vibe === vKey;
          return `
            <div class="glass-surface" style="padding: 12px; border-radius: 12px; text-align: center; cursor: pointer; border: 1px solid ${isSelected ? v.color : 'var(--glass-border)'}; background: ${isSelected ? v.color + '22' : 'var(--glass-surface)'};" onclick="setPlannerProp('vibe', '${vKey}')">
              <div style="font-size: 1.4rem;">${v.emoji}</div>
              <div style="font-size: 0.8rem; font-weight: 700; color: ${isSelected ? v.color : 'var(--text-primary)'}; margin-top: 4px;">${v.label}</div>
            </div>
          `;
        }).join('')}
      </div>
    </div>

    <!-- Step 3: Duration & Squad -->
    <div class="glass-card" style="padding: 24px; margin-bottom: 20px;">
      <div style="margin-bottom: 18px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
          <span style="font-size: 0.75rem; font-weight: 700; color: var(--gold-primary); text-transform: uppercase;">3. Duration</span>
          <span style="font-size: 0.85rem; font-weight: 700; color: var(--gold-secondary);">${p.duration} Days / ${p.duration - 1} Nights</span>
        </div>
        <div style="display: flex; gap: 8px;">
          ${durations.map(d => `
            <button class="btn-secondary ${p.duration === d ? 'border-gold text-gold' : ''}" style="flex: 1; padding: 8px 0; font-size: 0.85rem;" onclick="setPlannerProp('duration', ${d})">
              ${d}D
            </button>
          `).join('')}
        </div>
      </div>

      <div>
        <div style="font-size: 0.75rem; font-weight: 700; color: var(--gold-primary); text-transform: uppercase; margin-bottom: 10px;">4. Travelers / Squad</div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 8px;">
          ${squads.map(sq => `
            <button class="btn-secondary ${p.squad === sq ? 'border-gold text-gold' : ''}" style="padding: 8px 10px; font-size: 0.8rem;" onclick="setPlannerProp('squad', '${sq}')">
              ${sq}
            </button>
          `).join('')}
        </div>
      </div>
    </div>

    <!-- Step 5: Budget Allocation -->
    <div class="glass-card-gold" style="padding: 24px; margin-bottom: 24px;">
      <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 8px;">
        <span style="font-size: 0.75rem; font-weight: 700; color: var(--gold-primary); text-transform: uppercase;">5. Target Budget (₹/person)</span>
        <span style="font-size: 1.6rem; font-weight: 800; color: var(--gold-primary);">₹${p.budget.toLocaleString('en-IN')}</span>
      </div>

      <input type="range" class="budget-slider" min="4000" max="60000" step="1000" value="${p.budget}" oninput="updatePlannerBudget(this.value)" />

      <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 14px;">
        <div style="font-size: 0.75rem; color: var(--text-tertiary); text-transform: uppercase; font-weight: 700;">Estimated Allocation Breakdown</div>
        <div style="display: flex; justify-content: space-between; padding: 8px 12px; background: rgba(0,0,0,0.3); border-radius: 8px; font-size: 0.85rem;">
          <span>🏨 Verified Stays / Huts</span>
          <strong style="color: var(--gold-primary);">₹${estStay.toLocaleString('en-IN')} (40%)</strong>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 8px 12px; background: rgba(0,0,0,0.3); border-radius: 8px; font-size: 0.85rem;">
          <span>🍜 Food & Cafés (@beyondbengalurufoods)</span>
          <strong style="color: var(--gold-primary);">₹${estFood.toLocaleString('en-IN')} (30%)</strong>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 8px 12px; background: rgba(0,0,0,0.3); border-radius: 8px; font-size: 0.85rem;">
          <span>🛵 Scooty / Ferries / Transport</span>
          <strong style="color: var(--gold-primary);">₹${estTransport.toLocaleString('en-IN')} (18%)</strong>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 8px 12px; background: rgba(0,0,0,0.3); border-radius: 8px; font-size: 0.85rem;">
          <span>🎟️ Kayaking, Guide & Experiences</span>
          <strong style="color: var(--gold-primary);">₹${estExperiences.toLocaleString('en-IN')} (12%)</strong>
        </div>
      </div>
    </div>

    <!-- WhatsApp Inquiry Export -->
    <div class="glass-card-gold" style="padding: 28px; margin-bottom: 40px; text-align: center;">
      <h3 style="font-size: 1.4rem; margin-bottom: 8px;">Ready To Sort Your Custom Plan?</h3>
      <p style="color: var(--text-secondary); font-size: 0.9rem; max-width: 500px; margin: 0 auto 20px;">
        We review your preferences and message your complete Day-by-Day itinerary on WhatsApp within hours.
      </p>
      <button class="btn-gold" style="width: 100%; max-width: 400px; margin: 0 auto 12px;" onclick="sendCustomPlanWhatsApp()">
        Send Request On WhatsApp 💬
      </button>
      <div style="display: flex; justify-content: center; gap: 12px;">
        <button class="btn-secondary" onclick="openPhone()">📞 Call 9742311023</button>
        <button class="btn-secondary" onclick="sendCustomPlanEmail()">✉️ Email Plan</button>
      </div>
    </div>
  `;
}

function attachPlannerEvents() {}

function setPlannerProp(key, value) {
  AppState.planner[key] = value;
  renderApp();
}

function updatePlannerBudget(val) {
  AppState.planner.budget = parseInt(val);
  renderApp();
}

function sendCustomPlanWhatsApp() {
  const p = AppState.planner;
  const vibeLabel = TRIP_VIBES[p.vibe]?.label || p.vibe;
  const msg = `Hey ComeTripWithMe! Please sort a custom trip for me:
📍 Destination: ${p.destination}
✨ Vibe: ${vibeLabel}
📅 Duration: ${p.duration} Days
🫂 Travelers: ${p.squad}
💰 Target Budget: ₹${p.budget.toLocaleString('en-IN')}/person`;
  openWhatsApp(msg);
}

function sendCustomPlanEmail() {
  const p = AppState.planner;
  const vibeLabel = TRIP_VIBES[p.vibe]?.label || p.vibe;
  const body = `Custom Trip Request Details:

Destination: ${p.destination}
Vibe: ${vibeLabel}
Duration: ${p.duration} Days
Travelers: ${p.squad}
Budget: ₹${p.budget.toLocaleString('en-IN')}/person`;
  openEmail(`Custom Trip Request - ${p.destination}`, body);
}

// ==========================================================================
// 5. SAVED TRIPS SCREEN
// ==========================================================================
function renderSavedScreen() {
  const savedTrips = CURATED_TRIPS.filter(t => AppState.wishlist.includes(t.id));

  const savedHtml = savedTrips.length > 0 ? savedTrips.map(trip => `
    <div class="glass-card" style="padding: 20px; margin-bottom: 16px; display: flex; gap: 16px; align-items: center; justify-content: space-between; flex-wrap: wrap;">
      <div style="display: flex; gap: 16px; align-items: center;">
        <img src="${trip.imageUrl}" alt="${trip.name}" style="width: 80px; height: 80px; border-radius: 12px; object-fit: cover;" loading="lazy" />
        <div>
          <h3 style="font-size: 1.2rem;">${trip.name}</h3>
          <div style="font-size: 0.85rem; color: var(--gold-secondary);">${trip.duration} · ${trip.price}</div>
          <p style="font-size: 0.8rem; color: var(--text-tertiary); margin-top: 2px;">${trip.heroTags.slice(0, 2).join(" · ")}</p>
        </div>
      </div>
      <div style="display: flex; gap: 10px;">
        <button class="btn-gold" style="padding: 8px 16px; font-size: 0.85rem;" onclick="startGuide('${trip.id}')">
          Launch Guide ✦
        </button>
        <button class="wishlist-btn active" onclick="toggleWishlist('${trip.id}')" title="Remove">
          <i data-lucide="trash-2"></i>
        </button>
      </div>
    </div>
  `).join("") : `
    <div class="glass-card" style="padding: 48px 24px; text-align: center;">
      <div style="font-size: 2.5rem; margin-bottom: 12px;">🏖️</div>
      <h3 style="font-size: 1.3rem; margin-bottom: 6px;">No Saved Trips Yet</h3>
      <p style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 20px;">Browse our curated routes and tap the heart icon to save itineraries for your next getaway.</p>
      <button class="btn-gold" onclick="setTab('explore')">Explore Trips ✦</button>
    </div>
  `;

  return `
    <div style="margin-bottom: 28px;">
      <span class="pill-badge">Wishlist</span>
      <h1 style="font-size: 2rem; margin-top: 6px;">Your Saved Itineraries</h1>
      <p style="color: var(--text-secondary); font-size: 0.95rem;">Quick access to your dream routes and offline guides.</p>
    </div>

    <div>
      ${savedHtml}
    </div>
  `;
}

function attachSavedEvents() {}

// ==========================================================================
// MODAL DIALOG CONTROLLERS
// ==========================================================================
function openTripDetail(tripId) {
  const trip = CURATED_TRIPS.find(t => t.id === tripId);
  if (!trip) return;

  const modalOverlay = document.getElementById("trip-modal");
  const modalBody = document.getElementById("trip-modal-body");

  if (!modalOverlay || !modalBody) return;

  const vibe = TRIP_VIBES[trip.vibe] || TRIP_VIBES.CHILL;

  const daysHtml = trip.days.map(d => `
    <div style="margin-bottom: 24px; background: var(--bg-dark-elevated); padding: 18px; border-radius: 16px; border: 1px solid var(--glass-border);">
      <div style="font-size: 0.8rem; font-weight: 700; color: var(--gold-primary); text-transform: uppercase;">Day ${d.dayNumber}: ${d.title}</div>
      <p style="font-size: 0.9rem; color: var(--text-secondary); margin: 6px 0 14px;">${d.summary}</p>

      <div style="display: flex; flex-direction: column; gap: 10px;">
        ${d.stops.map((s, idx) => `
          <div style="background: rgba(0,0,0,0.3); padding: 12px; border-radius: 10px; display: flex; gap: 12px; align-items: center;">
            <span style="width: 24px; height: 24px; border-radius: 50%; background: var(--gold-container); color: var(--gold-primary); font-size: 0.75rem; font-weight: 700; display: flex; align-items: center; justify-content: center;">${idx + 1}</span>
            <div style="flex: 1;">
              <div style="font-weight: 700; font-size: 0.9rem;">${s.name}</div>
              <div style="font-size: 0.75rem; color: var(--text-tertiary);">${s.timing} · ${s.category}</div>
            </div>
            ${s.insiderTip ? `<span style="font-size: 0.75rem; color: var(--gold-secondary);" title="${s.insiderTip}">⚡ Tip</span>` : ''}
          </div>
        `).join('')}
      </div>
    </div>
  `).join("");

  modalBody.innerHTML = `
    <div style="position: relative; height: 260px;">
      <img src="${trip.imageUrl}" alt="${trip.name}" style="width: 100%; height: 100%; object-fit: cover;" />
      <div style="position: absolute; inset: 0; background: linear-gradient(180deg, transparent 30%, var(--bg-dark-card) 100%);"></div>
      <div style="position: absolute; bottom: 18px; left: 24px; right: 24px;">
        <span class="pill-badge" style="background: ${vibe.color}33; border-color: ${vibe.color}; color: ${vibe.color};">${vibe.emoji} ${vibe.label}</span>
        <h2 style="font-size: 2rem; margin-top: 4px;">${trip.name}</h2>
        <div style="font-size: 0.9rem; color: var(--gold-secondary); font-weight: 700;">${trip.duration} · ${trip.price} / person</div>
      </div>
    </div>

    <div style="padding: 24px;">
      <p style="font-size: 1rem; color: var(--text-secondary); line-height: 1.6; margin-bottom: 20px;">${trip.description}</p>
      
      <div style="background: rgba(232, 201, 122, 0.1); border: 1px solid var(--glass-border-gold); padding: 14px; border-radius: 12px; margin-bottom: 24px; font-size: 0.9rem; color: var(--gold-primary);">
        "${trip.creatorNote}"
      </div>

      <h3 style="font-size: 1.3rem; margin-bottom: 16px;">Day-by-Day Route</h3>
      ${daysHtml}

      <div style="display: flex; gap: 12px; flex-wrap: wrap; margin-top: 24px;">
        <button class="btn-gold" style="flex: 1;" onclick="startGuide('${trip.id}'); closeTripModal();">
          Start Pocket Guide ✦
        </button>
        <button class="btn-secondary" onclick="openWhatsApp('Hey! I want to book the ${trip.name} curated trip.')">
          Inquire On WhatsApp 💬
        </button>
      </div>
    </div>
  `;

  modalOverlay.classList.add("open");
  if (window.lucide) lucide.createIcons();
}

function closeTripModal() {
  const modalOverlay = document.getElementById("trip-modal");
  if (modalOverlay) modalOverlay.classList.remove("open");
}

function openTripSelectorModal() {
  openTripDetail(AppState.activeGuideTripId);
}

function openSpotlight(spotId) {
  const spot = (typeof SPOTLIGHTS !== "undefined") ? SPOTLIGHTS.find(s => s.id === spotId) : null;
  if (!spot) {
    const matchingTrip = CURATED_TRIPS.find(t => t.id.includes(spotId) || spotId.includes(t.id));
    if (matchingTrip) openTripDetail(matchingTrip.id);
    return;
  }

  const modalOverlay = document.getElementById("trip-modal");
  const modalBody = document.getElementById("trip-modal-body");
  if (!modalOverlay || !modalBody) return;

  const matchingTrip = CURATED_TRIPS.find(t => t.id === spot.id || spot.id.includes(t.id) || t.id.includes(spot.id));
  const cleanDestName = spot.title.split("&")[0].trim();

  const spotsListHtml = spot.documentedSpots ? spot.documentedSpots.map((s, idx) => `
    <div style="background: var(--bg-dark-elevated); padding: 14px; border-radius: 12px; border: 1px solid var(--glass-border); margin-bottom: 10px;">
      <div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 8px;">
        <div style="display: flex; align-items: center; gap: 10px;">
          <span style="width: 26px; height: 26px; border-radius: 50%; background: var(--gold-container); color: var(--gold-primary); font-size: 0.75rem; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">${idx + 1}</span>
          <div style="font-weight: 700; font-size: 0.95rem; color: var(--text-primary);">${s.name}</div>
        </div>
        <span style="font-size: 0.7rem; padding: 2px 8px; border-radius: 6px; background: rgba(232, 201, 122, 0.1); color: var(--gold-primary); font-weight: 600; white-space: nowrap;">${s.category}</span>
      </div>
      ${s.tip ? `
        <div style="margin-top: 8px; padding-left: 36px; font-size: 0.85rem; color: var(--text-secondary); line-height: 1.4;">
          ⚡ <strong style="color: var(--gold-secondary);">Insider Tip:</strong> ${s.tip}
        </div>
      ` : ''}
    </div>
  `).join("") : "";

  const foodPillsHtml = spot.foodHighlights ? spot.foodHighlights.map(f => `
    <span style="font-size: 0.75rem; background: rgba(255,255,255,0.06); border: 1px solid var(--glass-border); padding: 4px 10px; border-radius: 6px; color: var(--text-primary);">🍜 ${f}</span>
  `).join("") : "";

  modalBody.innerHTML = `
    <div style="position: relative; height: 260px;">
      <img src="${spot.imageUrl}" alt="${spot.title}" style="width: 100%; height: 100%; object-fit: cover;" />
      <div style="position: absolute; inset: 0; background: linear-gradient(180deg, transparent 20%, var(--bg-dark-card) 100%);"></div>
      <div style="position: absolute; bottom: 18px; left: 24px; right: 24px;">
        <span class="pill-badge" style="background: rgba(232, 201, 122, 0.2); border-color: var(--gold-primary); color: var(--gold-primary); margin-bottom: 6px;">✦ Regional Deep Dive</span>
        <h2 style="font-size: 1.9rem; margin-top: 4px;">${spot.title}</h2>
        <div style="font-size: 0.85rem; color: var(--gold-secondary); font-weight: 600;">${spot.region} · ${spot.documentedSpotsCount}</div>
      </div>
    </div>

    <div style="padding: 24px;">
      <p style="font-size: 1rem; color: var(--text-secondary); line-height: 1.6; margin-bottom: 20px;">${spot.overview || spot.subtitle}</p>

      <!-- Quick Intel Bar -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-bottom: 24px;">
        ${spot.bestSeason ? `
          <div style="background: rgba(0,0,0,0.3); padding: 12px 16px; border-radius: 12px; border: 1px solid var(--glass-border);">
            <div style="font-size: 0.7rem; color: var(--text-tertiary); text-transform: uppercase; font-weight: 700;">Best Time To Visit</div>
            <div style="font-size: 0.85rem; font-weight: 600; color: var(--gold-primary); margin-top: 2px;">${spot.bestSeason}</div>
          </div>
        ` : ''}
        ${spot.durationRec ? `
          <div style="background: rgba(0,0,0,0.3); padding: 12px 16px; border-radius: 12px; border: 1px solid var(--glass-border);">
            <div style="font-size: 0.7rem; color: var(--text-tertiary); text-transform: uppercase; font-weight: 700;">Recommended Duration</div>
            <div style="font-size: 0.85rem; font-weight: 600; color: var(--gold-primary); margin-top: 2px;">${spot.durationRec}</div>
          </div>
        ` : ''}
      </div>

      <!-- Creator Advice -->
      ${spot.creatorAdvice ? `
        <div style="background: rgba(232, 201, 122, 0.1); border-left: 4px solid var(--gold-primary); padding: 14px 16px; border-radius: 0 12px 12px 0; margin-bottom: 24px; font-size: 0.9rem; color: var(--gold-primary); line-height: 1.5;">
          <strong>⚡ Creator Field Note:</strong> "${spot.creatorAdvice}"
        </div>
      ` : ''}

      <!-- Documented Spots -->
      ${spotsListHtml ? `
        <h3 style="font-size: 1.25rem; margin-bottom: 14px; display: flex; align-items: center; gap: 8px;">
          <span>📍 Documented Trails & Secret Spots</span>
        </h3>
        <div style="margin-bottom: 24px;">
          ${spotsListHtml}
        </div>
      ` : ''}

      <!-- Food Highlights -->
      ${foodPillsHtml ? `
        <div style="margin-bottom: 28px;">
          <h4 style="font-size: 0.85rem; font-weight: 700; color: var(--gold-primary); text-transform: uppercase; margin-bottom: 10px; letter-spacing: 0.05em;">Curated Local Food & Specialties</h4>
          <div style="display: flex; flex-wrap: wrap; gap: 8px;">
            ${foodPillsHtml}
          </div>
        </div>
      ` : ''}

      <!-- Action Buttons -->
      <div style="display: flex; gap: 12px; flex-wrap: wrap; margin-top: 24px;">
        <button class="btn-gold" style="flex: 1;" onclick="planForRegion('${cleanDestName}')">
          Plan Custom Trip For ${cleanDestName} ✦
        </button>
        ${matchingTrip ? `
          <button class="btn-secondary" onclick="openTripDetail('${matchingTrip.id}')">
            View Full Circuit ↗
          </button>
        ` : ''}
        <button class="btn-secondary" onclick="openWhatsApp('Hey ComeTripWithMe! I want intel and a route for ${spot.title}.')">
          Inquire On WhatsApp 💬
        </button>
      </div>
    </div>
  `;

  modalOverlay.classList.add("open");
  if (window.lucide) lucide.createIcons();
}

function planForRegion(regionName) {
  closeTripModal();
  AppState.planner.destination = regionName;
  setTab("planner");
  showToast(`Custom Planner ready for ${regionName} ✦`);
}

// ==========================================================================
// WISHLIST & PACKING STORAGE
// ==========================================================================
function toggleWishlist(tripId) {
  const idx = AppState.wishlist.indexOf(tripId);
  if (idx > -1) {
    AppState.wishlist.splice(idx, 1);
    showToast("Removed from wishlist");
  } else {
    AppState.wishlist.push(tripId);
    showToast("Added to wishlist ♡");
  }
  safeSetStorage("ctwm_wishlist", AppState.wishlist);
  renderApp();
}

function togglePacking(itemId) {
  const item = AppState.packingList.find(p => p.id === itemId);
  if (item) {
    item.checked = !item.checked;
    safeSetStorage("ctwm_packing", AppState.packingList);
    renderApp();
  }
}

function addPackingPrompt() {
  const title = prompt("Enter packing item title:");
  if (title && title.trim()) {
    AppState.packingList.push({
      id: "p_" + Date.now(),
      title: title.trim(),
      category: "Personal",
      checked: false
    });
    safeSetStorage("ctwm_packing", AppState.packingList);
    renderApp();
  }
}

function surpriseMe() {
  const randomTrip = CURATED_TRIPS[Math.floor(Math.random() * CURATED_TRIPS.length)];
  openTripDetail(randomTrip.id);
  showToast(`🎲 How about ${randomTrip.name}?`);
}

// ==========================================================================
// EXTERNAL ACTIONS & TOAST
// ==========================================================================
function openWhatsApp(message = "Hey ComeTripWithMe! I want to plan a trip.") {
  const encoded = encodeURIComponent(message);
  window.open(`https://wa.me/919742311023?text=${encoded}`, "_blank");
}

function openInstagram(handle = "cometriipwme") {
  const clean = handle.replace("@", "");
  window.open(`https://instagram.com/${clean}`, "_blank");
}

function openInstagramReel(url) {
  window.open(url || "https://instagram.com/beyondbengalurufoods", "_blank");
}

function openYouTube(url) {
  window.open(url || "https://youtube.com/@Cometripwithme", "_blank");
}

function openPhone() {
  window.open("tel:+919742311023", "_self");
}

function openEmail(subject = "Trip Inquiry - ComeTripWithMe", body = "") {
  const encSub = encodeURIComponent(subject);
  const encBody = encodeURIComponent(body);
  window.open(`mailto:bengalurufoodss@gmail.com?subject=${encSub}&body=${encBody}`, "_self");
}

function openGoogleMaps(query) {
  window.open(`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(query)}`, "_blank");
}

function showToast(msg) {
  const container = document.getElementById("toast-container");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = "toast";
  toast.innerText = msg;
  container.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 3200);
}
