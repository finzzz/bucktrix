# Introduction
![](bucktrix.svg)

## What is Bucktrix
Bucktrix is a personal [matrix](https://github.com/matrix-org/synapse) chatbot that can send message or execute commands based on certain events.

## Why use Bucktrix?
- You want to eliminate the use of email as a tool of notifications.
- You want to run an app that only has CLI.
- You want to execute certain commands or scripts without SSH.

## Things to note
- Bucktrix should be installed in a machine where its privileges are being limited.
- Bucktrix responds to command from control user which is in the same **encrypted** room.
- It is also possible to send one-shot message.
- `trigger` are used to differentiate when/where bucktrix is being called.
- **Do not** use Bucktrix in a room where you cannot trust all participants.

# Installation
## Requirements
- libolm3
- libolm-dev (must be version 3.x)
- poetry (manual build only)

## Via PyPI
```bash
pip3 install bucktrix

export BUXTRIX_DIR="/home/debian/.bucktrix" # must be absolute path, by default ./.bucktrix
python3 -m bucktrix init
python3 -m bucktrix add
```

## Manual Build
```bash
poetry install
poetry run pip install pyinstaller
make build

dist/bucktrix init    # generate config
dist/bucktrix add     # add command
```

## Command examples (manual edit config.ini)
```
[commands]
echo1 = echo hello world
echo2 = echo #3 #2 #1       # positional arguments
echo3 = echo *              # wildcard
echo4 = echo #2 #1 *        # combination of both
```

## Available commands
```
init                # generate config file
edit                # edit config file
logout              # logout current session
clear               # clear all sessions
send "Hello world"  # send message
serve               # listen mode
add                 # add command
list                # list commands
rm                  # delete command
version             # show version
```

# Upgrading
## 0.14 to 0.15
Add `arg = #` to config.ini, like so:
```
[bot]
master = *
shell = /bin/sh
arg = #
trigger = !
timeout = 30
```

# Examples
- [Systemd service](examples/bucktrix.service)
- [Script to send message](examples/send.sh)

# Useful scripts
Visit [script folder](https://github.com/finzzz/bucktrix/tree/master/scripts)

# TODO
- Distributing
    - [ ] podman/docker build & image
    - [x] distribute to pypi
- Features
    - [x] run last command
    - [ ] logging
