
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select city
from "air_quality"."staging"."stg_air_quality_hourly"
where city is null



  
  
      
    ) dbt_internal_test