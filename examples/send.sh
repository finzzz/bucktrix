#! /bin/bash

# place in the same directory as the binary
# then run /path/to/send.sh
(cd "$(dirname $0)" && ./bucktrix send "Test")