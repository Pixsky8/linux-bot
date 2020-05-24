import json

def config_command(message, config, author):
    command = message.content[config.prefix_len*2:]
    if command.startswith("prefix"):
        if len(command) > 6:
            args = command.split()[1:]
            config.change_prefix(args[0])
            return ("> OK", "css", 0) # green text
        else:
            return (config.strings["HELP_PREFIX"].format(config), "", 1)

    if command.startswith("addadmin"):
        args = command.split()[1:]
        if len(args) > 0:
            if config.is_admin(author.id):
                for member in message.mentions:
                    config.add_admin(member.id)
                return ("> OK", "css", 0)
            else:
                return (config.strings["NOT_SUDOER"].format(message.author), "", 1)
        else:
            return (config.string["HELP_ADDADMIN"].format(config), "", 0)

    else:
        return ("\"\n" + config.strings["HELP_MSG"].format(config) + "\n\"", "bash", 0) # dark cyan text



class Config:

    token = ""
    prefix = ""
    prefix_len = 0
    strings = None
    admins = None

    def __init__(self):
        fsett = open("config/settings.json")
        data = json.load(fsett)
        self.token = data["token"]
        self.prefix = data["prefix"]
        self.prefix_len = len(self.prefix)
        if "admins" in data:
            self.admins = data["admins"]
        fsett.close()

        fstr = open("config/strings.json")
        self.strings = json.load(fstr)
        fstr.close()


    def save(self):
        data = {
            "token": self.token,
            "prefix": self.prefix,
            "admin": self.admins,
        }

        json_data = json.dumps(data, indent=2)
        f = open("/app/config/settings.json", "w+")
        f.write(json_data)
        f.close()


    def change_prefix(self, prefix):
        self.prefix = prefix
        self.prefix_len = len(self.prefix)
        self.save()


    def add_admin(self, user_id):
        if not user_id in self.admins:
            self.admins.append(user_id)
            self.save()

    def is_admin(self, user_id):
        return user_id in self.admins
