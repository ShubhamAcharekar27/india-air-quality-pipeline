
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select city_key
from "air_quality"."marts"."dim_city"
where city_key is null



  
  
      
    ) dbt_internal_test