import json
import logging
import sys
from datetime import date
from pathlib import Path

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

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
    failed = []

    for name, (lat, lon) in CITIES.items():
        try:
            payload = fetch_city(name, lat, lon)
            path = save_raw(name, payload, today)
            logger.info("Saved %s -> %s", name, path)
        except requests.exceptions.RequestException as exc:
            logger.error("API call failed for %s: %s", name, exc)
            failed.append(name)
        except (OSError, ValueError) as exc:
            logger.error("Could not save data for %s: %s", name, exc)
            failed.append(name)

    if failed:
        logger.error("Ingestion finished with failures: %s", ", ".join(failed))
        sys.exit(1)

    logger.info("Ingestion finished successfully for all %d cities", len(CITIES))


if __name__ == "__main__":
    main()