from tests.api.helper_test_functions import create_transaction

# Get Transactions Tests

# test get all transaction empty list
def test_get_all_transactions_empty(client):
    response = client.get("/transactions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    data = data["items"]
    assert isinstance(data, list)
    assert len(data) == 0
    
# test get all transactions with one transaction
def test_get_all_transactions_one(client):
    # First, create a transaction
    create_transaction(client)

    # Then, retrieve all transactions
    response = client.get("/transactions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    data = data["items"]
    assert isinstance(data, list)
    assert len(data) == 1

# test get all transactions with multiple transactions
def test_get_all_transactions_multiple(client):
    # Create multiple transactions
    
    test_number = 5
    for i in range(test_number):
        create_transaction(client, name=f"Transaction {i+1}", amount=100.0 * (i+1))

    # Retrieve all transactions
    response = client.get("/transactions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    data = data["items"]
    assert isinstance(data, list)
    assert len(data) == test_number 
    
# Get Transactions with transaction_id

# test get transaction by id successfully
def test_get_transaction_by_id_success(client):
    # First, create a transaction
    transaction_data = {
        "name": "June Salary",
        "amount": 100.0,
        "category": "Salary",
        "transaction_type": "income",
        "transaction_date": "2024-06-01"
    }
    create_response = create_transaction(client, **transaction_data)
    transaction_id = create_response["id"]

    # Then, retrieve the transaction by id
    response = client.get(f"/transactions/{transaction_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == transaction_id
    assert data["name"] == transaction_data["name"]
    assert data["amount"] == transaction_data["amount"]
    assert data["category"] == transaction_data["category"]
    assert data["transaction_type"] == transaction_data["transaction_type"]
    assert data["transaction_date"] == transaction_data["transaction_date"]
    
# test get transaction by id not found fails with 404
def test_get_transaction_by_id_not_found(client):
    response = client.get("/transactions/9999")  # Assuming 9999 does not exist
    assert response.status_code == 404

