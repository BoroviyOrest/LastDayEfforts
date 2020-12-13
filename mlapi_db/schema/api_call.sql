create table "API_CALL" (
    id serial constraint api_call_pk primary key,
    user_uuid uuid constraint api_call_user_fk references "USER" on delete cascade not null,
    image_id int unique constraint api_call_image_fk references "IMAGE" on DELETE cascade not null,
    created_on timestamp default now()
);
