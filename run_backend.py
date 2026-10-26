#!/usr/bin/env python3
"""
ComeTripWithMe FastAPI Backend Launcher
Starts the API server with live Swagger Docs and Tester Dashboard.
"""
import os
import sys
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print("======================================================")
    print("🚀 ComeTripWithMe FastAPI Backend is Starting!")
    print(f"🔗 API Endpoint:     http://localhost:{port}")
    print(f"📚 Swagger UI Docs:  http://localhost:{port}/docs")
    print(f"📊 Tester Dashboard: http://localhost:{port}/dashboard")
    print("💳 Payment Gateway:  Razorpay Sandbox / Test Mode")
    print("💾 Database:         SQLite (local) / PostgreSQL (cloud ready)")
    print("======================================================")
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)
