# Introduction
## What is bucky
Bucky is a personal [matrix](https://github.com/matrix-org/synapse) chatbot that can send message or execute commands based on certain events.

## Why use bucky?
- You want to eliminate the use of email as a tool of notifications.
- You want to run an app that only has CLI.
- You want to execute certain commands or scripts without SSH.

## Things to note
- Bucky should be installed in a machine where its privileges are being limited.
- Bucky responds to command from control user which is in the same **encrypted** room.
- It is also possible to send one-shot message using `./bucky send`.
- `trigger` are used to differentiate when/where Bucky is being called.
- **Do not** use bucky in a room where you cannot trust all participants.

# Getting started
For testing purposes, I have built debian based binary which is available in `dist` folder. Otherwise, you need to build it manually.

## Installation
### Requirements
- poetry
- libolm3
- libolm-dev (must be version 3.x)

### Build
```
poetry install
make build
```

## Next steps
```bash
# follow the guided setup
./bucky init    # generate config
./bucky add     # add command
```

## Folder structures
```
.
├── bucky (binary)
└── .bucky
    ├── config.ini
    └── session
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
./bucky init                # generate config file
./bucky edit                # edit config file
./bucky logout              # logout current session
./bucky clear               # clear all sessions
./bucky send "Hello world"  # send message
./bucky serve               # listen mode
./bucky add                 # add command
./bucky list                # list commands
./bucky rm                  # delete command
./bucky version             # show version
```

# Sample scripts
- Systemd service : check out `examples/bucky.service`
- Bash script to send message : check out `examples/send.sh`

# TODO
- Distributing
    - [ ] podman/docker build & image
    - [ ] distribute to pypi
- Features
    - [ ] logging