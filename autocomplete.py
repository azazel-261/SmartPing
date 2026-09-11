from typing import Callable, Coroutine, Any
import hikari
import database
import utils


async def handle_join_autocomplete(interaction: hikari.AutocompleteInteraction, bot: hikari.RESTBot, args: dict[str, Any]):
    group_names = await database.fetch_joinable_groups_autocomplete(args['name'],
                                                                    interaction.guild_id, interaction.user.id,
                                                                    await utils.check_if_admin(bot, interaction.user.id,
                                                                                               interaction.guild_id))
    return interaction.build_response([hikari.impl.AutocompleteChoiceBuilder(_[0], _[0]) for _ in group_names])


async def handle_leave_autocomplete(interaction: hikari.AutocompleteInteraction, bot: hikari.RESTBot, args: dict[str, Any]):
    group_names = await database.fetch_user_groups_autocomplete(args['name'],
                                                                interaction.guild_id, interaction.user.id)
    return interaction.build_response([hikari.impl.AutocompleteChoiceBuilder(_[0], _[0]) for _ in group_names])


async def handle_manage_autocomplete(interaction: hikari.AutocompleteInteraction, bot: hikari.RESTBot, args: dict[str, Any]):
    group_names = await database.fetch_owned_groups_autocomplete(args['name'],
                                                                 interaction.guild_id, interaction.user.id,
                                                                 await utils.check_if_admin(bot, interaction.user.id,
                                                                                            interaction.guild_id))
    return interaction.build_response([hikari.impl.AutocompleteChoiceBuilder(_[0], _[0]) for _ in group_names])


async def handle_call_autocomplete(interaction: hikari.AutocompleteInteraction, bot: hikari.RESTBot, args: dict[str, Any]):
    group_names = await database.fetch_callable_groups_autocomplete(args['name'],
                                                                 interaction.guild_id, interaction.user.id,
                                                                 await utils.check_if_admin(bot, interaction.user.id,
                                                                                            interaction.guild_id))
    return interaction.build_response([hikari.impl.AutocompleteChoiceBuilder(_[0], _[0]) for _ in group_names])


async def handle_invite_autocomplete(interaction: hikari.AutocompleteInteraction, bot: hikari.RESTBot, args: dict[str, Any]):
    group_names = await database.fetch_invitable_groups_autocomplete(args['name'],
                                                                 interaction.guild_id, interaction.user.id,
                                                                 await utils.check_if_admin(bot, interaction.user.id,
                                                                                            interaction.guild_id))
    return interaction.build_response([hikari.impl.AutocompleteChoiceBuilder(_[0], _[0]) for _ in group_names])


autocomplete_handlers: dict[str, Callable[[hikari.AutocompleteInteraction, hikari.RESTBot, dict[str, Any]], Coroutine[
    Any, Any, hikari.impl.InteractionAutocompleteBuilder]]] = {
    "group join": handle_join_autocomplete,
    "group leave": handle_leave_autocomplete,
    "group delete": handle_manage_autocomplete,
    "group call": handle_call_autocomplete,
    "group invite": handle_invite_autocomplete,
    "group set private": handle_manage_autocomplete,
    "group set member_calls": handle_manage_autocomplete,
    "group set external_calls": handle_manage_autocomplete,
    "group set max_members": handle_manage_autocomplete,
    "group set member_invites": handle_manage_autocomplete,
    "group set owner": handle_manage_autocomplete
}


def get(name: str):
    return autocomplete_handlers.get(name, None)
