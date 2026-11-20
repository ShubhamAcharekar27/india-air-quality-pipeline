
    

    create  table
      "air_quality"."marts"."fct_air_quality_hourly__dbt_tmp"
  
    
    as (
      select
    md5(city || '|' || cast(reading_time as varchar)) as reading_id,
    md5(city) as city_key,
    reading_date as date_day,
    reading_time,
    pm10,
    pm2_5,
    carbon_monoxide,
    nitrogen_dioxide,
    sulphur_dioxide,
    ozone,
    us_aqi,
    case
        when us_aqi is null then null
        when us_aqi <= 50 then 'Good'
        when us_aqi <= 100 then 'Moderate'
        when us_aqi <= 150 then 'Unhealthy for Sensitive Groups'
        when us_aqi <= 200 then 'Unhealthy'
        when us_aqi <= 300 then 'Very Unhealthy'
        else 'Hazardous'
    end as aqi_category
from "air_quality"."staging"."stg_air_quality_hourly"
    );
    
  