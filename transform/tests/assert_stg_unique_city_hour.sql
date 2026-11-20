select
    city,
    reading_time,
    count(*) as copies
from {{ ref('stg_air_quality_hourly') }}
group by city, reading_time
having count(*) > 1