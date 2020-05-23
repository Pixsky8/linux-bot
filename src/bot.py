import discord
import asyncio
import config
import command
import os
from subprocess import Popen, PIPE


if command.is_docker:
    os.system("echo \"Bot is starting...\"")
else:
    print("Bot is starting...")


client = discord.Client()
config = config.Config()

# allow users to write to /data
if command.is_docker:
    os.system("chmod -R a+rwxs /data/")
    os.chdir("/data")

@client.event
async def on_ready():
    if command.is_docker:
        os.system("echo \"We have logged in as {0.user}\"".format(client))
    else:
        print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author != client.user:
        if message.content.startswith(config.prefix):
            await command.on_command(message, client, config)

client.run(config.token)
