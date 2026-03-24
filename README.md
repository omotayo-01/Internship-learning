# CRUD API for Jobs and Companies

This is a FastAPI application that provides CRUD endpoints for Job and Company entities, with query parameter filtering for jobs by location and job_type.

## Installation

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:

   ```bash
   uvicorn main:app --reload
   ```

3. Open your browser to `http://127.0.0.1:8000/docs` to see the interactive API documentation.

## Endpoints

### Companies

- `POST /companies/` - Create a company
- `GET /companies/` - List companies
- `GET /companies/{company_id}` - Get a specific company
- `PUT /companies/{company_id}` - Update a company
- `DELETE /companies/{company_id}` - Delete a company

### Jobs

- `POST /jobs/` - Create a job
- `GET /jobs/` - List jobs (with optional filtering by location and job_type)
- `GET /jobs/{job_id}` - Get a specific job
- `PUT /jobs/{job_id}` - Update a job
- `DELETE /jobs/{job_id}` - Delete a job

## Filtering

For the `/jobs/` endpoint, you can filter by:

- `location`: Filter jobs by location (case-insensitive partial match)
- `job_type`: Filter jobs by job type (case-insensitive partial match)

Example: `GET /jobs/?location=New%20York&job_type=full-time`
