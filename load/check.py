import duckdb

con = duckdb.connect("warehouse/air_quality.duckdb", read_only=True)

print("\n--- Rows per city ---")
print(con.execute("""
    SELECT city, COUNT(*) AS row_count,
           MIN(reading_time) AS first_reading,
           MAX(reading_time) AS last_reading
    FROM raw.air_quality_hourly
    GROUP BY city
    ORDER BY city
""").df())

print("\n--- Sample rows ---")
print(con.execute("""
    SELECT * FROM raw.air_quality_hourly
    WHERE city = 'Mumbai'
    ORDER BY reading_time
    LIMIT 5
""").df())

print("\n--- Duplicate city/hour combinations ---")
print(con.execute("""
    SELECT city, reading_time, COUNT(*) AS copies
    FROM raw.air_quality_hourly
    GROUP BY city, reading_time
    HAVING COUNT(*) > 1
    LIMIT 10
""").df())