import hikari

async def check_if_admin(bot: hikari.RESTBot, user_id: int, guild_id: int):
    member = await bot.rest.fetch_member(guild_id, user_id)
    roles = await member.fetch_roles()
    for role in roles:
        if role.permissions & hikari.Permissions.ADMINISTRATOR:
            return True
    return False