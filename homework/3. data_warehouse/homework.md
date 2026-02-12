## Module 3 Homework: Data Warehouse

ATTENTION: At the end of the submission form, you will be required to include a link to your GitHub repository or other public code-hosting site. This repository should contain your code for solving the homework. If your solution includes code that is not in file format, please include these directly in the README file of your repository.

> In case you don't get one option exactly, select the closest one

For this homework we will be using the 2024 Yellow Taxi Trip Data.

We will use the data loaded into BigQuery from external sources (GCS bucket).

### Question 1. What is count of records for the 2024 Yellow Taxi Data? (1 point)

- 65,623
- 840,402
- 20,332,093
- 85,431,289

### Question 2. Estimated data read (External Table vs Materialized Table)

What is the estimated amount of data that will be read when this query is executed on the External Table and the Table? (1 point)

- 18.82 MB for the External Table and 47.60 MB for the Materialized Table
- 0 MB for the External Table and 155.12 MB for the Materialized Table
- 2.14 GB for the External Table and 0MB for the Materialized Table
- 0 MB for the External Table and 0MB for the Materialized Table

### Question 3. Why are the estimated number of Bytes different? (1 point)

- BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.
- BigQuery duplicates data across multiple storage partitions, so selecting two columns instead of one requires scanning the table twice, doubling the estimated bytes processed.
- BigQuery automatically caches the first queried column, so adding a second column increases processing time but does not affect the estimated bytes scanned.
- When selecting multiple columns, BigQuery performs an implicit join operation between them, increasing the estimated bytes processed.

### Question 4. How many records have a fare_amount of 0? (1 point)

- 128,210
- 546,578
- 20,188,016
- 8,333

### Question 5. Optimized table strategy (1 point)

What is the best strategy to make an optimized table in Big Query if your query will always filter based on `tpep_dropoff_datetime` and order the results by `VendorID`?

- Partition by tpep_dropoff_datetime and Cluster on VendorID
- Cluster on by tpep_dropoff_datetime and Cluster on VendorID
- Cluster on tpep_dropoff_datetime Partition by VendorID
- Partition by tpep_dropoff_datetime and Partition by VendorID

### Question 6. Partitioned vs Non-partitioned table (1 point)

Write a query to retrieve the distinct VendorIDs between `tpep_dropoff_datetime` 2024-03-01 and 2024-03-15 (inclusive). Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?

- 12.47 MB for non-partitioned table and 326.42 MB for the partitioned table
- 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table
- 5.87 MB for non-partitioned table and 0 MB for the partitioned table
- 310.31 MB for non-partitioned table and 285.64 MB for the partitioned table

### Question 7. Where is the data stored in the External Table you created? (1 point)

- Big Query
- Container Registry
- GCP Bucket
- Big Table

### Question 8. Best practice: always cluster? (1 point)

It is best practice in Big Query to always cluster your data:

- True
- False

### Question 9 (Not graded)

Write a `SELECT count(*)` query FROM the materialized table you created. How many bytes does it estimate will be read? Why?

## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2026/homework/hw3
