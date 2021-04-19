import os
import shutil
import configparser


class Config:
    def __init__(self, file, store_path):
        self.file = file
        self.store_path = store_path

        # defaults
        self.server = "matrix.org"
        self.username = "bucky"
        self.password = "bucky"
        self.room_id = "!buckyroom:matrix.org"
        self.master = "*"
        self.shell = "/bin/sh"
        self.trigger = "!"
        self.timeout = "30"
        self.commands = {}

    def read_config(self):
        config = configparser.ConfigParser()
        config.read(self.file)

        self.server = config['connection']['server']
        self.username = config['connection']['username']
        self.password = config['connection']['password']
        self.room_id = config['connection']['room_id']

        self.master = config['bot']['master']
        self.shell = config['bot']['shell']
        self.trigger = config['bot']['trigger']
        self.timeout = config['bot']['timeout']

        self.commands = config['commands']

    def init(self):
        DIR = os.path.dirname(self.file)

        if not os.path.exists(DIR):
            os.mkdir(DIR)

        # store_path should exists
        if not os.path.exists(self.store_path):
            os.mkdir(self.store_path)

        cfg_is_exist = os.path.exists(self.file)
        overwrite = ""
        if cfg_is_exist:
            overwrite = input("Config file already exists, overwrite [y/N]? ")

        if cfg_is_exist and overwrite != "y":
            quit(1)

        # write config
        config = configparser.ConfigParser()
        self.write(config)

    def edit(self):
        if not os.path.exists(self.file):
            print("Config file doesn't exist")
            quit(1)

        # read config
        config = configparser.ConfigParser()
        config.read(self.file)

        # connection
        self.server = config['connection']['server']
        self.username = config['connection']['username']
        self.password = config['connection']['password']
        self.room_id = config['connection']['room_id']

        # bot
        self.master = config['bot']['master']
        self.shell = config['bot']['shell']
        self.trigger = config['bot']['trigger']
        self.timeout = config['bot']['timeout']

        self.write(config)

    def write(self, config):
        config['connection'] = {
            'server': input(f"Server [{self.server}]: ") or self.server,
            'username':
                input(f"Username [{self.username}]: ") or self.username,
            'password':
                input(f"Password [{self.password}]: ") or self.password,
            'room_id': input(f"Room ID [{self.room_id}]: ") or self.room_id
        }

        config['bot'] = {
            'master': input(f"Master [{self.master}]: ") or self.master,
            'shell': input(f"Shell [{self.shell}]: ") or self.shell,
            'trigger': input(f"Trigger [{self.trigger}]: ") or self.trigger,
            'timeout': input(f"Timeout [{self.timeout}]: ") or self.timeout
        }

        if 'session' not in config:
            config['session'] = {}

        if 'commands' not in config:
            config['commands'] = {}

        with open(self.file, 'w') as f:
            config.write(f)

    def list(self):
        config = configparser.ConfigParser()
        config.read(self.file)

        for cmd in config['commands']:
            print(f"{cmd}\t: {config['commands'][cmd]}")

    def add(self):
        config = configparser.ConfigParser()
        config.read(self.file)

        cmd_name = input("Name: ")
        cmd_exec = input("Exec: ")

        if cmd_name == "" or cmd_exec == "":
            print("Entry cannot be blank")
            quit(1)

        if not config['commands'].get(cmd_name):
            config['commands'].update({cmd_name: cmd_exec})
        else:
            print(f"Command {cmd_name} already exists")
            quit(1)

        with open(self.file, 'w') as f:
            config.write(f)

    def rm(self):
        config = configparser.ConfigParser()
        config.read(self.file)

        cmd_name = input("Name: ")

        if cmd_name == "":
            print("Entry cannot be blank")
            quit(1)

        if config['commands'].get(cmd_name):
            del config['commands'][cmd_name]
        else:
            print(f"Command {cmd_name} doesn't exist")
            quit(1)

        with open(self.file, 'w') as f:
            config.write(f)

    def get_session(self):
        config = configparser.ConfigParser()
        config.read(self.file)

        # session
        access_token = ''
        device_id = ''
        if 'session' in config and 'access_token' in config['session']:
            access_token = config['session']['access_token']
            device_id = config['session']['device_id']

        return access_token, device_id

    def set_session(self, access_token, device_id):
        config = configparser.ConfigParser()
        config.read(self.file)

        config['session'] = {
            'access_token': access_token,
            'device_id': device_id
        }

        with open(self.file, 'w') as f:
            config.write(f)

    def del_session(self):
        config = configparser.ConfigParser()
        config.read(self.file)

        config['session'] = {}

        with open(self.file, 'w') as f:
            config.write(f)

        shutil.rmtree(self.store_path)
        os.mkdir(self.store_path)
