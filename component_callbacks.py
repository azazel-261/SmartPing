import database
import hikari
from typing import Callable, Coroutine, Any


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

commands: dict[str, Callable[[hikari.ComponentInteraction, hikari.RESTBot], Coroutine[Any, Any, None]]] = {
    "inv": handle_invite_callback
}

def get(name: str):
    return commands.get(name, None)