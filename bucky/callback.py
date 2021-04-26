import subprocess
import shlex
from . import task


class Callbacks(object):
    def __init__(self, client, config):
        self.client = client
        self.room_id = config.room_id
        self.master = config.master
        self.trigger = config.trigger
        self.commands = config.commands

    async def process_message(self, room, event):
        # return if different room
        if room.room_id != self.room_id:
            return

        # return if not start with trigger
        if not (event.body).startswith(self.trigger):
            return

        # return if not authorized master
        master = (self.master).split(",")
        if "*" not in master and event.sender not in master:
            print(master, event.sender)
            return

        # strip trigger, return on empty query
        query = (event.body).lstrip(self.trigger)
        query = shlex.split(query)
        if len(query) < 1:
            return

        # check if command is specified in the config
        if query[0] not in self.commands:
            await task.send(self.client, self.room_id, "Command not found")
            return

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

            command += " " + tmp
            idx += 1

        return command

    async def execute_command(self, command):
        output = subprocess.run(
            ["/bin/sh", "-c", command],
            capture_output=True)
        stdout = (output.stdout).decode()
        stderr = (output.stderr).decode()

        if stdout != "":
            await task.send(self.client, self.room_id, stdout)

        if stderr != "":
            await task.send(self.client, self.room_id, stderr)
