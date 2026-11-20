
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with child as (
    select city_key as from_field
    from "air_quality"."marts"."fct_air_quality_hourly"
    where city_key is not null
),

parent as (
    select city_key as to_field
    from "air_quality"."marts"."dim_city"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null



  
  
      
    ) dbt_internal_test