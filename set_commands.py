import asyncio
import os
import hikari

TOKEN = str(os.getenv("DISCORD_TOKEN"))

async def main():
    rest = hikari.RESTApp()
    await rest.start()
    async with rest.acquire(TOKEN, "Bot") as bot:
        group_command = bot.slash_command_builder("group", "Manage groups").set_context_types(
            [hikari.ApplicationContextType.GUILD])
        group_command.add_option(
            hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND, name="create",
                                 description="Create a new call group",  # ✅
                                 options=[
                                     hikari.CommandOption(type=hikari.OptionType.STRING, name="name",
                                                          description="Group name", max_length=32,
                                                          is_required=True),
                                     hikari.CommandOption(type=hikari.OptionType.BOOLEAN,
                                                          name="private",
                                                          description="Make the group invite-only",
                                                          is_required=False)
                                 ]))
        group_command.add_option(
            hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND, name="join",
                                 description="Join an existing call group",  # ✅
                                 options=[
                                     hikari.CommandOption(type=hikari.OptionType.STRING, name="name",
                                                          description="Group name", max_length=32, is_required=True,
                                                          autocomplete=True)
                                 ]))
        group_command.add_option(
            hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND, name="leave", description="Leave a call group",
                                 # ✅
                                 options=[
                                     hikari.CommandOption(type=hikari.OptionType.STRING, name="name",
                                                          description="Group name", max_length=32, is_required=True,
                                                          autocomplete=True)
                                 ]))
        group_command.add_option(hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND, name="leaveall",  # ✅
                                                      description="Leave all call groups in the server"))
        group_command.add_option(
            hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND, name="call", description="Call a group",  # ✅
                                 options=[
                                     hikari.CommandOption(type=hikari.OptionType.STRING, name="name",
                                                          description="Group name", max_length=32,
                                                          is_required=True, autocomplete=True),
                                     hikari.CommandOption(type=hikari.OptionType.STRING, name="msg",
                                                          description="Message to send with a call", max_length=50,
                                                          is_required=False)
                                 ]))
        group_command.add_option(
            hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND, name="delete", description="Delete a call group",
                                 # ✅
                                 options=[
                                     hikari.CommandOption(type=hikari.OptionType.STRING, name="name",
                                                          description="Group name", max_length=32,
                                                          is_required=True, autocomplete=True)
                                 ]))
        group_command.add_option(
            hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND, name="invite",
                                 description="Invite another user to a call group",  # ✅
                                 options=[
                                     hikari.CommandOption(type=hikari.OptionType.STRING, name="name",
                                                          description="Group name", max_length=32,
                                                          is_required=True, autocomplete=True),
                                     hikari.CommandOption(type=hikari.OptionType.USER, name="user",
                                                          description="User to be invited", is_required=True)
                                 ]))
        group_command.add_option(
            hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND_GROUP, name="set",
                                 description="Set a group parameter",
                                 options=[
                                     hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND,
                                                          name="private",
                                                          description="Make a group invite-only",
                                                          options=[
                                                              hikari.CommandOption(type=hikari.OptionType.STRING,
                                                                                   name="name",
                                                                                   description="Group name",
                                                                                   max_length=32,
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
                                                                                   description="Group name",
                                                                                   max_length=32,
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
                                                                                   description="Group name",
                                                                                   max_length=32,
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
                                                                                   description="Group name",
                                                                                   max_length=32,
                                                                                   is_required=True, autocomplete=True),
                                                              hikari.CommandOption(
                                                                  type=hikari.OptionType.INTEGER,
                                                                  name="value",
                                                                  description="Value of the parameter",
                                                                  is_required=True,
                                                                  min_value=0)
                                                          ]),
                                     hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND,
                                                          name="member_invites",
                                                          description="Whether or not members are allowed to invite others",
                                                          options=[
                                                              hikari.CommandOption(type=hikari.OptionType.STRING,
                                                                                   name="name",
                                                                                   description="Group name",
                                                                                   max_length=32,
                                                                                   is_required=True, autocomplete=True),
                                                              hikari.CommandOption(
                                                                  type=hikari.OptionType.BOOLEAN,
                                                                  name="value",
                                                                  description="Value of the parameter",
                                                                  is_required=True)
                                                          ]),
                                     hikari.CommandOption(type=hikari.OptionType.SUB_COMMAND,
                                                          name="owner",
                                                          description="Transfer group ownership to another person",
                                                          options=[
                                                              hikari.CommandOption(type=hikari.OptionType.STRING,
                                                                                   name="name",
                                                                                   description="Group name",
                                                                                   max_length=32,
                                                                                   is_required=True, autocomplete=True),
                                                              hikari.CommandOption(type=hikari.OptionType.USER,
                                                                                   name="user",
                                                                                   description="New group owner",
                                                                                   is_required=True)
                                                          ])

                                 ]))
        app = await bot.fetch_application()
        await bot.set_application_commands(
            app.id,
            [
                group_command
            ]
        )
        await rest.close()


asyncio.run(main())