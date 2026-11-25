import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from backend.config import settings
from backend.database import engine, Base, ensure_db_schema
from backend.routers import auth, trips, bookings, payments, testing, agents, hr, support

# Initialize database schema automatically
Base.metadata.create_all(bind=engine)
ensure_db_schema()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend API for ComeTripWithMe: Data Persistence, Razorpay Payment Gateway, and Beta Testing Telemetry."
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(trips.router, prefix=settings.API_V1_STR)
app.include_router(bookings.router, prefix=settings.API_V1_STR)
app.include_router(payments.router, prefix=settings.API_V1_STR)
app.include_router(testing.router, prefix=settings.API_V1_STR)
app.include_router(agents.router, prefix=settings.API_V1_STR)
app.include_router(hr.router, prefix=settings.API_V1_STR)
app.include_router(support.router, prefix=settings.API_V1_STR)

@app.get("/", response_class=HTMLResponse, tags=["Consumer Traveler App"])
def root():
    """Serves the primary ComeTripWithMe Consumer Traveler Web Application."""
    return web_app()

@app.get("/status", tags=["Health & Service Info"])
@app.get("/api", tags=["Health & Service Info"])
def api_status():
    """Returns the backend API system status and microservice routing map."""
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "traveler_app": "/",
        "cloud_platform": "/platform",
        "docs_url": "/docs",
        "testing_dashboard": "/dashboard",
        "autonomous_agents": f"{settings.API_V1_STR}/agents/status",
        "payment_gateway": {
            "provider": "Razorpay",
            "mode": "Sandbox Mock Mode" if not settings.RAZORPAY_KEY_ID else "Razorpay Test/Live Mode"
        }
    }

@app.get("/health", tags=["Health & Service Info"])
def health_check():
    return {"status": "healthy"}

@app.get("/platform", response_class=HTMLResponse, tags=["Operations Platform"])
def operations_platform():
    """Serves the Master Cloud Operations Platform & Autonomous Agents Hub."""
    plat_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "platform.html")
    if os.path.exists(plat_path):
        with open(plat_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>ComeTripWithMe Platform Loading...</h1>"

@app.get("/app", response_class=HTMLResponse, tags=["Web App"])
def web_app():
    """Serves the ComeTripWithMe Single Page Application."""
    app_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "index.html")
    if os.path.exists(app_path):
        with open(app_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>ComeTripWithMe App loading...</h1>"

@app.get("/dashboard", response_class=HTMLResponse, tags=["Testing Dashboard"])
def testing_dashboard():
    """
    Visual HTML Dashboard for monitoring beta testers and criteria scores in real time.
    """
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ComeTripWithMe · Beta Testing & Payment Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #07090E;
            --surface: #0F131C;
            --surface-elevated: #161C2A;
            --gold: #E8C97A;
            --text-primary: #F8FAFC;
            --text-muted: #94A3B8;
            --green: #3CA082;
            --red: #DC503C;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background: var(--bg);
            color: var(--text-primary);
            font-family: 'Plus Jakarta Sans', sans-serif;
            padding: 30px;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(232,201,122,0.2);
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        h1 { font-family: 'Outfit', sans-serif; font-size: 26px; color: var(--gold); }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: var(--surface);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px;
            padding: 20px;
        }
        .card-title { font-size: 13px; color: var(--text-muted); text-transform: uppercase; margin-bottom: 8px; }
        .card-value { font-family: 'Outfit', sans-serif; font-size: 28px; font-weight: 700; color: #FFF; }
        .criteria-box {
            background: var(--surface);
            border: 1px solid rgba(232,201,122,0.2);
            border-radius: 14px;
            padding: 24px;
            margin-bottom: 30px;
        }
        .criteria-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        .criteria-name { font-weight: 600; font-size: 14px; }
        .badge {
            background: rgba(232,201,122,0.15);
            color: var(--gold);
            padding: 4px 12px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 700;
        }
        .refresh-btn {
            background: var(--gold);
            color: #000;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            font-weight: 700;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>ComeTripWithMe · Tester Command Center</h1>
            <p style="color: var(--text-muted); font-size: 14px; margin-top: 4px;">Live criteria scores, payment funnel, and tester feedback.</p>
        </div>
        <button class="refresh-btn" onclick="fetchMetrics()">Refresh Data</button>
    </div>

    <div class="grid">
        <div class="card">
            <div class="card-title">Total Tester Submissions</div>
            <div class="card-value" id="totalFeedbacks">-</div>
        </div>
        <div class="card">
            <div class="card-title">Average Overall Rating</div>
            <div class="card-value" id="avgRating" style="color: var(--gold);">-</div>
        </div>
        <div class="card">
            <div class="card-title">Bookings Initiated</div>
            <div class="card-value" id="bookingsInitiated">-</div>
        </div>
        <div class="card">
            <div class="card-title">Payments Captured</div>
            <div class="card-value" id="paymentsCaptured" style="color: var(--green);">-</div>
        </div>
    </div>

    <div class="criteria-box">
        <h2 style="font-family: 'Outfit'; font-size: 20px; color: var(--gold); margin-bottom: 16px;">Tested Criteria Benchmarks (Target: 5.0)</h2>
        <div id="criteriaList">Loading criteria evaluations...</div>
    </div>

    <script>
        async function fetchMetrics() {
            try {
                const res = await fetch('/api/v1/testing/metrics');
                const data = await res.json();
                
                document.getElementById('totalFeedbacks').innerText = data.testing_program.total_feedback_submissions;
                document.getElementById('avgRating').innerText = data.testing_program.average_overall_rating + ' / 5.0';
                document.getElementById('bookingsInitiated').innerText = data.funnel_analytics.total_bookings_initiated;
                document.getElementById('paymentsCaptured').innerText = data.funnel_analytics.payments_captured;

                const cMap = data.testing_program.criteria_benchmarks;
                let html = '';
                for (const [k, v] of Object.entries(cMap)) {
                    const cleanName = k.replace(/_/g, ' ').toUpperCase();
                    html += `
                        <div class="criteria-row">
                            <span class="criteria-name">${cleanName}</span>
                            <span class="badge">${v} / 5.0</span>
                        </div>
                    `;
                }
                document.getElementById('criteriaList').innerHTML = html || '<p style="color:var(--text-muted);">No tester scores submitted yet. Invite testers to review!</p>';
            } catch(e) {
                console.error(e);
            }
        }
        fetchMetrics();
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)
