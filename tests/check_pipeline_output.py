import sys

import duckdb

EXPECTED = {
    "raw.air_quality_hourly": 384,
    "staging.stg_air_quality_hourly": 288,
    "marts.fct_air_quality_hourly": 288,
}

con = duckdb.connect("warehouse/air_quality.duckdb", read_only=True)
failures = []

for table, expected in EXPECTED.items():
    actual = con.execute(f"select count(*) from {table}").fetchone()[0]
    status = "OK" if actual == expected else "MISMATCH"
    print(f"{status}: {table} has {actual} rows (expected {expected})")
    if actual != expected:
        failures.append(table)

con.close()

if failures:
    sys.exit(1)