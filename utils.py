from typing import Sequence
import hikari

async def check_if_admin(bot: hikari.RESTBot, user_id: int, guild_id: int):
    guild = await bot.rest.fetch_guild(guild_id)
    if guild.owner_id == user_id:
        return True
    member = await bot.rest.fetch_member(guild_id, user_id)
    roles = await member.fetch_roles()
    for role in roles:
        if role.permissions & hikari.Permissions.ADMINISTRATOR:
            return True
    return False


def map_options(options: Sequence[hikari.CommandInteractionOption] | None):
    out = {}
    if not options:
        return out
    for option in options:
        if option.type == hikari.OptionType.SUB_COMMAND or option.type == hikari.OptionType.SUB_COMMAND_GROUP:
            extra = map_options(option.options)
            out.update(extra)
        else:
            out[option.name] = option.value
    return out