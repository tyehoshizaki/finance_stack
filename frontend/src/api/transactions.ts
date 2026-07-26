import type {
  Transaction,
  PaginatedTransactionsResponse,
  TransactionSort,
  TransactionSortOrder,
  TransactionCreate,
  TransactionUpdate,
} from "../types/transactions";

const API_URL = "/api";

export async function getTransactions(
  page: number = 1,
  pageSize: number = 10,
  sortBy: TransactionSort,
  sortOrder: TransactionSortOrder,
): Promise<PaginatedTransactionsResponse> {

  const params = new URLSearchParams({
    page: page.toString(),
    page_size: pageSize.toString(),
    sort_by: sortBy.sort_by,
    sort_order: sortOrder.sort_order,
  });

  const url = `${API_URL}/transactions/?${params.toString()}`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Error fetching transactions: ${response.statusText}`);
  }

  const data: PaginatedTransactionsResponse = await response.json();
  return data;
}

export async function createTransaction(
  transaction: TransactionCreate,
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
  updatedTransaction: TransactionUpdate,
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

export async function deleteTransaction(transactionId: number): Promise<void> {
  const response = await fetch(`${API_URL}/transactions/${transactionId}/`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error(`Error deleting transaction: ${response.statusText}`);
  }
}
