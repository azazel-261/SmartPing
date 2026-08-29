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