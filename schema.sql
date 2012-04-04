drop table if exists projects;
drop table if exists numbers;
create table projects (
    id integer primary key autoincrement,
    title string not null,
    description string not null,
    votes integer
);

create table numbers (
    num string primary key
);
