# Metadata

command: shell:riak admin bucket-type update
versions: 3.4.0, 3.4.1

# Summary

Change properties of an existing bucket type.

# Description

Supply only the properties you intend to change inside the props object. Type validation can reject incompatible changes.

# Arguments

## type

datatype: bucket type name
required: true
repeatable: false

### Description

Bucket type name, for example `cli_reference_type`. Creation and activation are separate steps.

## properties

datatype: JSON object
required: true
repeatable: false

### Description

JSON object containing a `props` object. Quote the whole JSON value in the shell, for example `'{"props":{"allow_mult":true}}'`.

# Results

## outcome

### Description

On success, subsequent bucket-type status output reflects the changed properties. The example uses the bundled release launcher to preserve the JSON argument and verifies the updated property.

# Reviewed against

3.4.0: 4b8a89ccc48f0347ea3f94fa8b77a87e9f6158ae8d96ab05585cb05b3b925aab
3.4.1: 4b8a89ccc48f0347ea3f94fa8b77a87e9f6158ae8d96ab05585cb05b3b925aab
