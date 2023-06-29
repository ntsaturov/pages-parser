SET SCHEMA 'public';

CREATE TABLE tasks (
    id character varying(255),
    execution_timestamp timestamp without time zone,
    creation_timestamp timestamp without time zone,
    status integer,
    url character varying(500),
    data text
);

insert into tasks (id, creation_timestamp, status, url, data) values (1, now(), 0, 'https://dzen.ru/', '');
insert into tasks (id, creation_timestamp, status, url, data) values (2, now(), 0, 'https://askubuntu.com/', '');
insert into tasks (id, creation_timestamp, status, url, data) values (3, now(), 0, 'https://github.com', '');
insert into tasks (id, creation_timestamp, status, url, data) values (4, now(), 0, 'https://habr.com', '');
insert into tasks (id, creation_timestamp, status, url, data) values (5, now(), 0, 'https://example.com/', '');
