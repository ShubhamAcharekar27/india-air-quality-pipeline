
    

    create  table
      "air_quality"."marts"."dim_city__dbt_tmp"
  
    
    as (
      select
    md5(city) as city_key,
    city,
    state,
    latitude,
    longitude
from "air_quality"."main"."cities"
    );
    
  