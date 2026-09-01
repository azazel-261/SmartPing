import aiopg
import os
import psycopg2

dsn = f'dbname=data user={os.getenv("DATABASE_USER")} password={os.getenv("DATABASE_PASSWORD")} host={os.getenv("DATABASE_HOST")} port={os.getenv("DATABASE_PORT")}'

async def get_connection():
    conn = await aiopg.connect(dsn=dsn)
    return conn

async def fetch_joinable_groups_autocomplete(search: str, guild_id: int, user_id: int, admin: bool = False):
    async with await get_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT g.name FROM (SELECT name, id, private FROM groups WHERE guild_id = %s) g \
            LEFT JOIN (SELECT group_id FROM group_relations WHERE user_id = %s) AS r \
            ON g.id = r.group_id WHERE g.name LIKE %s AND r.group_id IS NULL AND (g.private = FALSE OR %s = TRUE)", (guild_id, user_id, f"{search}%", admin, ))
            res = await cursor.fetchall()
            return res

async def fetch_user_groups_autocomplete(search: str, guild_id: int, user_id: int):
    async with await get_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT g.name FROM (SELECT id, name FROM groups WHERE guild_id = %s) g \
            INNER JOIN (SELECT group_id FROM group_relations WHERE user_id = %s) r ON g.id = r.group_id WHERE g.name LIKE %s", (guild_id, user_id, f"{search}%", ))
            res = await cursor.fetchall()
            return res

async def fetch_group_autocomplete(guild_id: int, admin: bool = False):
    async with await get_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT name FROM groups WHERE guild_id = %s AND (private = FALSE OR %s = TRUE)", (guild_id, admin, ))
            res = await cursor.fetchall()
            return res

async def count_group_members(group_id: int):
    async with await get_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT count(*) FROM group_relations WHERE group_id = %s", (group_id, ))
            res = await cursor.fetchone()
            if res:
                return res[0]
            return 0

async def delete_if_empty(group_id: int):
    member_count = await count_group_members(group_id)
    if not member_count:
        async with await get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("DELETE FROM groups WHERE id = %s", (group_id, ))


async def create_group(owner_id: int, guild_id: int, name: str,
                       private: bool = False, member_calls: bool = True,
                       ext_calls: bool = True):
    async with await get_connection() as conn:
        async with conn.cursor() as cursor:
            try:
                await cursor.execute("INSERT INTO groups(owner_id, guild_id, name, private, member_calls, external_calls) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                                     (owner_id, guild_id, name, private, member_calls, ext_calls, ))
            except psycopg2.errors.UniqueViolation:
                return 1
            group_id: int = await cursor.fetchone()
            await cursor.execute("INSERT INTO group_relations(user_id, group_id) VALUES (%s, %s)", (owner_id, group_id))
            return 0

async def join_group(name: str, guild_id: int, user_id: int, admin: bool = False):
    async with await get_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT id, max_members FROM groups WHERE guild_id = %s AND name = %s AND (private = FALSE OR %s = TRUE)", (guild_id, name, admin))
            res = await cursor.fetchone()
            if not res:
                return 3
            if res[1]:
                member_count = await count_group_members(res[0])
                if member_count >= res[1]:
                    return 4
            try:
                await cursor.execute("INSERT INTO group_relations (user_id, group_id) VALUES (%s, %s)", (user_id, res[0]))
            except psycopg2.errors.UniqueViolation:
                return 2
            return 0

async def leave_group(name: str, guild_id: int, user_id: int):
    async with await get_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT id FROM groups WHERE guild_id = %s AND name = %s", (guild_id, name, ))
            group_res = await cursor.fetchone()
            if not group_res:
                return 3
            await cursor.execute("DELETE FROM group_relations WHERE group_id = %s AND user_id = %s RETURNING group_id", (group_res[0], user_id, ))
            res = await cursor.fetchone()
            if not res:
                return 5
            await delete_if_empty(res[0])
            return 0

async def leave_all_groups(guild_id: int, user_id: int):
    async with await get_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("DELETE FROM group_relations r USING groups g \
            WHERE r.group_id = g.id AND g.guild_id = %s AND r.user_id = %s RETURNING r.group_id", (guild_id, user_id, ))
            res = await cursor.fetchone()
            if not res:
                return 6
            while res:
                await delete_if_empty(res[0])
                res = await cursor.fetchone()
            return 0
