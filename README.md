# Dashboard as a Service - Backend

This is the FastAPI backend for the Dashboard as a Service application.

## Features
- **File Upload**: Support for CSV and Excel (.xls, .xlsx) files.
- **Data Analysis**: Automatic data summary generation using Pandas.
- **CORS Enabled**: Configured for cross-origin requests.

## Setup
1. Install dependencies:
   ```bash
   uv sync
   ```
2. Run the server:
   ```bash
   uv run main.py
   ```
3. Run tests:
   ```bash
   uv run pytest
   ```

## API Endpoints
- `GET /`: Health check.
- `POST /api/upload`: Upload a file for processing.

  

# Dashboard as a Service - Frontend

Frontend for the Service  (navigate to frontend folder)

## Setup
1. Install dependencies using bun:
   ```bash
   
   bun install
   ```
2. Run dev:
  ```bash

      bun run dev
   ```

