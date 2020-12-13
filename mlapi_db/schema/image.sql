create table "IMAGE" (
    id serial constraint image_pk primary key,
    style_id int constraint image_style_fk references "STYLE" on DELETE cascade not null,
    raw_image_name varchar,
    transformed_image_name varchar
);
