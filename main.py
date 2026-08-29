import os
import hikari
import commands
import data

token = os.getenv("DISCORD_TOKEN")

if not token:
    exit(-1)

bot = hikari.GatewayBot(token, intents=hikari.Intents.MESSAGE_CONTENT | hikari.Intents.GUILD_MESSAGES)

# Guaranteed to receive a command that starts with "ping! " as the prefix
async def handle_command(event: hikari.GuildMessageCreateEvent):
    if not event.message.content:
        return
    command_text = event.message.content.removeprefix("ping! ")
    w = command_text.find(" ")
    command_name = command_text[:w] if w >= 0 else command_text
    command = commands.get(command_name)
    if command:
        await command(command_text.removeprefix(command_name).removeprefix(" "), event, bot)

@bot.listen()
async def on_join(event: hikari.GuildJoinEvent):
    if event.guild.system_channel_id:
        await bot.rest.create_message(event.guild.system_channel_id, data.join_message)

@bot.listen()
async def on_message(event: hikari.GuildMessageCreateEvent):
    if event.author.is_bot:
        return

    if not event.message.content:
        return

    if event.message.content.startswith("ping! "):
        await handle_command(event)

if __name__ == "__main__":
    bot.run()
