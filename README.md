# How to run?

-   `git clone https://github.com/CantBeSubh/marker-serve.git`
-   `cd marker-serve`
-   `make dev-run`

## TODOs

-   Fix config


## Exmpimental changes

1. Worker set to 1
- Hard setting these to 1 reason: hypercorn uses uvloop/trio/asyncio, which will give this error `daemonic processes are not allowed to have children`

- FYI: saw a minor loss of in performance - about 20s increase in processing time