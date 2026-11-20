
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    city_key as unique_field,
    count(*) as n_records

from "air_quality"."marts"."dim_city"
where city_key is not null
group by city_key
having count(*) > 1



  
  
      
    ) dbt_internal_test