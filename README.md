# Sample SQL Queries

This repository contains a compact PostgreSQL sample dataset and five optimized analytical queries built on top of it.

## Contents

- `sample_queries.sql`: schema, seed data, indexes, and query examples

## Dataset

The sample dataset models a small retail workflow with four related tables:

- `customers`
- `products`
- `orders`
- `order_items`

The script inserts enough sample data to test joins, filters, aggregations, and grouped reporting queries.

## Included Queries

The SQL file includes five optimized queries:

1. Monthly revenue for completed orders
2. Top 3 customers by lifetime spend
3. Best-selling electronics products by quantity sold
4. Repeat customers with more than one completed order
5. Regional average order value

## Optimization Notes

The script includes supporting indexes and follows a few practical query patterns:

- filter early on selective columns such as `status`, `category`, and `order_date`
- aggregate only after narrowing the working set
- use indexed join keys for relational lookups
- precompute order totals once before rolling them up by region

## How To Run

Use PostgreSQL and execute the script:

```sql
\i sample_queries.sql
```

Or from the shell:

```powershell
psql -U <username> -d <database_name> -f sample_queries.sql
```

## Expected Use

This project is suitable for:

- SQL practice
- query optimization demos
- portfolio examples
- database interview preparation

## Branch And Push

If this folder is a standalone git repo, you can push it with:

```powershell
git checkout -b feat/sample-sql-queries
git add .
git commit -m "Add sample dataset and optimized SQL queries"
git remote add origin <your-github-repo-url>
git push -u origin feat/sample-sql-queries
```
