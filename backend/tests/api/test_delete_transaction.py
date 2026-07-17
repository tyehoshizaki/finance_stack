from tests.api.helper_test_functions import create_transaction

# Delete Transaction Tests

# test delete transaction successfully
def test_delete_transaction_success(client):
    # First, create a transaction
    create_response = create_transaction(client)
    transaction_id = create_response["id"]

    # Delete the transaction
    response = client.delete(f"/transactions/{transaction_id}")
    assert response.status_code == 200
    
# test delete non-existent transaction fails with 404
def test_delete_transaction_not_found(client):
    response = client.delete("/transactions/9999")  # Assuming 9999 does not exist
    assert response.status_code == 404
    
# test delete transaction can no longer be retrieved after deletion
def test_delete_transaction_cannot_retrieve(client):
    # First, create a transaction
    create_response = create_transaction(client)
    transaction_id = create_response["id"]

    # Delete the transaction
    client.delete(f"/transactions/{transaction_id}")

    # Attempt to retrieve the deleted transaction
    response = client.get(f"/transactions/{transaction_id}")
    assert response.status_code == 404