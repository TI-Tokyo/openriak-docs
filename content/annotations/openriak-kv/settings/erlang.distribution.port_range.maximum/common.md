# Description

Upper port bound for distributed Erlang listeners. Set it together with `erlang.distribution.port_range.minimum` when restricting firewall rules; it does not cover the separate handoff or client-service ports.

# Tags

feature: erlang-runtime
repository: cuttlefish
module: erlang_vm.schema
concept: runtime

# Reviewed against

3.4.0: 077fe9a95d3bacd18440939d23ff8924d9483da84aae3621e8af0e94680e05f2
3.4.1: 077fe9a95d3bacd18440939d23ff8924d9483da84aae3621e8af0e94680e05f2
