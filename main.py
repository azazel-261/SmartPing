import os
import hikari
import commands

token = os.getenv("DISCORD_TOKEN")
public_key = os.getenv("PUBLIC_KEY")

if not token or not public_key:
    exit(-1)

async def handle_command(interaction: hikari.CommandInteraction):
    command_path = [interaction.command_name]

    subcommands = [_ for _ in interaction.options if _.type == hikari.OptionType.SUB_COMMAND or _.type == hikari.OptionType.SUB_COMMAND_GROUP]

    for sub in subcommands:
        command_path.append(sub.name)

    command = commands.get(" ".join(command_path)) or commands.get(interaction.command_name)

    if command:
        await command(interaction, bot)
    else:
        await interaction.create_initial_response(hikari.ResponseType.MESSAGE_CREATE, "Internal error", flags=hikari.MessageFlag.EPHEMERAL)

async def handle_autocomplete(interaction: hikari.AutocompleteInteraction):
    return interaction.build_response(
        [
            hikari.impl.AutocompleteChoiceBuilder(name="foo", value="a"),
            hikari.impl.AutocompleteChoiceBuilder(name="bar", value="b"),
            hikari.impl.AutocompleteChoiceBuilder(name="baz", value="c"),
        ]
    )

async def create_commands(_bot: hikari.RESTBot):
    application = await _bot.rest.fetch_application()

    help_command = _bot.rest.slash_command_builder("help", "Get help with using SmartPing!")
    help_command.add_option(hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND, name="commands", description="List bot commands"))
    help_command.add_option(hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND, name="attributes", description="List all possible group attributes"))

    group_command = _bot.rest.slash_command_builder("group", "Manage groups").set_context_types([hikari.ApplicationContextType.GUILD])
    group_command.add_option(hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND, name="create", description="Create a new call group",
                                                   options=[
                                                       hikari.CommandOption(type=hikari.OptionType.STRING, name="name",
                                                                            description="Group name", max_length=32,
                                                                            is_required=True),
                                                       hikari.CommandOption(type=hikari.OptionType.BOOLEAN,
                                                                            name="private",
                                                                            description="Make the group invite-only",
                                                                            is_required=False)
                                                   ]))
    group_command.add_option(hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND, name="join", description="Join an existing call group",
                                                  options=[
                                                      hikari.CommandOption(type=hikari.OptionType.STRING, name="name",
                                                                           description="Group name", max_length=32, is_required=True, autocomplete=True)
                                                  ]))
    group_command.add_option(hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND, name="leave", description="Leave a call group",
                                                  options=[
                                                      hikari.CommandOption(type=hikari.OptionType.STRING, name="name",
                                                                           description="Group name", max_length=32, is_required=True, autocomplete=True)
                                                  ]))
    group_command.add_option(hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND, name="leaveall", description="Leave all call groups in the server"))

    await _bot.rest.set_application_commands(
        application=application.id,
        commands=[
            help_command,
            group_command
        ],
    )

bot = hikari.RESTBot(token=token, public_key=public_key)

bot.add_startup_callback(create_commands)
bot.set_listener(hikari.CommandInteraction, handle_command)
bot.set_listener(hikari.AutocompleteInteraction, handle_autocomplete)

bot.run()
