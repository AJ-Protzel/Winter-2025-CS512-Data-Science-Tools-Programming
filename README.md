# CS 512 — Data Science Tools & Programming

Graduate coursework for Oregon State University CS 512, Winter 2025. Nine weeks moving from Python fundamentals through SQL, visualization, and distributed processing with Spark.

The recurring thread is a personal-finance ETL project: raw bank and credit-card statement exports get imported, merged, cleaned, categorized, loaded into SQLite, and finally processed with PySpark. That pipeline grew into a standalone repository — [Transaction Pipeline](https://github.com/AJ-Protzel/Transaction-Pipeline).

> **Note on data.** The source statements were real personal financial records and have been removed from this repository. The pipeline code, schema, configs, and query results remain; the inputs do not. Nothing here runs end-to-end without supplying your own CSVs.

## Weeks

| Week | Topic |
|---|---|
| w1 | Python fundamentals and an OSEMN-framework report |
| w2 | SQL against the course database — ten query exercises with expected results |
| w3 | Data wrangling: the transaction import / merge / clean / categorize pipeline |
| w4 | Visualization with matplotlib (Anatomy of Matplotlib tutorial materials and exercises) |
| w5 | Midterm — SQLite schema design, table population, and analytical queries with charted results |
| w6 | BigQuery and working at larger scale |
| w7 | PySpark, part one — window functions over flight-distance data |
| w8 | PySpark, part two — continued Spark activities |
| w9 | Final project — the full pipeline plus a PySpark processing pass |

## Layout

```text
w1/ … w9/          weekly assignments, source, and written deliverables
Instructions.pdf   course instructions
```
