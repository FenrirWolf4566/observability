`d1_tracer`: docker printing trace from `d2_server` 

    python3 tracer.py


`d2_server`: docker with opentelemetry, receipts trace from `h1_sender` and forward to `d1_tracer`

    python3 servWeb.py

`h1_sender`:  simple host sending GET requests to `d2_server`

    python3 servAsk.py