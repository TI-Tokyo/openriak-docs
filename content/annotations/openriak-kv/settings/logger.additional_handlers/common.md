# Description

Extra log handlers to enable, such as `crash`, `error`, `report`, `backend`, `background` or `json`. These copy matching events unless `logger.default_filters` also removes them from the default log. `none` selects no extra handlers.

# Tags

feature: observability
repository: riak
module: riak.schema
concept: diagnostics

# Reviewed against

3.4.0: 373fc91f6cdff7c010129610a4b762cfbca6f1eab66e858730575addbed2ba8d
3.4.1: 373fc91f6cdff7c010129610a4b762cfbca6f1eab66e858730575addbed2ba8d
