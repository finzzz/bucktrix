import subprocess
import shlex
import os
from . import task


class Callbacks(object):
    def __init__(self, client, config):
        self.client = client
        self.room_id = config.room_id
        self.master = config.master
        self.shell = config.shell
        self.trigger = config.trigger
        self.commands = config.commands
        self.hist = config.history_path

    async def process_message(self, room, event):
        if room.room_id != self.room_id:
            return  # if not same room

        if not (event.body).startswith(self.trigger):
            return  # if not trigger

        if not self.is_authorized(event.sender):
            return

        query = self.is_last_command(event.body)

        query = shlex.split(query)
        if len(query) < 1:
            return  # return on empty query

        if query[0] not in self.commands:
            return  # if command is specified in the config

        parsed_cmd = await self.parse_command(query)

        if parsed_cmd != "":
            await self.execute_command(parsed_cmd)

    async def parse_command(self, query):
        command = ""
        idx = 0

        for i in shlex.split(self.commands[query[0]]):
            tmp = i
            try:
                if i == "*":
                    command += " " + " ".join(query[idx:])
                    break
                elif i.startswith('$'):
                    tmp = query[int(i.lstrip('$'))]
            except IndexError:
                await task.send(
                    self.client,
                    self.room_id, "Not enough argument")
                command = ""
                break
            except ValueError:
                await task.send(
                    self.client,
                    self.room_id, f"Error parsing '{i}' : must be integer")
                command = ""
                break

            command += " " + tmp
            idx += 1

        return command

    async def execute_command(self, command):
        output = subprocess.run(
            [self.shell, "-c", command],
            capture_output=True,
        )

        stdout = (output.stdout).decode()
        stderr = (output.stderr).decode()

        if stdout != "":
            await task.send(self.client, self.room_id, stdout)

        if stderr != "":
            await task.send(self.client, self.room_id, stderr)

    def is_authorized(self, s) -> bool:
        master = self.master.split(",")
        if "*" not in master and s not in master:
            print(f"{s} is not authorized")
            return False

        return True

    def is_last_command(self, s) -> str:
        query = s.lstrip(self.trigger)  # strip trigger

        if not (os.path.exists(self.hist)
                and s == self.trigger*2):

            with open(self.hist, "w") as f:
                f.write(query)  # write to history

            return query

        with open(self.hist, "r") as f:
            return f.read()
