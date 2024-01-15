`d1_tracer`: docker printing trace from `d2_server` 

    python3 tracer.py


`d2_server`: docker with opentelemetry, receipts trace from `d3 and d4` and forward to `d1_tracer`

    python3 server.py

`d3_random`:  docker host sending GET requests to `d2_server` with a random delay (between 0 and 4)

    python3 client_random.py

`d4_ddos`:  docker host sending GET requests to `d2_server` (ddos simulation)

    python3 client_ddos.py


To run all xterm : 

    xterm d1_tracer && xterm d2_server && xterm d3_random && xterm d4_ddos