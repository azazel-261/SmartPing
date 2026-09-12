import database
import hikari
from typing import Callable, Coroutine, Any

import utils


async def handle_invite_callback(interaction: hikari.ComponentInteraction, bot: hikari.RESTBot):
    await interaction.create_initial_response(hikari.ResponseType.DEFERRED_MESSAGE_CREATE,
                                              flags=hikari.MessageFlag.EPHEMERAL)
    args = interaction.custom_id.split(":")
    target_group = int(args[1])
    target_user = int(args[2])
    decision = bool(int(args[3]))
    if target_user != interaction.user.id:
        await interaction.edit_initial_response("This invite is meant for someone else!")
        return
    if not decision:
        await interaction.delete_initial_response()
        await interaction.message.edit("Invite rejected", component=None)
        return
    try:
        await database.accept_join_invite(target_group, target_user)
        await interaction.delete_initial_response()
    except database.DatabaseError as e:
        await interaction.edit_initial_response(e.args[0])
    finally:
        await interaction.message.edit("Invite accepted", component=None)


async def handle_delete_callback(interaction: hikari.ComponentInteraction, bot: hikari.RESTBot):
    await interaction.create_initial_response(hikari.ResponseType.DEFERRED_MESSAGE_UPDATE,
                                              flags=hikari.MessageFlag.EPHEMERAL)
    args = interaction.custom_id.split(":")
    target_group = int(args[1])
    executing_user = int(args[2])
    decision = bool(int(args[3]))
    if executing_user != interaction.user.id:
        await interaction.edit_initial_response("This dialog is meant for another user!", component=None)
        return
    if not decision:
        await interaction.delete_initial_response()
        return
    try:
        await database.delete_group(target_group, executing_user, await utils.check_if_admin(bot, executing_user, interaction.guild_id))
        await interaction.edit_initial_response("Group deleted successfully", component=None)
    except database.DatabaseError as e:
        await interaction.edit_initial_response(e.args[0])


async def handle_transfer_callback(interaction: hikari.ComponentInteraction, bot: hikari.RESTBot):
    await interaction.create_initial_response(hikari.ResponseType.DEFERRED_MESSAGE_UPDATE,
                                              flags=hikari.MessageFlag.EPHEMERAL)
    args = interaction.custom_id.split(":")
    target_group = int(args[1])
    executing_user = int(args[2])
    target_user = int(args[3])
    decision = bool(int(args[4]))
    if executing_user != interaction.user.id:
        await interaction.edit_initial_response("This dialog is meant for another user!", component=None)
        return
    if not decision:
        await interaction.delete_initial_response()
        return
    try:
        await database.transfer_group(target_group, executing_user, await utils.check_if_admin(bot, executing_user, interaction.guild_id), target_user)
        await interaction.edit_initial_response("Group transferred successfully", component=None)
    except database.DatabaseError as e:
        await interaction.edit_initial_response(e.args[0])


commands: dict[str, Callable[[hikari.ComponentInteraction, hikari.RESTBot], Coroutine[Any, Any, None]]] = {
    "inv": handle_invite_callback,
    "del": handle_delete_callback,
    "trs": handle_transfer_callback
}

def get(name: str):
    return commands.get(name, None)