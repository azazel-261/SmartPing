from typing import Callable, Coroutine, Any
import hikari
import data

async def help_command(body: str, event: hikari.GuildMessageCreateEvent, bot: hikari.GatewayBot):
    out = "Unknown help section"
    match body:
        case "":
            out = data.help_message
        case "attr":
            out = data.attribute_help_message
    await bot.rest.create_message(event.message.channel_id, out)

async def create_command(body: str, event: hikari.GuildMessageCreateEvent, bot: hikari.GatewayBot):
    pass

async def join_command(body: str, event: hikari.GuildMessageCreateEvent, bot: hikari.GatewayBot):
    pass

commands: dict[str, Callable[[str, hikari.GuildMessageCreateEvent, hikari.GatewayBot], Coroutine[Any, Any, None]]] = {
    "help" : help_command,
    "create": create_command,
    "join" : join_command
}

def get(name: str):
    return commands.get(name, None)