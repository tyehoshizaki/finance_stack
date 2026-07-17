import type { 
    Transaction,
    TransactionCreate,
    PaginatedTransactionsResponse,
    TransactionUpdate
 } from "../types/transactions";

const API_URL = "http://localhost:8000";

export async function getTransactions(
    page: number = 1,
    pageSize: number = 10
): Promise<PaginatedTransactionsResponse> {
    const response = await fetch(
        `${API_URL}/transactions/?page=${page}&page_size=${pageSize}`
    );

    if (!response.ok) {
        throw new Error(`Error fetching transactions: ${response.statusText}`);
    }

    const data: PaginatedTransactionsResponse = await response.json();
    return data;
}

export async function createTransaction(
    transaction: TransactionCreate
): Promise<Transaction> {
    const response = await fetch(`${API_URL}/transactions/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(transaction),
    });

    if (!response.ok) {
        throw new Error(`Error creating transaction: ${response.statusText}`);
    }

    const data: Transaction = await response.json();
    return data;
}

export async function updateTransaction(
    transactionId: number,
    updatedTransaction: TransactionUpdate
): Promise<Transaction> {
    const response = await fetch(`${API_URL}/transactions/${transactionId}/`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedTransaction),
    });

    if (!response.ok) {
        throw new Error(`Error updating transaction: ${response.statusText}`);
    }

    const data: Transaction = await response.json();
    return data;
}

export async function deleteTransaction(
    transactionId: number
): Promise<void> {
    const response = await fetch(`${API_URL}/transactions/${transactionId}/`, {
        method: "DELETE",
    });

    if (!response.ok) {
        throw new Error(`Error deleting transaction: ${response.statusText}`);
    }
}
