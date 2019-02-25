#!/bin/tcsh

set socket = /tmp/indigo-atlas-socket

if ( ! -e $socket ) then
# -S: use/create socket
# -f: background
# -M: master mode (for tunnel)
# -N: do not execute remote command
	ssh -S $socket -fMN indigo@10.1.64.68
endif

if ( ! -e $socket ) then
	echo "atlas: unable to create ssh socket '$socket'"
	exit 1
endif

# -S: use socket
# -Y: enable trusted X11 forwarding
ssh -S $socket -Y indigo@10.1.64.68

