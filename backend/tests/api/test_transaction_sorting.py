from tests.api.helper_test_functions import create_transaction

# Testing Sorting Transactions

def test_sort_transactions_by_date(client):
    # Create multiple transactions
    for i in range(5):
        create_transaction(client, name=f"Transaction {i+1}", amount=100.0 * (i+1), transaction_date=f"2024-06-0{i+1}")

    # Test sorting transactions by date
    response = client.get("/transactions/?sort_by=transaction_date&sort_order=asc")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    data = data["items"]
    assert isinstance(data, list)
    assert len(data) == 5  # Should return 5 transactions
    assert data[0]["transaction_date"] == "2024-06-01"  # First transaction should be the earliest date
    assert data[-1]["transaction_date"] == "2024-06-05"  # Last transaction should be the latest date
    
def test_sort_transactions_by_amount(client):
    # Create multiple transactions
    for i in range(5):
        create_transaction(client, name=f"Transaction {i+1}", amount=100.0 * (i+1))

    # Test sorting transactions by amount
    response = client.get("/transactions/?sort_by=amount&sort_order=desc")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    data = data["items"]
    assert isinstance(data, list)
    assert len(data) == 5  # Should return 5 transactions
    assert data[0]["amount"] == 500.0  # First transaction should be the highest amount
    assert data[-1]["amount"] == 100.0  # Last transaction should be the lowest amount
    
def test_sort_transactions_by_category(client):
    # Create multiple transactions with different categories
    categories = ["Salary", "Groceries", "Entertainment", "Utilities", "Miscellaneous"]
    for i in range(5):
        create_transaction(client, name=f"Transaction {i+1}", amount=100.0 * (i+1), category=categories[i])

    # Test sorting transactions by category
    response = client.get("/transactions/?sort_by=category&sort_order=asc")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    data = data["items"]
    assert isinstance(data, list)
    assert len(data) == 5  # Should return 5 transactions
    assert data[0]["category"] == "Entertainment"  # First transaction should be the first category alphabetically
    assert data[-1]["category"] == "Utilities"  # Last transaction should be the last category alphabetically
    
def test_sort_transactions_by_type(client):
    # Create multiple transactions with different types
    types = ["income", "expense", "income", "expense", "income"]
    for i in range(5):
        create_transaction(client, name=f"Transaction {i+1}", amount=100.0 * (i+1), transaction_type=types[i])

    # Test sorting transactions by type
    response = client.get("/transactions/?sort_by=transaction_type&sort_order=asc")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    data = data["items"]
    assert isinstance(data, list)
    assert len(data) == 5  # Should return 5 transactions
    assert data[0]["transaction_type"] == "expense"  # First transaction should be the first type alphabetically
    assert data[-1]["transaction_type"] == "income"  # Last transaction should be the last type alphabetically
    
def test_sort_transactions_by_id(client):
    # Create multiple transactions
    for i in range(5):
        create_transaction(client, name=f"Transaction {i+1}", amount=100.0 * (i+1))

    # Test sorting transactions by ID
    response = client.get("/transactions/?sort_by=id&sort_order=asc")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    data = data["items"]
    assert isinstance(data, list)
    assert len(data) == 5  # Should return 5 transactions
    assert data[0]["id"] == 1  # First transaction should have the lowest ID
    assert data[-1]["id"] == 5  # Last transaction should have the highest ID
    
def test_sort_transactions_by_name(client):
    # Create multiple transactions with different names
    names = ["Zeta", "Alpha", "Delta", "Beta", "Gamma"]
    for i in range(5):
        create_transaction(client, name=names[i], amount=100.0 * (i+1))

    # Test sorting transactions by name
    response = client.get("/transactions/?sort_by=name&sort_order=asc")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    data = data["items"]
    assert isinstance(data, list)
    assert len(data) == 5  # Should return 5 transactions
    assert data[0]["name"] == "Alpha"  # First transaction should be the first name alphabetically
    assert data[-1]["name"] == "Zeta"  # Last transaction should be the last name alphabetically