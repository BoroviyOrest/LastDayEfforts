create table "USER" (
    uuid uuid constraint user_pk primary key,
    email varchar unique,
    name varchar,
    salt varchar,
    hashed_password varchar,
    api_key varchar unique,
    calls_per_day_limit smallint default 10,
    is_active boolean default true,
    is_admin boolean default false
);
