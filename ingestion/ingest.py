import json
from datetime import date
from pathlib import Path

import requests

API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

CITIES = {
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.6139, 77.2090),
    "Bengaluru": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
}

HOURLY_FIELDS = "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,us_aqi"
RAW_DIR = Path("data/raw/air_quality")


def fetch_city(name: str, lat: float, lon: float) -> dict:
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": HOURLY_FIELDS,
        "timezone": "Asia/Kolkata",
        "past_days": 1,
        "forecast_days": 1,
    }
    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def save_raw(name: str, payload: dict, run_date: date) -> Path:
    out_dir = RAW_DIR / f"city={name}" / f"date={run_date.isoformat()}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "data.json"
    out_file.write_text(json.dumps(payload))
    return out_file


def main() -> None:
    today = date.today()
    for name, (lat, lon) in CITIES.items():
        payload = fetch_city(name, lat, lon)
        path = save_raw(name, payload, today)
        print(f"Saved {name} -> {path}")


if __name__ == "__main__":
    main()