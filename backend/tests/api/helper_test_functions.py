def create_transaction(
    client,
    *,
    name="Coffee",
    amount=50000,
    category="food",
    transaction_type="expense",
    description="Default description",
    transaction_date="2026-07-12",
):
    response = client.post(
        "/transactions/",
        json={
            "name": name,
            "amount": amount,
            "category": category,
            "transaction_type": transaction_type,
            "description": description,
            "transaction_date": transaction_date,
        },
    )

    assert response.status_code == 201

    return response.json()