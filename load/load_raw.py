import logging
import sys
from pathlib import Path

import duckdb

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

DB_PATH = Path("warehouse/air_quality.duckdb")
RAW_GLOB = "data/raw/air_quality/*/*/data.json"

LOAD_SQL = f"""
CREATE OR REPLACE TABLE raw.air_quality_hourly AS
SELECT
    city,
    CAST("date" AS DATE)              AS ingestion_date,
    CAST(unnest(hourly.time) AS TIMESTAMP) AS reading_time,
    unnest(hourly.pm10)               AS pm10,
    unnest(hourly.pm2_5)              AS pm2_5,
    unnest(hourly.carbon_monoxide)    AS carbon_monoxide,
    unnest(hourly.nitrogen_dioxide)   AS nitrogen_dioxide,
    unnest(hourly.sulphur_dioxide)    AS sulphur_dioxide,
    unnest(hourly.ozone)              AS ozone,
    unnest(hourly.us_aqi)             AS us_aqi,
    filename                          AS source_file
FROM read_json(
    '{RAW_GLOB}',
    hive_partitioning = true,
    filename = true
)
"""


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH))
    try:
        con.execute("CREATE SCHEMA IF NOT EXISTS raw")
        con.execute(LOAD_SQL)
        row_count = con.execute(
            "SELECT COUNT(*) FROM raw.air_quality_hourly"
        ).fetchone()[0]
        logger.info("Loaded %d rows into raw.air_quality_hourly", row_count)
    except duckdb.Error as exc:
        logger.error("Load failed: %s", exc)
        sys.exit(1)
    finally:
        con.close()


if __name__ == "__main__":
    main()