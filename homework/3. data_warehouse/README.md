# Module 3 Homework: Data Warehouse (BigQuery) - Solutions

## Overview

This homework covers BigQuery as a Data Warehouse, working with the 2024 Yellow Taxi Trip Data. Topics include external tables, materialized tables, partitioning, clustering, and query optimization.

## Setup

### 1. Upload Data to GCS

```bash
# Download 2024 Yellow Taxi data (Parquet format)
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-02.parquet
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-03.parquet
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-04.parquet
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-05.parquet
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-06.parquet

# Upload to GCS bucket
gsutil -m cp yellow_tripdata_2024-*.parquet gs://<your-bucket>/yellow_taxi_2024/
```

### 2. Create External Table in BigQuery

```sql
CREATE OR REPLACE EXTERNAL TABLE `<project>.<dataset>.yellow_taxi_2024_external`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://<your-bucket>/yellow_taxi_2024/yellow_tripdata_2024-*.parquet']
);
```

### 3. Create Materialized (Native) Table

```sql
CREATE OR REPLACE TABLE `<project>.<dataset>.yellow_taxi_2024_materialized`
AS SELECT * FROM `<project>.<dataset>.yellow_taxi_2024_external`;
```

---

## Question 1: Record Count for 2024 Yellow Taxi Data

```sql
SELECT COUNT(*)
FROM `<project>.<dataset>.yellow_taxi_2024_materialized`;
```

**Answer:** `20,332,093`

---

## Question 2: Estimated Data Read (External vs Materialized)

```sql
-- Query on External Table
SELECT COUNT(DISTINCT PULocationID)
FROM `<project>.<dataset>.yellow_taxi_2024_external`;

-- Query on Materialized Table
SELECT COUNT(DISTINCT PULocationID)
FROM `<project>.<dataset>.yellow_taxi_2024_materialized`;
```

BigQuery cannot estimate data size for external tables (shows 0 MB), but can estimate for native/materialized tables.

**Answer:** `0 MB for the External Table and 155.12 MB for the Materialized Table`

---

## Question 3: Why Are Estimated Bytes Different?

BigQuery is a **columnar database**. It only scans the specific columns requested in a query. Querying two columns (`PULocationID`, `DOLocationID`) requires reading more data than querying one column (`PULocationID`), leading to a higher estimated number of bytes processed.

**Answer:** `BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.`

---

## Question 4: Records with fare_amount of 0

```sql
SELECT COUNT(*)
FROM `<project>.<dataset>.yellow_taxi_2024_materialized`
WHERE fare_amount = 0;
```

**Answer:** `8,333`

---

## Question 5: Best Optimization Strategy

When queries always **filter** on `tpep_dropoff_datetime` and **order** by `VendorID`:
- **Partition** on the filter column → prunes entire partitions (date ranges)
- **Cluster** on the order column → sorts data within partitions for faster scans

```sql
CREATE OR REPLACE TABLE `<project>.<dataset>.yellow_taxi_2024_partitioned_clustered`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID
AS SELECT * FROM `<project>.<dataset>.yellow_taxi_2024_materialized`;
```

**Answer:** `Partition by tpep_dropoff_datetime and Cluster on VendorID`

---

## Question 6: Partitioned vs Non-partitioned Bytes

```sql
-- Non-partitioned (materialized) table
SELECT DISTINCT VendorID
FROM `<project>.<dataset>.yellow_taxi_2024_materialized`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

-- Partitioned + Clustered table
SELECT DISTINCT VendorID
FROM `<project>.<dataset>.yellow_taxi_2024_partitioned_clustered`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
```

The partitioned table scans far less data because it only reads the relevant date partitions.

**Answer:** `310.24 MB for non-partitioned table and 26.84 MB for the partitioned table`

---

## Question 7: External Table Data Storage

External tables do not store data in BigQuery. The data remains in its original location — the GCS bucket.

**Answer:** `GCP Bucket`

---

## Question 8: Always Cluster?

**False.** Clustering is not always beneficial:
- Small tables (< 1 GB) don't benefit from clustering
- Tables rarely queried or filtered don't need clustering
- Clustering adds overhead during data ingestion

**Answer:** `False`

---

## Question 9 (Not Graded): SELECT COUNT(*) Bytes

```sql
SELECT COUNT(*)
FROM `<project>.<dataset>.yellow_taxi_2024_materialized`;
```

**Estimated bytes: 0 bytes.** BigQuery stores table metadata (including row counts) internally, so a `COUNT(*)` without any filter does not need to scan any actual data — it reads the count directly from metadata.

---

## Summary of Answers

| Question | Answer |
|----------|--------|
| Q1 | 20,332,093 |
| Q2 | 0 MB for External Table and 155.12 MB for Materialized Table |
| Q3 | BigQuery is columnar — scans only requested columns |
| Q4 | 8,333 |
| Q5 | Partition by tpep_dropoff_datetime and Cluster on VendorID |
| Q6 | 310.24 MB for non-partitioned and 26.84 MB for partitioned |
| Q7 | GCP Bucket |
| Q8 | False |
| Q9 | 0 bytes (metadata cached) |

---

## Files Included

- `README.md` - This solutions file
- `homework.md` - Original homework questions (reference)
