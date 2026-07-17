from tests.api.helper_test_functions import create_transaction

# Test Transaction Pagination Tests

def test_transaction_pagination(client):
    # Create multiple transactions
    for i in range(15):
        create_transaction(client, name=f"Transaction {i+1}", amount=100.0 * (i+1))

    # Test pagination with limit and offset
    response = client.get("/transactions/?page_size=5&page=1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data["items"]) == 5  # Should return 5 transactions
    assert data["page"] == 1  # First page
    assert data["page_size"] == 5  # Page size is 5
    assert data["total_items"] == 15  # Total transactions created
    assert data["total_pages"] == 3  # Total pages should be 3
    assert data["has_next"] == True  # There should be more transactions to fetch
    assert data["has_previous"] == False  # This is the first page, so no previous page
    
def test_transaction_pagination_next_page(client):
    # Create multiple transactions
    for i in range(15):
        create_transaction(client, name=f"Transaction {i+1}", amount=100.0 * (i+1))

    # Test pagination with limit and offset for the second page
    response = client.get("/transactions/?page_size=5&page=2")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data["items"]) == 5  # Should return 5 transactions
    assert data["page"] == 2  # Second page
    assert data["page_size"] == 5  # Page size is 5
    assert data["total_items"] == 15  # Total transactions created
    assert data["total_pages"] == 3  # Total pages should be 3
    assert data["has_next"] == True  # There should be more transactions to fetch
    assert data["has_previous"] == True  # This is not the first page, so there should be a previous page
    
def test_transaction_pagination_last_page(client):
    # Create multiple transactions
    for i in range(15):
        create_transaction(client, name=f"Transaction {i+1}", amount=100.0 * (i+1))

    # Test pagination with limit and offset for the last page
    response = client.get("/transactions/?page_size=5&page=3")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data["items"]) == 5  # Should return 5 transactions
    assert data["page"] == 3  # Last page
    assert data["page_size"] == 5  # Page size is 5
    assert data["total_items"] == 15  # Total transactions created
    assert data["total_pages"] == 3  # Total pages should be 3
    assert data["has_next"] == False  # There should be no more transactions to fetch
    assert data["has_previous"] == True  # This is not the first page, so there should be a previous page
    
def test_partial_page(client):
    # Create multiple transactions
    for i in range(12):
        create_transaction(client, name=f"Transaction {i+1}", amount=100.0 * (i+1))

    # Test pagination with limit and offset for a partial last page
    response = client.get("/transactions/?page_size=5&page=3")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data["items"]) == 2  # Should return 2 transactions (partial page)
    assert data["page"] == 3  # Last page
    assert data["page_size"] == 5  # Page size is 5
    assert data["total_items"] == 12  # Total transactions created
    assert data["total_pages"] == 3  # Total pages should be 3
    assert data["has_next"] == False  # There should be no more transactions to fetch
    assert data["has_previous"] == True  # This is not the first page, so there should be a previous page
    
def test_different_pages_have_different_transactions(client):
    # Create multiple transactions
    for i in range(15):
        create_transaction(client, name=f"Transaction {i+1}", amount=100.0 * (i+1))

    # Test that different pages return different transactions
    response_page_1 = client.get("/transactions/?page_size=5&page=1")
    response_page_2 = client.get("/transactions/?page_size=5&page=2")
    assert response_page_1.status_code == 200
    assert response_page_2.status_code == 200
    data_page_1 = response_page_1.json()
    data_page_2 = response_page_2.json()
    assert data_page_1["items"] != data_page_2["items"]  # The transactions on page 1 should be different from those on page 2
    
def test_empty_database(client):
    # Test pagination on an empty database
    response = client.get("/transactions/?page_size=5&page=1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data["items"]) == 0  # Should return an empty list
    assert data["page"] == 1  # Empty page
    assert data["page_size"] == 5  # Page size is 5
    assert data["total_items"] == 0  # No transactions created
    assert data["total_pages"] == 1  # Total pages should be 1
    assert data["has_next"] == False  # There should be no more transactions to fetch
    assert data["has_previous"] == False  # This is the first page, so no previous page
    
def test_invalid_page_number(client):
    # Create multiple transactions
    for i in range(10):
        create_transaction(client, name=f"Transaction {i+1}", amount=100.0 * (i+1))

    # Test pagination with an invalid page number (e.g., page 0)
    response = client.get("/transactions/?page_size=5&page=3")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data["items"]) == 0  # Should return an empty list since page 3 does not exist
    assert data["page"] == 3  # Invalid page number
    assert data["page_size"] == 5  # Page size is 5
    assert data["total_items"] == 10  # Total transactions created
    assert data["total_pages"] == 2  # Total pages should be 2
    assert data["has_next"] == False  # There should be no more transactions to fetch
    assert data["has_previous"] == True  # This is not the first page, so there should be a previous page