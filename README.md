# TODO
- [x] create/edit config
    - bucky init
    - bucky edit
- [x] 2 modes
    - bucky serve
    - bucky send "hello world"
- [x] command management
    - bucky list
    - bucky add
    - bucky rm
- [x] session
    - bucky logout (delete current session)
    - bucky clear (delete all sessions -> logout)
- [x] bucky serve parse `commands`
    - ls = /usr/bin/ls $1               => only one argument allowed
    - ls = /usr/bin/ls *                => wildcard
    - grep = grep -i $1 -v $3 $2        => positional
    - ls = /usr/bin/ls $2 $1 *          => wildcard, positional
    - handle arguments containing space => put inside quote
- [ ] podman/docker build & image
- [x] Add `only listen to` feature 
- [ ] add logging feature
- [x] systemd example

# Inner works
\#1. commands
```
[commands]
echo = echo a b c
echo2 = echo $3 $2 $1
echo3 = echo *
echo4 = echo $2 $1 *
```
\#2. folder structs
```
.
├── bucky (binary)
└── .bucky
    ├── config.ini
    ├── sessions
    └── logs
```

# Requirements
- poetry
- libolm3 libolm-dev (for E2EE)

# Manual build
```
poetry install
make build
```

# Intended Uses
- Bucky is installed in a machine where its privileges are being limited.
- Control user should be in the same encrypted room with bucky.
- Bucky responds to command from matrix client as a service.
- It is also possible to send one-shot message.

# Things to Note
- Any user with the same room as bucky can execute commands (for now).
- `trigger` should be used to differentiate when/where Bucky is being called.

# Running Bucky
```
./bucky init                # generate config file
./bucky edit                # edit config file
./bucky logout              # logout current session
./bucky clear               # clear all sessions
./bucky send "Hello world"  # one-shot message
./bucky serve               # listen mode
./bucky add                 # add command
./bucky list                # list command
./bucky rm                  # delete command
```