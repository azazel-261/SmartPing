import asyncio
from typing import Callable, Coroutine, Any, Sequence

import hikari
import database
import utils
from database import generator_fetch_users_for_call


def get_option(options: Sequence[hikari.CommandInteractionOption], name: str, default=None):
    for o in options:
        if o.name == name:
            return o.value
    return default

async def create_command(interaction: hikari.CommandInteraction, bot: hikari.RESTBot):
    await interaction.create_initial_response(hikari.ResponseType.DEFERRED_MESSAGE_CREATE,
                                              flags=hikari.MessageFlag.EPHEMERAL)
    if not interaction.guild_id:
        return
    try:
        args = utils.map_options(interaction.options)
        await database.create_group(interaction.user.id, interaction.guild_id,
                                    args['name'],
                                    args.get('private', False))
        await interaction.edit_initial_response("Group created successfully")
    except database.DatabaseError as e:
        await interaction.edit_initial_response(e.args[0])


async def join_command(interaction: hikari.CommandInteraction, bot: hikari.RESTBot):
    await interaction.create_initial_response(hikari.ResponseType.DEFERRED_MESSAGE_CREATE,
                                              flags=hikari.MessageFlag.EPHEMERAL)
    if not interaction.guild_id:
        return
    try:
        args = utils.map_options(interaction.options)
        await database.join_group(args['name'], interaction.guild_id, interaction.user.id,
                                  await utils.check_if_admin(bot, interaction.user.id, interaction.guild_id))
        await interaction.edit_initial_response("Group joined successfully")
    except database.DatabaseError as e:
        await interaction.edit_initial_response(e.args[0])


async def leave_command(interaction: hikari.CommandInteraction, bot: hikari.RESTBot):
    await interaction.create_initial_response(hikari.ResponseType.DEFERRED_MESSAGE_CREATE,
                                              flags=hikari.MessageFlag.EPHEMERAL)
    if not interaction.guild_id:
        return
    try:
        args = utils.map_options(interaction.options)
        await database.leave_group(args['name'], interaction.guild_id, interaction.user.id)
        await interaction.edit_initial_response("Group leave successful")
    except database.DatabaseError as e:
        await interaction.edit_initial_response(e.args[0])


async def leaveall_command(interaction: hikari.CommandInteraction, bot: hikari.RESTBot):
    await interaction.create_initial_response(hikari.ResponseType.DEFERRED_MESSAGE_CREATE,
                                              flags=hikari.MessageFlag.EPHEMERAL)
    if not interaction.guild_id:
        return
    try:
        await database.leave_all_groups(interaction.guild_id, interaction.user.id)
        await interaction.edit_initial_response("Successfully left all groups")
    except database.DatabaseError as e:
        await interaction.edit_initial_response(e.args[0])


async def delete_command(interaction: hikari.CommandInteraction, bot: hikari.RESTBot):
    await interaction.create_initial_response(hikari.ResponseType.DEFERRED_MESSAGE_CREATE,
                                              flags=hikari.MessageFlag.EPHEMERAL)
    if not interaction.guild_id:
        return
    try:
        args = utils.map_options(interaction.options)
        await database.delete_group(args['name'], interaction.guild_id, interaction.user.id,
                                    await utils.check_if_admin(bot, interaction.user.id, interaction.guild_id))
        await interaction.edit_initial_response("Successfully deleted group")
    except database.DatabaseError as e:
        await interaction.edit_initial_response(e.args[0])


async def call_command(interaction: hikari.CommandInteraction, bot: hikari.RESTBot):
    await interaction.create_initial_response(hikari.ResponseType.DEFERRED_MESSAGE_CREATE,
                                              flags=hikari.MessageFlag.EPHEMERAL)
    try:
        args = utils.map_options(interaction.options)
        group_id = await database.prepare_group_for_call(args['name'], interaction.guild_id, interaction.user.id,
                                                    await utils.check_if_admin(bot, interaction.user.id, interaction.guild_id))
    except database.DatabaseError as e:
        await interaction.edit_initial_response(e.args[0])
        return
    await interaction.delete_initial_response()
    msg = args.get('msg', "") + "\n"
    generator = generator_fetch_users_for_call(group_id)
    await bot.rest.create_message(interaction.channel_id, f"Call by <@{interaction.user.id}>\n{msg}")
    async for group in generator:
        if not group:
            continue
        await asyncio.sleep(1)
        ids = [_[0] for _ in group]
        pings = "".join([f"<@{_}>" for _ in ids])
        out = await bot.rest.create_message(interaction.channel_id, msg + pings, user_mentions=ids)
        await asyncio.sleep(0.5)
        await out.delete()


async def invite_command(interaction: hikari.CommandInteraction, bot: hikari.RESTBot):
    await interaction.create_initial_response(hikari.ResponseType.DEFERRED_MESSAGE_CREATE,
                                              flags=hikari.MessageFlag.EPHEMERAL)
    try:
        args = utils.map_options(interaction.options)
        group = await database.fetch_group_for_invite(args['name'], interaction.guild_id,
                                                         interaction.user.id,
                                                         await utils.check_if_admin(bot, interaction.user.id,
                                                                                    interaction.guild_id))
    except database.DatabaseError as e:
        await interaction.edit_initial_response(e.args[0])
        return
    await interaction.delete_initial_response()
    await bot.rest.create_message(interaction.channel_id,
                                  f"<@{args['user']}>, you've been invited to join call group {group[1]}",
                                  component=bot.rest.build_message_action_row()
                                  .add_interactive_button(hikari.ButtonStyle.PRIMARY,
                                                          f"inv:{group[0]}:{args['user']}:1",
                                                          label="Accept")
                                  .add_interactive_button(hikari.ButtonStyle.SECONDARY,
                                                          f"inv:{group[0]}:{args['user']}:0",
                                                          label="Reject"), user_mentions=[args['user']])


commands: dict[str, Callable[[hikari.CommandInteraction, hikari.RESTBot], Coroutine[Any, Any, None]]] = {
    "group create": create_command,
    "group join": join_command,
    "group leave": leave_command,
    "group leaveall": leaveall_command,
    "group delete": delete_command,
    "group call": call_command,
    "group invite": invite_command
}


def get(name: str):
    return commands.get(name, None)
