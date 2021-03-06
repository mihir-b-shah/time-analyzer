
drop table if exists Events;

create table if not exists Events (
    email   varchar(256)   not null,
    url     varchar(512)   not null,
    host    varchar(128)   not null,
    wasted  bit            not null,
    start   bigint         not null, 
    end     bigint         not null
);