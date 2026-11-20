
    
    

select
    reading_id as unique_field,
    count(*) as n_records

from "air_quality"."marts"."fct_air_quality_hourly"
where reading_id is not null
group by reading_id
having count(*) > 1


