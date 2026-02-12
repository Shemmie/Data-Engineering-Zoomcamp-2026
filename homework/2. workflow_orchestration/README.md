# Module 2 Homework: Workflow Orchestration - Solutions

## Overview

This homework covers workflow orchestration using Kestra, processing NYC Yellow and Green Taxi data for years 2019-2021.

---

## Question 1: Uncompressed File Size (Yellow Taxi, Dec 2020)

**Question:** Within the execution for `Yellow` Taxi data for the year `2020` and month `12`: what is the uncompressed file size (i.e. the output file `yellow_tripdata_2020-12.csv` of the `extract` task)?

**How to find:**
1. Run the flow `05_postgres_taxi_scheduled.yaml` with inputs: taxi=yellow, year=2020, month=12
2. After execution, check the Outputs tab of the `extract` task
3. Look at the file size for `yellow_tripdata_2020-12.csv`

**Answer:** `128.3 MiB`

---

## Question 2: Rendered Variable Value

**Question:** What is the rendered value of the variable `file` when the inputs `taxi` is set to `green`, `year` is set to `2020`, and `month` is set to `04` during execution?

**Explanation:**
The variable is defined as:
```yaml
file: "{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv"
```

When rendered with taxi=green, year=2020, month=04:
- `{{inputs.taxi}}` → `green`
- `{{inputs.year}}` → `2020`
- `{{inputs.month}}` → `04`

**Answer:** `green_tripdata_2020-04.csv`

---

## Question 3: Yellow Taxi Row Count (Year 2020)

**Question:** How many rows are there for the `Yellow` Taxi data for all CSV files in the year 2020?

**SQL Query (after loading all 2020 data to Postgres):**
```sql
SELECT COUNT(*) 
FROM public.yellow_tripdata
WHERE filename LIKE 'yellow_tripdata_2020%';
```

**Answer:** `24,648,499`

---

## Question 4: Green Taxi Row Count (Year 2020)

**Question:** How many rows are there for the `Green` Taxi data for all CSV files in the year 2020?

**SQL Query (after loading all 2020 data to Postgres):**
```sql
SELECT COUNT(*) 
FROM public.green_tripdata
WHERE filename LIKE 'green_tripdata_2020%';
```

**Answer:** `1,734,051`

---

## Question 5: Yellow Taxi Row Count (March 2021)

**Question:** How many rows are there for the `Yellow` Taxi data for the March 2021 CSV file?

**SQL Query:**
```sql
SELECT COUNT(*) 
FROM public.yellow_tripdata
WHERE filename = 'yellow_tripdata_2021-03.csv';
```

**Answer:** `1,925,152`

---

## Question 6: Timezone Configuration in Schedule Trigger

**Question:** How would you configure the timezone to New York in a Schedule trigger?

**Explanation:**
In Kestra, the Schedule trigger uses the IANA timezone database format. For New York, you would add a `timezone` property with the value `America/New_York`.

```yaml
triggers:
  - id: daily_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 9 * * *"
    timezone: America/New_York
```

**Answer:** `Add a timezone property set to America/New_York in the Schedule trigger configuration`

---

## Summary of Answers

| Question | Answer |
|----------|--------|
| Q1 | 128.3 MiB |
| Q2 | green_tripdata_2020-04.csv |
| Q3 | 24,648,499 |
| Q4 | 1,734,051 |
| Q5 | 1,925,152 |
| Q6 | Add a `timezone` property set to `America/New_York` in the `Schedule` trigger configuration |

---

## Assignment: Extend Data for 2021

The homework assignment requires extending the existing flows to include data for 2021.

### Option 1: Using Backfill
1. Navigate to the scheduled flow `05_gcp_taxi_scheduled.yaml` in Kestra UI
2. Use the backfill functionality
3. Select date range: `2021-01-01` to `2021-07-31`
4. Run for both `yellow` and `green` taxi data

### Option 2: Manual Execution
Run the flow manually for each month (January to July 2021) for both taxi types.

---

## Files Included

- `README.md` - This solutions file
- `docker-compose.yaml` - Docker Compose configuration for Kestra and Postgres
- `homework.md` - Original homework questions (reference)
