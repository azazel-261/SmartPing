import aiopg
import os

dsn = f'dbname=data user={os.getenv("DATABASE_USER")} password={os.getenv("DATABASE_PASSWORD")} host={os.getenv("DATABASE_HOST")} port={os.getenv("DATABASE_PORT")}'

pool = None

async def get_connection():
    global pool
    pool = pool or await aiopg.create_pool(dsn=dsn)

    return await pool.acquire()

async def create_group(owner_id: int, guild_id: int, name: str,
                       private: bool = False, member_calls: bool = True,
                       ext_calls: bool = True):
    print("Group create")
    conn = await get_connection()
    cursor = await conn.cursor()
    await cursor.execute("INSERT INTO groups(owner_id, guild_id, name, private, member_calls, external_calls) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                         (owner_id, guild_id, name, private, member_calls, ext_calls, ))
    group_id: int = await cursor.fetchone()
    await cursor.execute("INSERT INTO group_relations(user_id, group_id) VALUES (%s, %s)", (owner_id, group_id))
    cursor.close()
    await conn.close()
