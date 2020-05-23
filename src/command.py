import os
import discord
import subprocess

current_dir = "/"
is_docker = True

async def on_command(message, client):
    content = message.content[1:]
    os.system("echo " + message.author.name+ ": " + content)
    if content.startswith("cd"):
        if len(content) > 3:
            current_dir = content[3:]
        else:
            current_dir = "~/"
        os.chdir(current_dir)
        await message.channel.send("pwd: " + os.popen("pwd").read())
    else:
        if is_docker:
            out = os.popen("su quarantedeux -c \"" + content + '\"').read()
        else:
            out = os.popen(content).read()
        await message.channel.send(out)
