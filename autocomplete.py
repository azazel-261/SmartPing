from typing import Callable, Coroutine, Any
import hikari
import data

autocomplete_handlers: dict[str, Callable[[hikari.AutocompleteInteraction, hikari.RESTBot], Coroutine[Any, Any, hikari.impl.InteractionAutocompleteBuilder]]] = {

}

def get(name: str):
    return autocomplete_handlers.get(name, None)