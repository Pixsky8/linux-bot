import os
import discord
import subprocess

current_dir = "/data"
is_docker = True

async def on_command(message, client):
    markdown = "Markdown"
    reply = ""
    return_code = 0
    content = message.content[1:]
    os.system("echo \"" + message.author.name+ ": " + content + '\"')

    if content.startswith("cd"):
        if len(content) > 3:
            current_dir = content[3:]
        else:
            current_dir = "~/"
        os.chdir(current_dir)
        reply = "pwd: " + os.popen("pwd").read()

    elif content.startswith("ls"):
        args = content.split()[1:]
        if is_docker :
            command = command_arg("su quarantedeux -c \"ls -CF", args, "\"")
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            (out, err) = proc.communicate()
            return_code = proc.returncode
        else:
            command = command_arg("ls -CF ", args)
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            (out, err) = proc.communicate()
            return_code = proc.returncode
        reply = out.decode("utf-8")

    else:
        if is_docker:
            proc = subprocess.Popen("su quarantedeux -c \"" + content + '\"', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            (out, err) = proc.communicate()
            return_code = proc.returncode
        else:
            proc = subprocess.Popen(content, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            (out, err) = proc.communicate()
            return_code = proc.returncode
        reply = out.decode("utf-8")

    reply_command(message, reply, markdown, return_code)


def command_arg(command, args, suffix = None):
    """
    command is a string
    args is a list of strings
    sufix is a string
    return: string
    """
    res = command
    for arg in args:
        res = res + arg
    if suffix:
        res = res + suffix
    return res

def reply_command(message, reply, markdown, return_code):

    # reply to the user
    if return_code == 0:
        if reply:
            await message.channel.send("```" + markdown + "\n" + reply + "\n```")
        else:
            await message.channel.send("```(Empty)\n```")
    else:
        to_send = "```diff\n"
        lines = reply.splitlines(True)
        for line in lines:
            to_send = to_send + "- " + line
        await message.channel.send(to_send + "\n```")
