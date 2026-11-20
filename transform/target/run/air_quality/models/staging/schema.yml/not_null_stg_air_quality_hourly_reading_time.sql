
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select reading_time
from "air_quality"."staging"."stg_air_quality_hourly"
where reading_time is null



  
  
      
    ) dbt_internal_test