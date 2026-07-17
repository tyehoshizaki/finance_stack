from pydantic import ValidationError
import pytest

from tests.api.helper_test_functions import create_transaction

# Filter Transactions Tests

# test filter transactions by category successfully
def test_filter_transactions_by_category(client):
    # Create transactions with different categories
    transactions = [
        {
            "name": "June Salary",
            "amount": 100,
            "category": "Salary",
            "transaction_type": "income",
            "transaction_date": "2024-06-01"
        },
        {
            "name": "Grocery Shopping",
            "amount": 50,
            "category": "Groceries",
            "transaction_type": "expense",
            "transaction_date": "2024-06-02"
        }
    ]
    for transaction in transactions:
        create_transaction(client, **transaction)

    # Filter by category 'Salary'
    response = client.get("/transactions/?category=Salary")
    assert response.status_code == 200
    data = response.json()
    data = data["items"]
    assert len(data) == 1
    assert data[0]["category"] == "Salary"
    
# test filter transactions by type successfully
def test_filter_transactions_by_type(client):
    # Create transactions with different types
    transactions = [
        {
            "name": "June Salary",
            "amount": 100,
            "category": "Salary",
            "transaction_type": "income",
            "transaction_date": "2024-06-01"
        },
        {
            "name": "Grocery Shopping",
            "amount": 50,
            "category": "Groceries",
            "transaction_type": "expense",
            "transaction_date": "2024-06-02"
        }
    ]
    for transaction in transactions:
        create_transaction(client, **transaction)

    # Filter by transaction_type 'income'
    response = client.get("/transactions/?transaction_type=income")
    assert response.status_code == 200
    data = response.json()
    data = data["items"]
    assert len(data) == 1
    assert data[0]["transaction_type"] == "income"
    
# test filter transactions by amount range successfully
def test_filter_transactions_by_amount_range(client):
    # Create transactions with different amounts
    transactions = [
        {
            "name": "June Salary",
            "amount": 175,
            "category": "Salary",
            "transaction_type": "income",
            "transaction_date": "2024-06-01"
        },
        {
            "name": "June Salary",
            "amount": 150,
            "category": "Salary",
            "transaction_type": "income",
            "transaction_date": "2024-06-01"
        },
        {
            "name": "June Salary",
            "amount": 100,
            "category": "Salary",
            "transaction_type": "income",
            "transaction_date": "2024-06-01"
        },
        {
            "name": "June Salary",
            "amount": 60,
            "category": "Salary",
            "transaction_type": "income",
            "transaction_date": "2024-06-01"
        },
        {
            "name": "Grocery Shopping",
            "amount": 50,
            "category": "Groceries",
            "transaction_type": "expense",
            "transaction_date": "2024-06-02"
        }
    ]
    for transaction in transactions:
        create_transaction(client, **transaction)

    # Filter by amount range 60 to 150
    response = client.get("/transactions/?min_amount=60&max_amount=150")
    assert response.status_code == 200
    data = response.json()
    data = data["items"]
    assert len(data) == 3
    assert data[1]["amount"] == 100
    
# test filter transactions by date range successfully
def test_filter_transactions_by_date_range(client):
    # Create transactions with different dates
    transactions = [
        {
            "name": "June Salary",
            "amount": 175,
            "category": "Salary",
            "transaction_type": "income",
            "transaction_date": "2024-05-31"
        },
        {
            "name": "June Salary",
            "amount": 150,
            "category": "Salary",
            "transaction_type": "income",
            "transaction_date": "2024-06-01"
        },
        {
            "name": "June Salary",
            "amount": 100,
            "category": "Salary",
            "transaction_type": "income",
            "transaction_date": "2024-06-02"
        },
        {
            "name": "June Salary",
            "amount": 60,
            "category": "Salary",
            "transaction_type": "income",
            "transaction_date": "2024-06-03"
        },
        {
            "name": "Grocery Shopping",
            "amount": 50,
            "category": "Groceries",
            "transaction_type": "expense",
            "transaction_date": "2024-06-04"
        }
    ]
    for transaction in transactions:
        create_transaction(client, **transaction)

    # Filter by date range 2024-06-01 to 2024-06-01
    response = client.get("/transactions/?first_date=2024-06-01&last_date=2024-06-03")
    assert response.status_code == 200
    data = response.json()
    data = data["items"]
    assert len(data) == 3
    assert data[1]["transaction_date"] == "2024-06-02"
    
    
def test_invalid_amount_range(client):
    with pytest.raises(ValidationError) as exc_info:
        client.get("/transactions/?min_amount=200&max_amount=100")
    
    assert "min_amount cannot be greater than max_amount" in str(exc_info.value)
    
def test_invalid_date_range(client):
    with pytest.raises(ValidationError) as exc_info:
        client.get("/transactions/?first_date=2024-06-03&last_date=2024-06-01")
    
    assert "first_date cannot be greater than last_date" in str(exc_info.value)