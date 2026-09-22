# Metadata

command: shell:riak admin leave
versions: 3.4.0, 3.4.1

# Summary

Leave the cluster using the legacy immediate command.

# Description

Prefer the staged cluster subcommands for planned topology changes.

# Arguments

# Options

## -f

datatype: flag (no value)
required: false
repeatable: false

### Description

Acknowledge use of the legacy immediate membership operation. Review staged cluster commands before choosing this path.

# Results

## reference-result-1

### Description

On a valid request, the ring metadata is updated or the membership operation starts. Monitor ring-status and transfers; the acknowledgment is not completion of handoff.

# Reviewed against

3.4.0: 12565d5935f38b205e04770cd9d2fc8ca78e9bfe9519e67a498a8c9cdd77afe2
3.4.1: 12565d5935f38b205e04770cd9d2fc8ca78e9bfe9519e67a498a8c9cdd77afe2
