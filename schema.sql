create table groups
(
    id             bigserial
        primary key,
    owner_id       bigint                not null,
    last_call      timestamp,
    private        boolean default false not null,
    name           varchar(32),
    member_calls   boolean default true  not null,
    external_calls boolean default false not null,
    guild_id       bigint                not null,
    max_members    integer default 0     not null,
    member_invites boolean default true  not null,
    constraint uq_groups_name_guild_id
        unique (name, guild_id)
);

create index ix_groups_name
    on groups using hash (name);

create table group_relations
(
    user_id   bigint                              not null,
    group_id  bigint                              not null
        constraint fk_group_relations_group_id
            references groups
            on delete cascade,
    joined_at timestamp default clock_timestamp() not null,
    constraint pk_group_relations_user_id_group_id
        primary key (user_id, group_id)
);
