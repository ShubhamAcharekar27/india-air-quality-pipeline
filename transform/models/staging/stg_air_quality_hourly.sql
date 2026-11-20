with source as (

    select * from {{ source('raw', 'air_quality_hourly') }}

),

ranked as (

    select
        *,
        row_number() over (
            partition by city, reading_time
            order by ingestion_date desc, source_file desc
        ) as row_num
    from source

)

select
    city,
    reading_time,
    cast(reading_time as date) as reading_date,
    pm10,
    pm2_5,
    carbon_monoxide,
    nitrogen_dioxide,
    sulphur_dioxide,
    ozone,
    us_aqi,
    ingestion_date
from ranked
where row_num = 1