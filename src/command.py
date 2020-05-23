import os
import discord
import subprocess

current_dir = "/"
is_docker = True

async def on_command(message, client):
    content = message.content[1:]
    os.system("echo \"" + message.author.name+ ": " + content + '\"')
    if content.startswith("cd"):
        if len(content) > 3:
            current_dir = content[3:]
        else:
            current_dir = "~/"
        os.chdir(current_dir)
        await message.channel.send("pwd: " + os.popen("pwd").read())

    else:
        if is_docker:
            proc = subprocess.Popen("su quarantedeux -c \"" + content + '\"', stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
        else:
            proc = subprocess.Popen(content, stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
        if err:
            await message.channel.send("Error: " + err.decode("utf-8"))
        await message.channel.send(out.decode("utf-8"))
