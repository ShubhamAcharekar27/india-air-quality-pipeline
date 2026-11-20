with dates as (

    select distinct reading_date as date_day
    from {{ ref('stg_air_quality_hourly') }}

)

select
    date_day,
    year(date_day) as year,
    month(date_day) as month,
    monthname(date_day) as month_name,
    day(date_day) as day,
    dayname(date_day) as day_name,
    dayofweek(date_day) in (0, 6) as is_weekend
from dates