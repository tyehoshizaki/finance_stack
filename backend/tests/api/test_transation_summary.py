from tests.api.helper_test_functions import create_transaction

# Testing summary

# test get summary with no transactions returns zeros
def test_get_summary_no_transactions(client):
    response = client.get("/transactions/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_income"] == 0
    assert data["total_expense"] == 0
    assert data["total_transfer"] == 0
    assert data["net_balance"] == 0
    assert data["transaction_count"] == 0
    
# test get summary with transactions returns correct totals and counts
def test_get_summary_with_transactions(client):
    # Create transactions
    transactions_types = ["income", "expense", "transfer"]
    for i in range(6):
        create_transaction(client, amount=100+100*i, transaction_type=transactions_types[i%3])
        
    # income: 100 + 400 = 500
    # expense: 200 + 500 = 700
    # transfer: 300 + 600 = 900

    # Get summary
    response = client.get("/transactions/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_income"] == 500
    assert data["total_expense"] == 700
    assert data["total_transfer"] == 900
    assert data["net_balance"] == -200  # income - expense
    assert data["transaction_count"] == 6
    
    
def test_summary_without_filters(client):
    # Create transactions
    create_transaction(client, amount=100, transaction_type="income", category="Salary", transaction_date="2024-06-01")
    create_transaction(client, amount=200, transaction_type="expense", category="Food", transaction_date="2024-06-02")
    create_transaction(client, amount=300, transaction_type="transfer", category="Bank", transaction_date="2024-06-03")
    
    # Get summary without filters
    response = client.get("/transactions/summary")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total_income"] == 100
    assert data["total_expense"] == 200
    assert data["total_transfer"] == 300
    assert data["net_balance"] == -100  # income - expense
    assert data["transaction_count"] == 3

def test_summary_applies_filters(client):
    # Create transactions
    create_transaction(client, amount=100, transaction_type="income", category="Salary", transaction_date="2024-06-01")
    create_transaction(client, amount=200, transaction_type="expense", category="Food", transaction_date="2024-06-02")
    create_transaction(client, amount=300, transaction_type="transfer", category="Bank", transaction_date="2024-06-03")
    
    # Apply filters to get only income transactions
    response = client.get("/transactions/summary?transaction_type=income")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total_income"] == 100
    assert data["total_expense"] == 0
    assert data["total_transfer"] == 0
    assert data["net_balance"] == 100  # income - expense
    assert data["transaction_count"] == 1

def test_summary_returns_zero_values_when_no_transactions_match(client):
    # Create a transaction that does not match the filter
    create_transaction(client, amount=100, transaction_type="income", category="Salary", transaction_date="2024-06-01")
    
    # Apply filters that do not match any transactions
    response = client.get("/transactions/summary?category=NonExistentCategory&transaction_type=expense&min_amount=1000&max_amount=2000&first_date=2025-01-01&last_date=2025-12-31")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total_income"] == 0
    assert data["total_expense"] == 0
    assert data["total_transfer"] == 0
    assert data["net_balance"] == 0
    assert data["transaction_count"] == 0