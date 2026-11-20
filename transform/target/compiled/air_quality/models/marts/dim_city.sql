select
    md5(city) as city_key,
    city,
    state,
    latitude,
    longitude
from "air_quality"."main"."cities"