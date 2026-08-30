from typing import Callable, Coroutine, Any
import hikari
import data

async def help_command(interaction: hikari.CommandInteraction, bot: hikari.RESTBot):
    await interaction.create_initial_response(hikari.ResponseType.DEFERRED_MESSAGE_CREATE, flags=hikari.MessageFlag.EPHEMERAL)
    out = "Unknown help section"
    match interaction.options[0].name:
        case "commands":
            out = data.help_message
        case "attributes":
            out = data.attribute_help_message
    await interaction.edit_initial_response(out)

async def create_command(interaction: hikari.CommandInteraction, bot: hikari.RESTBot):
    await interaction.create_initial_response(hikari.ResponseType.DEFERRED_MESSAGE_CREATE, flags=hikari.MessageFlag.EPHEMERAL)
    await interaction.edit_initial_response("Group create")

async def join_command(interaction: hikari.CommandInteraction, bot: hikari.RESTBot):
    await interaction.create_initial_response(hikari.ResponseType.DEFERRED_MESSAGE_CREATE,
                                              flags=hikari.MessageFlag.EPHEMERAL)
    await interaction.edit_initial_response("Group join")

async def leave_command(interaction: hikari.CommandInteraction, bot: hikari.RESTBot):
    await interaction.create_initial_response(hikari.ResponseType.DEFERRED_MESSAGE_CREATE, flags=hikari.MessageFlag.EPHEMERAL)
    await interaction.edit_initial_response("Group leave")

async def leaveall_command(interaction: hikari.CommandInteraction, bot: hikari.RESTBot):
    await interaction.create_initial_response(hikari.ResponseType.DEFERRED_MESSAGE_CREATE, flags=hikari.MessageFlag.EPHEMERAL)
    await interaction.edit_initial_response("Group leaveall")

async def call_command(interaction: hikari.CommandInteraction, bot: hikari.RESTBot):
    await interaction.create_initial_response(hikari.ResponseType.DEFERRED_MESSAGE_CREATE, flags=hikari.MessageFlag.EPHEMERAL)
    await interaction.delete_initial_response()
    await bot.rest.create_message(interaction.channel_id, "CALL")

commands: dict[str, Callable[[hikari.CommandInteraction, hikari.RESTBot], Coroutine[Any, Any, None]]] = {
    "help" : help_command,
    "group create": create_command,
    "group join" : join_command,
    "group leave" : leave_command,
    "group leaveall" : leaveall_command,
    "group call" : call_command
}

def get(name: str):
    return commands.get(name, None)