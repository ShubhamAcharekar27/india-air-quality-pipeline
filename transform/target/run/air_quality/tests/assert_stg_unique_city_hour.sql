
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  select
    city,
    reading_time,
    count(*) as copies
from "air_quality"."staging"."stg_air_quality_hourly"
group by city, reading_time
having count(*) > 1
  
  
      
    ) dbt_internal_test