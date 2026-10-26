<div align="center">
  <h1>✨ ComeTripWithMe</h1>
  <p><strong>India's 1st Creator Tour Operator Platform</strong></p>
  <p>Curated 3-Tier Itineraries (Luxury · Mid-Tier · Budget) · Interactive Live Audio Guide · Route Map Visualizer · AI Travel Copilot</p>
</div>

---

## 📖 Overview

**ComeTripWithMe** is a dual-platform travel companion providing curated itineraries created by top travel creators across India. It supports both a full-featured, zero-dependency **Web Application (PWA)** and a native **Android Application** (Jetpack Compose + Google Gemini AI SDK).

### Core Highlights
- 🌟 **3-Tier Trip Engine**: Seamlessly switch between **Luxury** (5-star heritage resorts, private charters), **Mid-Tier** (boutique stays, cab transfers), and **Budget** (social hostels, Volvo sleepers & trains).
- 🎧 **Interactive Live Audio Guide**: Creator voice narrations, secret viewpoints, cultural anecdotes, and real-time audio playback controls.
- 🗺️ **Canvas Route Map Visualizer**: Interactive route waypoints, day-by-day stops, and coordinate tracking.
- 🤖 **Gemini AI Travel Copilot**: On-demand itinerary generation tailored to destination, group type, budget, and travel vibe.
- 🎟️ **Instant Booking & Travel Passes**: Digital passes, breakdown calculations, and offline storage.

---

## 📂 Project Structure & File Guide

```
cometripwithme/
├── 🌐 Web & Server Layer
│   ├── index.html                   # Master single-page app (4,700+ lines, full client UI)
│   ├── server.py                    # Zero-dependency Python 3 HTTP server (port auto-fallback)
│   ├── server.js                    # Node.js HTTP static & SPA server
│   ├── package.json                 # NPM scripts (start, dev, serve)
│   └── metadata.json                # Google AI Studio manifest
│
├── ⚙️ Build & Generation Scripts
│   ├── generate_tiered_index.py     # Master 3-Tier Luxury/Mid/Budget generator
│   ├── build_airport_app.py         # Multi-city airport transit & hub generator
│   ├── generate_enhanced_index.py   # Enhanced UI and audio routines generator
│   ├── generate_index.py            # Baseline Python generator
│   └── generate_index.js            # Node.js generator script
│
├── 📱 Native Android App (/app)
│   ├── src/main/java/com/example/
│   │   ├── MainActivity.kt          # Compose root activity & bottom navigation
│   │   ├── ui/viewmodel/            # MainViewModel (Room flows, cart, state)
│   │   ├── ui/screens/              # Explore, Planner, Guide, Booking, Saved, AI Copilot
│   │   ├── ui/components/           # AudioGuidePlayer, RouteMapVisualizer, CommonComponents
│   │   ├── ui/theme/                # Dark theme, Obsidian/Gold color palette, Typography
│   │   ├── data/service/            # GeminiAiService (Gemini 3.5 Flash + fallback)
│   │   ├── data/repository/         # TripRepository (2,200+ lines of curated trips)
│   │   ├── data/local/              # Room DB, DAOs, Entities
│   │   └── data/model/              # Trip, Pricing, Booking, Chat domain models
│   ├── src/main/AndroidManifest.xml # Android app manifest
│   └── build.gradle.kts             # App Gradle config (SDK 36, Compose, Room, KSP)
│
└── 🛠️ Gradle Toolchain
    ├── build.gradle.kts             # Root Gradle build script
    ├── settings.gradle.kts          # Plugin management & repositories
    ├── gradle.properties            # JVM & memory configuration
    └── gradle/libs.versions.toml    # Dependency version catalog
```

---

## 🚀 Running the Project

### 1. Web Application (Recommended / Quickest)

The web application runs with either **Python 3** (built into macOS) or **Node.js**:

#### Using Python 3:
```bash
python3 server.py
```
> The server automatically starts on **`http://localhost:3000`** (or `3001` if port 3000 is occupied).

#### Using Node.js:
```bash
npm start
# or
node server.js
```

---

### 2. Native Android Application

**Prerequisites:** [Android Studio](https://developer.android.com/studio) (Koala / Ladybug or newer recommended, JDK 17+).

1. Open **Android Studio**.
2. Select **Open** and choose this project root directory (`cometripwithme`).
3. Allow Gradle to sync and download required dependencies.
4. *(Optional)* Create a `.env` file in the root directory to set your Gemini API key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   *(If not provided, the app uses its built-in offline smart heuristic engine automatically).*
5. Select a device or emulator running **Android 7.0+ (API 24+)** and click **Run**.

---

## 🌐 Deploying & Hosting the Web App

The web client (`index.html`) is completely self-contained with no server-side build step required. You can host it for free in seconds:

### Option A: Netlify Drop / CLI
```bash
npx netlify-cli deploy --prod --dir=.
```

### Option B: Vercel
```bash
npx vercel --prod
```

### Option C: GitHub Pages
1. Push this repository to GitHub.
2. Go to **Settings > Pages**.
3. Under **Build and deployment**, select **Deploy from a branch** and choose `main` / `root`.

---

## ⚡ FastAPI Backend & Payment Gateway

The project includes a production-ready **Python FastAPI** backend located in [`backend/`](file:///Users/karthikdalabanjan/Downloads/cometripwithme%20%281%29/backend) for data storage, Razorpay payments, and beta testing telemetry:

### 1. Launching the Backend API
```bash
python3 run_backend.py
```
- **API Base**: `http://localhost:8000`
- **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Tester Command Center Dashboard**: [http://localhost:8000/dashboard](http://localhost:8000/dashboard)

### 2. Features & Testing Endpoints
- **Data Persistence**: SQLite (`cometripwithme.db`) by default; switch to PostgreSQL / Supabase via `DATABASE_URL`.
- **Razorpay Payment Gateway**: Supports **Smart Sandbox Mock Mode** out of the box (or real test keys via `RAZORPAY_KEY_ID` & `RAZORPAY_KEY_SECRET`).
- **Beta Testing Criteria Telemetry**: Evaluates and benchmarks:
  - `CRIT-01`: Pricing & Tier Calculation Clarity
  - `CRIT-02`: Audio Guide Experience & Latency
  - `CRIT-03`: Route Map Waypoint Rendering
  - `CRIT-04`: Payment Sandbox End-to-End Flow
  - `CRIT-05`: Mobile UX & Viewport Responsiveness
  - `CRIT-06`: Offline State Recovery
- **Aggregated Analytics**: Live scores visible at `/api/v1/testing/metrics` and on the HTML `/dashboard`.

---

## 📄 Documentation

For deep-dive architectural specifications, refer to:
- [Backend Architecture & Testing Plan](file:///Users/karthikdalabanjan/.gemini/antigravity-ide/brain/84a75eba-1578-407d-a234-f80f44f581d5/backend_plan.md)
- [Complete File-by-File Documentation](file:///Users/karthikdalabanjan/.gemini/antigravity-ide/brain/84a75eba-1578-407d-a234-f80f44f581d5/file_documentation.md)
