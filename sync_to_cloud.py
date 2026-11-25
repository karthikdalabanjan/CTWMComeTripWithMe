#!/usr/bin/env python3
"""
ComeTripWithMe · Cloud Database Synchronizer
Migrates all tables and records from local SQLite (cometripwithme.db) to Supabase / PostgreSQL.
Usage: python3 sync_to_cloud.py [POSTGRES_URL]
"""
import os
import sys
import json
import sqlite3
from sqlalchemy import create_engine, inspect, text
from backend.database import Base
from backend.models import User, Booking, TripLeg, DriverMessage, Payment, CustomItinerary, TestFeedback, TelemetryEvent, WishlistItem, Stakeholder

SQLITE_PATH = "cometripwithme.db"

def sync_to_cloud(cloud_db_url: str):
    print("======================================================")
    print("🚀 ComeTripWithMe · Local SQLite ➔ Cloud PostgreSQL Sync")
    print("======================================================")
    print(f"📁 Local Source: {SQLITE_PATH}")
    print(f"☁️ Cloud Target: {cloud_db_url.split('@')[-1] if '@' in cloud_db_url else cloud_db_url}\n")

    if not os.path.exists(SQLITE_PATH):
        print(f"❌ Error: Local database '{SQLITE_PATH}' not found.")
        sys.exit(1)

    # 1. Connect to cloud database
    try:
        if cloud_db_url.startswith("postgres://"):
            cloud_db_url = cloud_db_url.replace("postgres://", "postgresql://", 1)

        cloud_engine = create_engine(cloud_db_url, pool_pre_ping=True)
        with cloud_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✓ Connected to Cloud PostgreSQL successfully!")
    except Exception as e:
        print(f"❌ Failed to connect to cloud database: {e}")
        sys.exit(1)

    # 2. Initialize Cloud Database Schema
    print("⚙️ Initializing cloud tables & relations...")
    Base.metadata.create_all(bind=cloud_engine)
    print("✓ Cloud schema synchronized!")

    # 3. Read Local SQLite records
    sqlite_conn = sqlite3.connect(SQLITE_PATH)
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cur = sqlite_conn.cursor()

    tables = [
        "users", "custom_itineraries", "bookings", "trip_legs",
        "driver_messages", "payments", "test_feedback", "telemetry_events", "wishlist_items", "stakeholders"
    ]

    total_migrated = 0

    with cloud_engine.begin() as cloud_conn:
        for t in tables:
            try:
                sqlite_cur.execute(f"SELECT * FROM {t}")
                rows = sqlite_cur.fetchall()
                if not rows:
                    print(f"• Table '{t}': 0 rows (Skipped)")
                    continue

                col_names = [col[0] for col in sqlite_cur.description]
                placeholders = ", ".join([f":{c}" for c in col_names])
                cols_str = ", ".join(col_names)

                insert_sql = text(f"INSERT INTO {t} ({cols_str}) VALUES ({placeholders}) ON CONFLICT DO NOTHING")

                count = 0
                for r in rows:
                    row_dict = dict(r)
                    # Convert integer boolean for Postgres
                    for k, v in row_dict.items():
                        if k in ("is_beta_tester", "is_sandbox") and isinstance(v, int):
                            row_dict[k] = bool(v)
                    cloud_conn.execute(insert_sql, row_dict)
                    count += 1

                print(f"✓ Table '{t}': Migrated {count} records successfully.")
                total_migrated += count
            except Exception as e:
                print(f"⚠️ Notice on table '{t}': {e}")

    sqlite_conn.close()

    print("\n======================================================")
    print(f"🎉 Cloud Synchronization Complete! Total {total_migrated} records transferred.")
    print("Your app is now running with cloud PostgreSQL backing!")
    print("======================================================\n")

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else os.getenv("DATABASE_URL")
    if not url or "sqlite" in url:
        print("💡 Usage:")
        print("   python3 sync_to_cloud.py postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres")
        print("Or set DATABASE_URL in your .env file.")
        sys.exit(1)
    sync_to_cloud(url)

