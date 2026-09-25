# Description

Percentage of requests sampled by Leveled statistics monitoring. Higher sampling improves coverage but adds monitor messages; the monitor has no flow control to protect it from excessive sampling traffic.

# Constraints

- Use an integer percentage from 0 through 100 inclusive.

# Tags

feature: leveled
repository: leveled
module: leveled.schema
concept: diagnostics, storage

# Reviewed against

3.4.0: 1e4b29ec4ab748fd0ad0fa78279c71ae285781fe44b00951b89635a2a3a63d82
3.4.1: 489cadb059c655b5227580431b3a60a437277d5242fa07734296bffef74b1913
