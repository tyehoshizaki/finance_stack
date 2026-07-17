# Test main.py route

def test_main_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Finance Tracker API"}