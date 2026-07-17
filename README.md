# Finance Tracker API

A RESTful personal finance tracking API built with **FastAPI** and **SQLAlchemy**. This project is designed to help manage financial transactions while demonstrating modern backend development practices, including layered architecture, database persistence, filtering, sorting, pagination, validation, and automated testing.

---

## Features

### Transactions

* Create transactions
* View all transactions
* Retrieve a single transaction
* Update existing transactions
* Delete transactions

### Filtering

Filter transactions by:

* Category
* Transaction type
* Minimum amount
* Maximum amount
* Start date
* End date

### Sorting

Sort transactions by:

* Transaction date
* Amount
* Category
* Transaction type
* Name
* ID

Supports both:

* Ascending order
* Descending order

### Pagination

Large transaction lists can be paginated using:

* Page number
* Page size

Responses include metadata such as:

* Current page
* Total pages
* Total items
* Has next page
* Has previous page

### Financial Summary

Generate an overview containing:

* Total income
* Total expenses
* Total transfers
* Net balance
* Transaction count

---

# Tech Stack

* Python 3.14+
* FastAPI
* SQLAlchemy 2.0
* SQLite
* Pydantic v2
* Uvicorn
* Pytest

---

# Project Structure

```text
app/
├── api/
│   └── transactions.py      # API routes
│
├── crud/
│   └── transactions.py      # Database operations
│
├── services/
│   └── transactions.py      # Business logic
│
├── models/
│   └── models.py            # SQLAlchemy models
│
├── schemas/
│   └── schemas.py           # Pydantic models
│
├── databases/
│   └── database.py          # Database configuration
│
├── utils/
│   └── pagination.py
│
├── core/
│   ├── constants.py
│   └── types.py
│
└── main.py
```

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
cd Finance_stack
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

Linux/macOS

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the API

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Interactive documentation:

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# Running Tests

Run all tests:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

---

# API Endpoints

| Method | Endpoint                | Description            |
| ------ | ----------------------- | ---------------------- |
| GET    | `/transactions`         | List transactions      |
| GET    | `/transactions/{id}`    | Retrieve a transaction |
| POST   | `/transactions`         | Create a transaction   |
| PATCH  | `/transactions/{id}`    | Update a transaction   |
| DELETE | `/transactions/{id}`    | Delete a transaction   |
| GET    | `/transactions/summary` | Financial summary      |

---

# Query Parameters

## Filtering

| Parameter        | Description                  |
| ---------------- | ---------------------------- |
| category         | Filter by category           |
| transaction_type | income, expense, or transfer |
| min_amount       | Minimum amount               |
| max_amount       | Maximum amount               |
| first_date       | Earliest transaction date    |
| last_date        | Latest transaction date      |

## Sorting

| Parameter  | Values                                                         |
| ---------- | -------------------------------------------------------------- |
| sort_by    | transaction_date, amount, category, transaction_type, name, id |
| sort_order | asc, desc                                                      |

## Pagination

| Parameter | Description                     |
| --------- | ------------------------------- |
| page      | Page number (starts at 1)       |
| page_size | Number of transactions per page |

Example:

```text
GET /transactions?category=food&sort_by=amount&sort_order=desc&page=1&page_size=10
```

---

# Money Representation

To avoid floating-point rounding errors, monetary values are stored as **integer ticks**.

Current conversion:

* 10,000 ticks = $1.00
* 1 tick = $0.0001

Examples:

| Dollars | Stored Value |
| ------- | -----------: |
| $1.00   |        10000 |
| $5.50   |        55000 |
| $10.99  |       109900 |

---

# Validation

The API validates:

* Required fields
* String lengths
* Transaction types
* Amounts
* Date ranges
* Pagination limits
* Sorting options

Invalid requests return descriptive validation errors.

---

# Architecture

The application follows a layered architecture.

```text
HTTP Request
      │
      ▼
API Routes
      │
      ▼
Business Services
      │
      ▼
CRUD Layer
      │
      ▼
Database
```

Each layer has a single responsibility:

* **API** handles HTTP requests and responses.
* **Services** contain business logic.
* **CRUD** performs database operations.
* **Schemas** validate request and response data.
* **Models** define the database schema.

---

# Future Improvements

Planned features include:

* User authentication
* PostgreSQL support
* Alembic database migrations
* Budget management
* Recurring transactions
* CSV import/export
* Dashboard analytics
* Tags
* Search
* File attachments
* Docker deployment
* CI/CD pipeline
* React frontend

---

# License

This project is intended for learning, experimentation, and portfolio development.
