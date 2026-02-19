# Module 4 Homework: Analytics Engineering with dbt - Solutions

## Overview

This homework covers analytics engineering with dbt, working with NYC Yellow, Green, and FHV taxi data for 2019-2020.

## Setup

1. Set up your dbt project following the [setup guide](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/04-analytics-engineering/setup/)
2. Load the Green and Yellow taxi data for 2019-2020 into your warehouse
3. Run `dbt build --target prod` to create all models and run tests

---

## Question 1: dbt Lineage and Execution

**Question:** Given a dbt project with the following structure:

```
models/
├── staging/
│   ├── stg_green_tripdata.sql
│   └── stg_yellow_tripdata.sql
└── intermediate/
    └── int_trips_unioned.sql (depends on stg_green_tripdata & stg_yellow_tripdata)
```

If you run `dbt run --select int_trips_unioned`, what models will be built?

**Answer:** `int_trips_unioned only`

**Explanation:** The `--select` flag without `+` prefix only runs the specified model. To include upstream dependencies, you'd use `dbt run --select +int_trips_unioned`.

---

## Question 2: dbt Tests

**Question:** You've configured a generic test with `accepted_values: [1, 2, 3, 4, 5]` on `payment_type`. A new value `6` appears in source data. What happens when you run `dbt test --select fct_trips`?

**Answer:** `dbt will fail the test, returning a non-zero exit code`

**Explanation:** dbt tests run against the current data. Since `6` is not in the accepted values, the test will fail.

---

## Question 3: Counting Records in `fct_monthly_zone_revenue`

```sql
SELECT COUNT(*) FROM `ny_taxi.fct_monthly_zone_revenue`;
```

**Answer:** `12,184`

---

## Question 4: Best Performing Zone for Green Taxis (2020)

```sql
SELECT pickup_zone, SUM(revenue_monthly_total_amount) AS total_revenue
FROM `ny_taxi.fct_monthly_zone_revenue`
WHERE service_type = 'Green'
  AND EXTRACT(YEAR FROM revenue_month) = 2020
GROUP BY pickup_zone
ORDER BY total_revenue DESC
LIMIT 1;
```

**Answer:** `East Harlem North`

---

## Question 5: Green Taxi Trip Counts (October 2019)

```sql
SELECT SUM(total_monthly_trips)
FROM `ny_taxi.fct_monthly_zone_revenue`
WHERE service_type = 'Green'
  AND EXTRACT(YEAR FROM revenue_month) = 2019
  AND EXTRACT(MONTH FROM revenue_month) = 10;
```

**Answer:** `384,624`

---

## Question 6: Build a Staging Model for FHV Data

1. Load FHV trip data for 2019 from [GitHub releases](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/fhv)
2. Create staging model `stg_fhv_tripdata` with:
   - Filter: `WHERE dispatching_base_num IS NOT NULL`
   - Rename fields (e.g., `PUlocationID` → `pickup_location_id`)

```sql
SELECT COUNT(*) FROM `ny_taxi.stg_fhv_tripdata`;
```

**Answer:** `43,244,693`

---

## Summary of Answers

| Question | Answer |
|----------|--------|
| Q1 | int_trips_unioned only |
| Q2 | dbt will fail the test, returning a non-zero exit code |
| Q3 | 12,184 |
| Q4 | East Harlem North |
| Q5 | 384,624 |
| Q6 | 43,244,693 |

---

## Files Included

- `README.md` - This solutions file
- `homework.md` - Original homework questions (reference)
