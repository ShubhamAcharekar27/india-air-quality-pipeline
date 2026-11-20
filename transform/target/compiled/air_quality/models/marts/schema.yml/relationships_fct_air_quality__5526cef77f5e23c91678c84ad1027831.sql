
    
    

with child as (
    select date_day as from_field
    from "air_quality"."marts"."fct_air_quality_hourly"
    where date_day is not null
),

parent as (
    select date_day as to_field
    from "air_quality"."marts"."dim_date"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


