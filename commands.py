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
    pass

async def join_command(interaction: hikari.CommandInteraction, bot: hikari.RESTBot):
    pass

commands: dict[str, Callable[[hikari.CommandInteraction, hikari.RESTBot], Coroutine[Any, Any, None]]] = {
    "help" : help_command,
    "create": create_command,
    "join" : join_command
}

def get(name: str):
    return commands.get(name, None)