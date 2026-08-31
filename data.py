join_message = \
"""\
Hello! type \"ping! help\" to receive usage instructions\
"""

help_message = \
"""\
# Command list:

`ping! help` - get help

`ping! join [name]` - join group

`ping! invite [name] [user]` - invite user to a group that has a "private" attribute

`ping! leave [name]` - leave group

`ping! leaveall` - removes caller from all groups they are in in a given server

`ping! call [name] [msg]` - mentions all users in a group with an optional message, max length 50 characters

`ping! create [name]` - creates a group named "name". NAME CANNOT CONTAIN SPACES

`ping! delete [name]` - deletes a group. Can only be called by group creator or a user with admin permissions

`ping! setattr [name] [attr] [value]` - edit group settings. Can only be called by group creator or a user with admin permissions. Use "ping! help attr" to see the list of attributes\
"""

attribute_help_message = \
"""\
Attribute list\
"""

error_codes = {
    0 : "Operation successful",
    1 : "UniqueViolation: group with this name already exists",
    2 : "UniqueViolation: user already present in the group",
    3 : "Query Failed: Group not found or is private",
    4 : "Insert Failed: Group reached it's max capacity"
}

def get_error_code(code: int):
    return error_codes.get(code, "Unknown error")