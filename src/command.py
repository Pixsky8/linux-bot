import os
import discord
import subprocess
from config import config_command

is_docker = True

current_dir = "/data"
max_message = 2

async def on_command(message, client, config):
    markdown = "Markdown"
    reply = ""
    return_code = 0
    content = message.content[config.prefix_len:]
    print(message.author.name+ ": " + content)

    if content.startswith(config.prefix):
        (reply, markdown, return_code) = config_command(message, config, message.author)

    elif content.startswith("sudo"):
        if config.is_admin(message.author.id):
            command = command_arg("", content.split()[1:], "")
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            (out, err) = proc.communicate()
            return_code = proc.returncode
            reply = out.decode("utf-8")
        else:
            reply = config.strings["NOT_SUDOER"].format(message.author)
            return_code = 1

    elif content.startswith("cd"):
        if len(content) > 3:
            current_dir = content[3:]
        else:
            current_dir = "~/"
        os.chdir(current_dir)
        reply = "pwd: " + os.popen("pwd").read()

    elif content.startswith("ls"):
        args = content.split()[1:]
        if is_docker :
            command = command_arg("su quarantedeux -c \"ls -CF ", args, "\"")
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
            try:
                (out, err) = proc.communicate(timeout=40)
            except TimeoutExpired:
                proc.kill()
                (out, err) = proc.communicate()
            return_code = proc.returncode
        else:
            proc = subprocess.Popen(content, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            try:
                (out, err) = proc.communicate(timeout=40)
            except TimeoutExpired:
                proc.kill()
                (out, err) = proc.communicate()
            return_code = proc.returncode
        reply = out.decode("utf-8")


    await reply_command(message, reply, markdown, return_code)


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

async def reply_command(message, reply, markdown, return_code, instance=0):
    # reply to the user
    if return_code == 0:
        if reply:
            max_size = 1991 - len(markdown)
            if len(reply) < max_size:
                await message.channel.send("```" + markdown + "\n" + reply + "\n```")
            # split message
            else:
                i = 0
                while len(reply) > max_size:
                    if i >= max_message:
                        await message.channel.send("```diff\n- Message is too long (" + len(reply) + " chars left)```")
                        return
                    await message.channel.send("```" + markdown + "\n" + reply[:max_size] + "\n```")
                    reply = reply[max_size:]
                    i += 1
        else:
            await message.channel.send("```(Empty)\n```")

    else:
        to_send = "```diff\n"
        lines = reply.splitlines(True)
        for line in lines:
            to_send = to_send + "- " + line
        await message.channel.send(to_send + "\n```")
