from typing import Callable, Coroutine, Any, Sequence
import hikari
import data
import database

def get_option(options: Sequence[hikari.CommandInteractionOption], name: str, default = None):
    for o in options:
        if o.name == name:
            return o.value
    return default

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
    if not interaction.guild_id:
        return
    print(interaction.options)
    await database.create_group(interaction.user.id, interaction.guild_id, str(get_option(interaction.options[0].options, "name", "new group")), bool(get_option(interaction.options[0].options, "private", False)))
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