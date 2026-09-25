# Description

Selects the statistical measures Folsom calculates for histogram and duration samples. The list is passed to Bear's statistics-subset function, allowing unused statistical calculations to be omitted.

# Datatype

List

# Constraints

- List of Bear statistic names: `arithmetic_mean`, `geometric_mean`, `harmonic_mean`, `histogram`, `kurtosis`, `n`, `max`, `median`, `min`, `skewness`, `standard_deviation`, `variance`, or `{percentile, Percentiles}`. Percentiles use Bear's integer encoding, for example `99` and `999` for 99% and 99.9%.

# Inferred default

`[arithmetic_mean, geometric_mean, harmonic_mean, histogram, kurtosis, n, max, median, min, {percentile, [50, 75, 95, 99, 999]}, skewness, standard_deviation, variance]`.

# Tags

feature: observability
repository: folsom
module: folsom_metrics, folsom_metrics_duration
concept: diagnostics

# Notes

This is the Erlang application environment key `enabled_metrics` in `folsom`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [folsom/src/folsom_metrics.erl](https://github.com/OpenRiak/folsom/blob/6b7343b67d19b0ac83de55cc2703fc8deefa52d7/src/folsom_metrics.erl#L191)
- [folsom/src/folsom_metrics_duration.erl](https://github.com/OpenRiak/folsom/blob/6b7343b67d19b0ac83de55cc2703fc8deefa52d7/src/folsom_metrics_duration.erl#L87)

Additional type/default evidence:

- [bear/src/bear.erl](https://github.com/OpenRiak/bear/blob/a73f9213af9cab63b9b955bf300554779b7f8e6a/src/bear.erl)
- [folsom/include/folsom.hrl](https://github.com/OpenRiak/folsom/blob/6b7343b67d19b0ac83de55cc2703fc8deefa52d7/include/folsom.hrl)

# Reviewed against

3.4.0: 7d12c7378c15c131a51b4a6ab66b6f6ff4b73ea721565348a7305a37d3be4631
3.4.1: 7d12c7378c15c131a51b4a6ab66b6f6ff4b73ea721565348a7305a37d3be4631
