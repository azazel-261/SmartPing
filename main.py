import os
import hikari
import commands
import autocomplete
import component_callbacks
import asyncio
import sys
import utils

if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

token = os.getenv("DISCORD_TOKEN")
public_key = os.getenv("PUBLIC_KEY")

if not token or not public_key:
    exit(-1)


def build_interaction_path(interaction: hikari.CommandInteraction | hikari.AutocompleteInteraction):
    path = [interaction.command_name]

    options = interaction.options

    while options:
        if options[0].type == hikari.OptionType.SUB_COMMAND or options[0].type == hikari.OptionType.SUB_COMMAND_GROUP:
            path.append(options[0].name)
            options = options[0].options
        else:
            break
    return " ".join(path)


async def handle_command(interaction: hikari.CommandInteraction):
    command_path = build_interaction_path(interaction)
    command = commands.get(command_path) or commands.get(interaction.command_name)

    if command:
        await command(interaction, bot, utils.map_options(interaction.options))
    else:
        await interaction.create_initial_response(hikari.ResponseType.MESSAGE_CREATE, "Internal error",
                                                  flags=hikari.MessageFlag.EPHEMERAL)


async def handle_component(interaction: hikari.ComponentInteraction):
    callback_id = interaction.custom_id.split(":")[0]
    callback = component_callbacks.get(callback_id)

    if callback:
        await callback(interaction, bot)
    else:
        await interaction.create_initial_response(hikari.ResponseType.MESSAGE_CREATE, "Internal error",
                                                  flags=hikari.MessageFlag.EPHEMERAL)
        

async def handle_autocomplete(interaction: hikari.AutocompleteInteraction):
    command_path = build_interaction_path(interaction)
    handler = autocomplete.get(command_path) or commands.get(interaction.command_name)

    if handler:
        return await handler(interaction, bot, utils.map_options(interaction.options))
    return interaction.build_response([])

if __name__ == "__main__":
    bot = hikari.RESTBot(token=token, public_key=public_key)

    bot.set_listener(hikari.CommandInteraction, handle_command)
    bot.set_listener(hikari.AutocompleteInteraction, handle_autocomplete)
    bot.set_listener(hikari.ComponentInteraction, handle_component)

    bot.run()
