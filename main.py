import os
import hikari
import commands
import autocomplete
import asyncio
import sys

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
        await command(interaction, bot)
    else:
        await interaction.create_initial_response(hikari.ResponseType.MESSAGE_CREATE, "Internal error", flags=hikari.MessageFlag.EPHEMERAL)

async def handle_autocomplete(interaction: hikari.AutocompleteInteraction):
    command_path = build_interaction_path(interaction)
    handler = autocomplete.get(command_path) or commands.get(interaction.command_name)

    if handler:
        return await handler(interaction, bot)
    return interaction.build_response([])

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
    group_command.add_option(hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND, name="call", description="Call a group",
                                                  options=[
                                                      hikari.CommandOption(type=hikari.OptionType.STRING, name="name",
                                                                           description="Group name", max_length=32,
                                                                           is_required=True, autocomplete=True),
                                                      hikari.CommandOption(type=hikari.OptionType.STRING, name="msg",
                                                                           description="Message to send with a call", max_length=50, is_required=False)
                                                  ]))
    group_command.add_option(hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND, name="delete", description="Delete a call group",
                                                  options=[
                                                      hikari.CommandOption(type=hikari.OptionType.STRING, name="name",
                                                                           description="Group name", max_length=32,
                                                                           is_required=True, autocomplete=True)
                                                  ]))
    group_command.add_option(
        hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND_GROUP, name="set", description="Set a group parameter",
                             options=[
                                 hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND,
                                                      name="private",
                                                      description="Make a group invite-only",
                                                      options=[
                                                          hikari.CommandOption(type=hikari.OptionType.STRING,
                                                                               name="name",
                                                                               description="Group name", max_length=32,
                                                                               is_required=True, autocomplete=True),
                                                          hikari.CommandOption(
                                                              type=hikari.OptionType.BOOLEAN,
                                                              name="value",
                                                              description="Value of the parameter",
                                                              is_required=True)
                                                      ]),
                                 hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND,
                                                      name="member_calls",
                                                      description="All members can call the group",
                                                      options=[
                                                          hikari.CommandOption(type=hikari.OptionType.STRING,
                                                                               name="name",
                                                                               description="Group name", max_length=32,
                                                                               is_required=True, autocomplete=True),
                                                          hikari.CommandOption(
                                                              type=hikari.OptionType.BOOLEAN,
                                                              name="value",
                                                              description="Value of the parameter",
                                                              is_required=True)
                                                      ]),
                                 hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND,
                                                      name="external_calls",
                                                      description="Non-members can call Group",
                                                      options=[
                                                          hikari.CommandOption(type=hikari.OptionType.STRING,
                                                                               name="name",
                                                                               description="Group name", max_length=32,
                                                                               is_required=True, autocomplete=True),
                                                          hikari.CommandOption(
                                                              type=hikari.OptionType.BOOLEAN,
                                                              name="value",
                                                              description="Value of the parameter",
                                                              is_required=True)
                                                      ]),
                                 hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND,
                                                      name="max_members",
                                                      description="Max group members, 0 for no limit",
                                                      options=[
                                                          hikari.CommandOption(type=hikari.OptionType.STRING,
                                                                               name="name",
                                                                               description="Group name", max_length=32,
                                                                               is_required=True, autocomplete=True),
                                                          hikari.CommandOption(
                                                              type=hikari.OptionType.INTEGER,
                                                              name="value",
                                                              description="Value of the parameter",
                                                              is_required=True)
                                                      ])

                                 ]))

    await _bot.rest.set_application_commands(
        application=application.id,
        commands=[
            help_command,
            group_command
        ]
    )

bot = hikari.RESTBot(token=token, public_key=public_key)

bot.add_startup_callback(create_commands)
bot.set_listener(hikari.CommandInteraction, handle_command)
bot.set_listener(hikari.AutocompleteInteraction, handle_autocomplete)

bot.run()
