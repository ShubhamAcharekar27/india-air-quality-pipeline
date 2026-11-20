
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        aqi_category as value_field,
        count(*) as n_records

    from "air_quality"."marts"."fct_air_quality_hourly"
    group by aqi_category

)

select *
from all_values
where value_field not in (
    'Good','Moderate','Unhealthy for Sensitive Groups','Unhealthy','Very Unhealthy','Hazardous'
)



  
  
      
    ) dbt_internal_test