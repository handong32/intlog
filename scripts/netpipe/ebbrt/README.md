## How to run parse trace logs from EbbRT-netpipe

`parse_ebbrt.c` parses an encoded binary from EbbRT-netpipe's server. To retrieve said binary, EbbRT-netpipe runs a separate TCP server which enables `socat` to communicate with it. For example `echo "get,0" | socat - TCP4:192.168.1.9:8889 > "ebbrt.bin"` where `192.168.1.9:8889` is where the EbbRT-netpipe TCP server is listening for commands.

After parsing the encoded binary, run `clean_netpipe_ebbrt.py` to post-process the trace log.
