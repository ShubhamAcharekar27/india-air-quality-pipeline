import json
import math
from datetime import datetime, timedelta
from pathlib import Path

RAW_DIR = Path("data/raw/air_quality")
CITIES = ["Mumbai", "Delhi", "Bengaluru", "Chennai"]
HOURS_PER_FILE = 48


def build_hourly(start: datetime, shift: float) -> dict:
    hourly = {
        "time": [],
        "pm10": [],
        "pm2_5": [],
        "carbon_monoxide": [],
        "nitrogen_dioxide": [],
        "sulphur_dioxide": [],
        "ozone": [],
        "us_aqi": [],
    }
    for i in range(HOURS_PER_FILE):
        wave = math.sin(i / 4)
        hourly["time"].append((start + timedelta(hours=i)).strftime("%Y-%m-%dT%H:%M"))
        hourly["pm10"].append(round(60 + 20 * wave + shift, 1))
        hourly["pm2_5"].append(round(35 + 12 * wave + shift, 1))
        hourly["carbon_monoxide"].append(round(400 + 50 * wave, 1))
        hourly["nitrogen_dioxide"].append(round(25 + 5 * wave, 1))
        hourly["sulphur_dioxide"].append(round(10 + 2 * wave, 1))
        hourly["ozone"].append(round(40 + 10 * wave, 1))
        hourly["us_aqi"].append(int(80 + 25 * wave + shift))
    return hourly


def write_file(city: str, run_date: str, start: datetime, shift: float) -> None:
    out_file = RAW_DIR / f"city={city}" / f"date={run_date}" / "data.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    payload = {"latitude": 0.0, "longitude": 0.0, "hourly": build_hourly(start, shift)}
    out_file.write_text(json.dumps(payload))


def main() -> None:
    for index, city in enumerate(CITIES):
        # File 1 covers 1-2 Nov, file 2 covers 2-3 Nov: 2 Nov appears in both.
        write_file(city, "2026-11-02", datetime(2026, 11, 1), shift=index)
        write_file(city, "2026-11-03", datetime(2026, 11, 2), shift=index + 1)
    print(f"Wrote sample data for {len(CITIES)} cities under {RAW_DIR}")


if __name__ == "__main__":
    main()