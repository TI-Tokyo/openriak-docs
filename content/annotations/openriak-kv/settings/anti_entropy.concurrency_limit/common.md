# Description

Maximum number of legacy AAE exchanges or tree builds allowed concurrently. Lower the limit when repair work competes with client traffic; raising it can speed reconciliation if CPU and disk capacity are available.

# Tags

feature: legacy-aae
repository: riak_kv
module: riak_kv_entropy_manager
concept: concurrency, replica-repair

# Reviewed against

3.4.0: 1071a5cd1b827083474c77cd189198c777a7527f611ddeb63597ba9fd7cc0d89
3.4.1: 70c6c0d84e073cc31a5dd0faf8aba0416d87790cdfec015fe889ed24a600e4e7
