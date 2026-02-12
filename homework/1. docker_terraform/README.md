# Module 1 Homework: Docker & SQL - Solutions

## Question 1: Understanding Docker Images

**Command used:**
```bash
docker run -it --entrypoint bash python:3.13
pip --version
```

**Answer:** `25.3`

---

## Question 2: Understanding Docker Networking

In Docker Compose, services communicate using the **service name** as hostname and the **internal port** (not the mapped host port).

From the given docker-compose.yaml:
- Service name: `db` (or container name: `postgres`)
- Internal PostgreSQL port: `5432`

**Answer:** `postgres:5432` / `db:5432`

---

## Data Preparation

```bash
# Download the data
wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv

# Start containers
docker-compose up -d

# Install Python dependencies
pip install pandas sqlalchemy psycopg2-binary pyarrow

# Ingest data
python ingest_data.py
```

Access pgAdmin at http://localhost:8085 (login: admin@admin.com / root)

---

## Question 3: Counting Short Trips

```sql
SELECT COUNT(*) 
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 1;
```

**Answer:** `8,007`

---

## Question 4: Longest Trip for Each Day

```sql
SELECT DATE(lpep_pickup_datetime) AS pickup_day, 
       MAX(trip_distance) AS max_distance
FROM green_taxi_trips
WHERE trip_distance < 100
GROUP BY DATE(lpep_pickup_datetime)
ORDER BY max_distance DESC
LIMIT 1;
```

**Answer:** `2025-11-14`

---

## Question 5: Biggest Pickup Zone (Nov 18)

```sql
SELECT z."Zone", SUM(t.total_amount) AS total
FROM green_taxi_trips t
JOIN taxi_zones z ON t."PULocationID" = z."LocationID"
WHERE DATE(lpep_pickup_datetime) = '2025-11-18'
GROUP BY z."Zone"
ORDER BY total DESC
LIMIT 1;
```

**Answer:** `East Harlem North`

---

## Question 6: Largest Tip from East Harlem North

```sql
SELECT dz."Zone" AS dropoff_zone, MAX(t.tip_amount) AS max_tip
FROM green_taxi_trips t
JOIN taxi_zones pz ON t."PULocationID" = pz."LocationID"
JOIN taxi_zones dz ON t."DOLocationID" = dz."LocationID"
WHERE pz."Zone" = 'East Harlem North'
  AND lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime < '2025-12-01'
GROUP BY dz."Zone"
ORDER BY max_tip DESC
LIMIT 1;
```

**Answer:** `Yorkville West`

---

## Question 7: Terraform Workflow

Based on [Terraform Overview](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/terraform/1_terraform_overview.md):

1. `terraform init` - Initializes & configures backend, installs plugins/providers
2. `terraform apply -auto-approve` - Applies changes without prompting for approval  
3. `terraform destroy` - Removes stack from Cloud

**Answer:** `terraform init, terraform apply -auto-approve, terraform destroy`

---

## Summary of Answers

| Question | Answer |
|----------|--------|
| Q1 | 25.3 |
| Q2 | postgres:5432 / db:5432 |
| Q3 | 8,007 |
| Q4 | 2025-11-14 |
| Q5 | East Harlem North |
| Q6 | Yorkville West |
| Q7 | terraform init, terraform apply -auto-approve, terraform destroy |
