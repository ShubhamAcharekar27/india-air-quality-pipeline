
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  select *
from "air_quality"."staging"."stg_air_quality_hourly"
where pm2_5 < 0
   or pm10 < 0
   or us_aqi < 0
   or us_aqi > 500
  
  
      
    ) dbt_internal_test