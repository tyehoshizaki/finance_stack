# test create transaction successfully
def test_create_transaction_success(client):
    transaction_data = {
        "name": "June Salary",
        "amount": 100.0,
        "category": "Salary",
        "transaction_type": "income",
        "transaction_date": "2024-06-01"
    }
    response = client.post("/transactions/", json=transaction_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == transaction_data["name"]
    assert data["amount"] == transaction_data["amount"]
    assert data["category"] == transaction_data["category"]
    assert data["transaction_type"] == transaction_data["transaction_type"]
    assert data["transaction_date"] == transaction_data["transaction_date"]
    
# test create transaction with missing required fields fails (name)
def test_create_transaction_missing_fields_name(client):
    transaction_data = {
        # "name": "June Salary", missing field
        "amount": 100.0,
        "category": "Salary",
        "transaction_type": "income",
        "transaction_date": "2024-06-01"
    }
    response = client.post("/transactions/", json=transaction_data)
    assert response.status_code == 422  # Unprocessable Entity
    
# test create transaction with missing required fields fails (amount)
def test_create_transaction_missing_fields_amount(client):
    transaction_data = {
        "name": "June Salary",
        # "amount": 100.0, missing field
        "category": "Salary",
        "transaction_type": "income",
        "transaction_date": "2024-06-01"
    }
    response = client.post("/transactions/", json=transaction_data)
    assert response.status_code == 422  # Unprocessable Entity

    # test create transaction with missing required fields fails (category)
def test_create_transaction_missing_fields_category(client):
    transaction_data = {
        "name": "June Salary",
        "amount": 100.0,
        # "category": "Salary", missing field
        "transaction_type": "income",
        "transaction_date": "2024-06-01"
    }
    response = client.post("/transactions/", json=transaction_data)
    assert response.status_code == 422  # Unprocessable Entity
        
    # test create transaction with missing required fields fails (transaction_type)
def test_create_transaction_missing_fields_transaction_type(client):
    transaction_data = {
        "name": "June Salary",
        "amount": 100.0,
        "category": "Salary",
        # "transaction_type": "income", missing field
        "transaction_date": "2024-06-01"
    }
    response = client.post("/transactions/", json=transaction_data)
    assert response.status_code == 422  # Unprocessable Entity

    # test create transaction with missing required fields fails (transaction_date)
def test_create_transaction_missing_fields_transaction_date(client):
    transaction_data = {
        "name": "June Salary",
        "amount": 100.0,
        "category": "Salary",
        "transaction_type": "income",
        # "transaction_date": "2024-06-01", missing field
    }
    response = client.post("/transactions/", json=transaction_data)
    assert response.status_code == 422  # Unprocessable Entity
    
# test create transaction with invalid transaction_type fails
def test_create_transaction_invalid_type(client):
    transaction_data = {
        "name": "June Salary",
        "amount": 100.0,
        "category": "Salary",
        "transaction_type": "invalid",
        "transaction_date": "2024-06-01"
    }
    response = client.post("/transactions/", json=transaction_data)
    assert response.status_code == 422  # Unprocessable Entity

# test create transaction with negative amount fails
def test_create_transaction_negative_amount(client):
    transaction_data = {
        "name": "June Salary",
        "amount": -100.0,
        "category": "Salary",
        "transaction_type": "income",
        "transaction_date": "2024-06-01"
    }
    response = client.post("/transactions/", json=transaction_data)
    assert response.status_code == 422  # Unprocessable Entity


