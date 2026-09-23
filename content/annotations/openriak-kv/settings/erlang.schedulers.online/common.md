# Description

Number of normal Erlang scheduler threads initially online. Used with `erlang.schedulers.total`; zero selects the runtime default and negative values subtract from its detected processor count.

# Tags

feature: erlang-runtime
repository: cuttlefish
module: erlang_vm.schema
concept: concurrency, runtime

# Reviewed against

3.4.0: 1029f7dba06835e8ea09f51a0177f734391171d8aadb7a6709278542978908a3
3.4.1: 1029f7dba06835e8ea09f51a0177f734391171d8aadb7a6709278542978908a3
