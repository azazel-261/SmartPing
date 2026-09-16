# SmartPing! - a discord bot to call your friends for you

## How it works:
- Users are organized into groups, that can either be private or open for anyone to join!
- Upon a group call, the required info is retrieved from the bot database and a message is sent into the chat, mentioning all the required users
- Unless you're an admin, calls are on a 5-minute cooldown to prevent spamming by users
## Features:
- Joining / Leaving groups
- Calling groups
- - With a custom message!
- Private groups and invites
- Manageable by admins! Anyone with an admin permission is granted access to all groups
## Where to try it:
Add the bot to your server here:\
https://discord.com/oauth2/authorize?client_id=1542944613961044138
## Usage instructions:
After adding the bot to your server via the link above, you can start using it immediately!

### Creation
Start by creating a group by running
`/group create example_group_name`\
Take note, the group name should be unique to the server, no two groups with the same name should exist within a server

### Private groups
An optional `private` parameter during creation allows you to set your group to a mode where users can only get in via an invitation
from the owner/another member

You can alter that later by running `/group set private example_group_name`

### Joining and inviting
If you want to join an existing group, run `/group join example_group_name`. That only works for public groups though! 
If you want to join a private group, persuade the owner or another member of said group to invite you via `/group invite example_group_name @example_user`.
Once done, a dialog will appear for you to accept or reject the invitation, pick wisely!

### Leaving and deleting
You can leave groups by running `/group leave example_group_name`, `/group leaveall` to leave all call groups within the server,
or `/group delete example_group_name` to get rid of the group altogether! The last one, however, is only available to the group owner and server admins.
If you're serious about deleting the call group, don't forget to click "yes" in the dialog that comes up

### Calling the group
Once everyone's in, use `/group call example_group_name` to mention all the group members! While a normal call simply attracts attention,
you can provide an optional `msg` parameter to bring along a small message for the recipients to see, up to 50 characters long.
Note that non-admin members can only call a group once every 5 minutes to prevent spamming

### Parameters
Boring to explain but necessary! The `/group set` command subgroup allows you to set different group parameters, list of which can be found below:
- `max_members [integer]` - the maximum amount of users in the call group. Set it to zero to disable the limit altogether, which it defaults to
- `private [bool]` - as mentioned earlier, sets a group to only accept new users via invites, defaults to off
- `external_calls [bool]` - allows non-member users to alert group members via calls, defaults to off
- `member_calls [bool]` - allows member users to alert other members via calls, defaults to on. If turned off, only admins and group owner can call
- `member_invites [bool]` - allows member users to invite other users, defaults to on. If off, only admins and group owner can invite others
- `owher [user]` - transfers the ownership of the group to another user. Please don't forget to confirm your decision in the dialog that shows up!

All of the `set` commands can be used by group owners upon their own groups or by admins onto any group within the server

## Self-hosting:

Four things will be needed for you to self-host this bot:
- A machine capable of running Python scripts
- A PostgreSQL database. Schema for the database can be found in the file `schema.sql`. Just execute the sql file on your database and you should be good to go
- A discord application, that can be created [here](https://discord.com/developers/applications)
- A static address to use for Discord Interaction Endpoint. If you plan on running the bol locally instead of a server, use [ngrok](https://ngrok.com/)

Note: Procfile is only necessary if you're going to host the bot on a server like Heroku/Render. You may delete it otherwise

Start by running\
`git clone https://github.com/azazel-261/SmartPing` \
` cd ./SmartPing`

To install all the dependencies, run\
`pip install -r requirements.txt`

Please make sure to run `python set_commands.py` (or `python3` for Linux/MacOS) to ensure discord knows what commands your bot can execute. This is required regardless of whether you are planning on hosting the bot locally or on a server

### Hosting on a local machine

Create a `.env` file and populate it with the following info:
- `PUBLIC_KEY` - can be found in your discord app's dashboard under "general information"
- `DISCORD_TOKEN` - in the same dashboard, under "Bot > Token > Reset Token"
- `DATABASE_HOST` - your database's ip/public address
- `DATABASE_USER` - self-explanatory, username under which your bot will log into the database
- `DATABASE_PASSWORD` - the password to use for the database authentication
- `DATABASE_PORT` - the port to use for the database connection

Once done, you can start the bot by running `python -O main.py` (or `python3`)

### Hosting on a remote server

The process is mostly identical, simply push the repository onto the server and provide the secret values in the server dashboard, as shown in setting up the `.env` file in local machine hosting

Finally, go to your bot's dashboard and under Interaction Endpoint URL paste in your ngrok/server url. 
You can then proceed to App Dashboard > Installation to get a link and invite the bot to your server for testing!


## Resources used:
- [Hikari](https://github.com/hikari-py/hikari) Python library to handle the bot
- [Aiopg](https://github.com/aio-libs/aiopg) library to access and manage the database
- - Respective documentations for the above-mentioned libraries
- - Dependencies for the above-mentioned libraries
- Stack Overflow and other online community-based forums
- Other publicly available documentation sources for python/PostgreSQL
- Multiple snacks and cups of tea consumed in the process of making code :3
### TO MY KNOWLEDGE, NO CODE IN THE PROJECT WAS CREATED BY GENERATIVE AI