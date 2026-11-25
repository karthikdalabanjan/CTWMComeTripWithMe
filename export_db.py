#!/usr/bin/env python3
"""
ComeTripWithMe Database Inspector & Exporter
Exports all data across all tables to structured JSON and CSV formats.
Usage: python3 export_db.py
"""
import os
import csv
import json
from datetime import datetime
from sqlalchemy import inspect, text
from backend.database import engine

EXPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime,)):
        return obj.isoformat()
    return str(obj)

def export_all():
    print("======================================================")
    print("📦 ComeTripWithMe Database Inspector & Exporter")
    print("======================================================")
    print(f"🔗 Database URL: {engine.url}")
    print(f"📁 Output Directory: {EXPORT_DIR}\n")

    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    
    full_database_dump = {}

    with engine.connect() as conn:
        for table in table_names:
            print(f"🔍 Reading table: '{table}'...")
            result = conn.execute(text(f"SELECT * FROM {table}"))
            columns = result.keys()
            rows = result.fetchall()

            table_data = []
            for row in rows:
                row_dict = {}
                for idx, col in enumerate(columns):
                    val = row[idx]
                    # Parse JSON string fields if applicable
                    if isinstance(val, str) and (col.endswith('_json') or col in ('day_plans_json', 'traveler_details_json', 'criteria_scores_json', 'device_info_json')):
                        try:
                            val = json.loads(val)
                        except:
                            pass
                    row_dict[col] = val
                table_data.append(row_dict)

            full_database_dump[table] = table_data
            print(f"   ✓ Extracted {len(table_data)} records.")

            # Export individual CSV
            csv_path = os.path.join(EXPORT_DIR, f"{table}.csv")
            if table_data:
                with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=columns)
                    writer.writeheader()
                    for r in table_data:
                        # flatten complex dict/list for CSV
                        csv_row = {}
                        for k, v in r.items():
                            if isinstance(v, (dict, list)):
                                csv_row[k] = json.dumps(v)
                            else:
                                csv_row[k] = v
                        writer.writerow(csv_row)
                print(f"   📄 CSV saved: exports/{table}.csv")

    # Export unified JSON dump
    json_path = os.path.join(EXPORT_DIR, "database_dump.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(full_database_dump, f, default=json_serial, indent=2)

    print("\n======================================================")
    print("🎉 Export Completed Successfully!")
    print(f"💾 Master JSON Dump: {json_path}")
    print(f"📊 Total Tables: {len(table_names)}")
    for t, rows in full_database_dump.items():
        print(f"   • {t}: {len(rows)} records")
    print("======================================================\n")

if __name__ == "__main__":
    export_all()

