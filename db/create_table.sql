SET SCHEMA 'public';

CREATE TABLE tasks (
    id character varying(255),
    execution_timestamp timestamp without time zone,
    creation_timestamp timestamp without time zone,
    status integer,
    url character varying(500),
    data text
);

insert into tasks (id, creation_timestamp, status, url, data) values (1, now(), 0, 'http://url_1.ru', 'some test data');
insert into tasks (id, creation_timestamp, status, url, data) values (2, now(), 0, 'http://url_2.ru', 'some test data');
insert into tasks (id, creation_timestamp, status, url, data) values (3, now(), 0, 'http://url_3.ru', 'some test data');
insert into tasks (id, creation_timestamp, status, url, data) values (4, now(), 0, 'http://url_4.ru', 'some test data');
insert into tasks (id, creation_timestamp, status, url, data) values (5, now(), 0, 'http://url_5.ru', 'some test data');
