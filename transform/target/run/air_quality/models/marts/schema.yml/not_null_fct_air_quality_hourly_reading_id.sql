
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select reading_id
from "air_quality"."marts"."fct_air_quality_hourly"
where reading_id is null



  
  
      
    ) dbt_internal_test