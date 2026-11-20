
    
    

select
    city_key as unique_field,
    count(*) as n_records

from "air_quality"."marts"."dim_city"
where city_key is not null
group by city_key
having count(*) > 1


