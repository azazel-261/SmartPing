from typing import Callable, Coroutine, Any
import hikari
import database
import utils

async def handle_join_autocomplete(interaction: hikari.AutocompleteInteraction, bot: hikari.RESTBot):
    group_names = await database.fetch_joinable_groups_autocomplete(interaction.options[0].options[0].value, interaction.guild_id, interaction.user.id, await utils.check_if_admin(bot, interaction.user.id, interaction.guild_id))
    return interaction.build_response([hikari.impl.AutocompleteChoiceBuilder(_[0], _[0]) for _ in group_names])

autocomplete_handlers: dict[str, Callable[[hikari.AutocompleteInteraction, hikari.RESTBot], Coroutine[Any, Any, hikari.impl.InteractionAutocompleteBuilder]]] = {
    "group join" : handle_join_autocomplete
}

def get(name: str):
    return autocomplete_handlers.get(name, None)