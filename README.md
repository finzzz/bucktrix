# Introduction
## What is Bucktrix
Bucktrix is a personal [matrix](https://github.com/matrix-org/synapse) chatbot that can send message or execute commands based on certain events.

## Why use Bucktrix?
- You want to eliminate the use of email as a tool of notifications.
- You want to run an app that only has CLI.
- You want to execute certain commands or scripts without SSH.

## Things to note
- Bucktrix should be installed in a machine where its privileges are being limited.
- Bucktrix responds to command from control user which is in the same **encrypted** room.
- It is also possible to send one-shot message using `./bucktrix send`.
- `trigger` are used to differentiate when/where bucktrix is being called.
- **Do not** use Bucktrix in a room where you cannot trust all participants.

# Getting started
The fastest way to install is via `pip`. For testing purposes, I have built debian based binary which is available in `dist` folder. Otherwise, you need to build it manually.

## Installation
### Requirements
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
make build
dist/bucktrix init    # generate config
dist/bucktrix add     # add command
```

## Folder structures
```
.
├── bucktrix (binary)
└── .bucktrix
    ├── config.ini
    ├── history.txt
    └── session/
```

## Command examples (manual edit config.ini)
```
[commands]
echo1 = echo hello world
echo2 = echo $3 $2 $1       # positional arguments
echo3 = echo *              # wildcard
echo4 = echo $2 $1 *        # combination of both
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

# Sample scripts
- [Systemd service](examples/bucktrix.service)
- [Bash script to send message](examples/send.sh)

# TODO
- Distributing
    - [ ] podman/docker build & image
    - [x] distribute to pypi
- Features
    - [x] run last command
    - [ ] logging