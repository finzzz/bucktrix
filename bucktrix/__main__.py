#! /usr/bin/python3

import os
import sys
import asyncio
from nio import RoomMessageText
from bucktrix import config, conn, task, callback


VERSION = "0.1.4"

BUXTRIX_DIR = os.getenv("BUCKTRIX_DIR")
if not BUXTRIX_DIR:
    BUXTRIX_DIR = ".bucktrix/"


def main():
    if len(sys.argv) < 2:
        print("not enough args")
        quit(1)

    cfg = config.Config(BUXTRIX_DIR)
    cmd = sys.argv[1]
    if cmd == "init":
        cfg.init()
    elif cmd == "edit":
        cfg.edit()
    elif cmd == "logout":
        cfg.del_session()
    elif cmd == "clear":
        cfg.read_config()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(clear_cmd(cfg))
        loop.close()
        cfg.del_session()
    elif cmd == "serve":
        cfg.read_config()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(serve_cmd(cfg))
        loop.close()
    elif cmd == "send":
        if len(sys.argv) == 2:
            print("Not enough arguments")
            quit(1)

        cfg.read_config()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(send_cmd(cfg, sys.argv[2]))
        loop.close()
    elif cmd == "list":
        cfg.list()
    elif cmd == "add":
        cfg.add()
    elif cmd == "rm":
        cfg.rm()
    elif cmd == "version":
        print(f"Bucktrix version {VERSION}")
    else:
        print("Invalid command.")


async def send_cmd(config, message):
    client = await conn.login(config)
    await task.send(client, config.room_id, message)
    await client.close()


async def serve_cmd(config):
    client = await conn.login(config)
    cb = callback.Callbacks(client, config)
    client.add_event_callback(cb.process_message, RoomMessageText)
    await client.sync_forever(timeout=int(config.timeout))


async def clear_cmd(config):
    client = await conn.login(config)
    await client.logout(all_devices=True)
    await client.close()

if __name__ == "__main__":
    main()
