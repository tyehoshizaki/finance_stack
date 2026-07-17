from tests.api.helper_test_functions import create_transaction

# Update Transaction Tests

# test update transaction successfully
def test_update_transaction_success(client):
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

    # Update the transaction
    update_data = {
        "name": "Updated Salary",
        "amount": 150.0
    }
    response = client.patch(f"/transactions/{transaction_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == transaction_id
    assert data["name"] == update_data["name"]
    assert data["amount"] == update_data["amount"]
    
# test update non-existent transaction fails with 404
def test_update_transaction_not_found(client):
    update_data = {
        "name": "Updated Salary",
        "amount": 150.0
    }
    response = client.patch("/transactions/9999", json=update_data)  # Assuming 9999 does not exist
    assert response.status_code == 404
    
# test update transaction with invalid data fails
def test_update_transaction_invalid_data(client):
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

    # Attempt to update with invalid data (negative amount)
    update_data = {
        "amount": -150.0
    }
    response = client.patch(f"/transactions/{transaction_id}", json=update_data)
    assert response.status_code == 422  # Unprocessable Entity
    
    