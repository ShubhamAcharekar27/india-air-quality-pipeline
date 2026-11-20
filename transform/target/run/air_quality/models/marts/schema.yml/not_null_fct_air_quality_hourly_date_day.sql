
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select date_day
from "air_quality"."marts"."fct_air_quality_hourly"
where date_day is null



  
  
      
    ) dbt_internal_test