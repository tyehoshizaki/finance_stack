export type TransactionType = "income" | "expense" | "transfer";

export interface Transaction {
    id: number;
    name: string;
    amount: number;
    category: string;
    transaction_type: TransactionType;
    description: string | null;
    transaction_date: string;
    created_at: string;
    last_updated: string | null;
    merchant: string | null;
}

export interface PaginatedTransactionsResponse {
    items: Transaction[];
    page: number;
    page_size: number;
    total_items: number;
    total_pages: number;
    has_next: boolean;
    has_previous: boolean;
}

export interface TransactionSort {
    sort_by: "name" | "amount" | "category" | "transaction_type" | "transaction_date";
}

export interface TransactionSortOrder {
    sort_order: "asc" | "desc";
}

export interface TransactionCreate {
    name: string;
    amount: number;
    category: string;
    transaction_type: TransactionType;
    description: string | null;
    transaction_date: string;
    merchant: string | null;
}

export interface TransactionUpdate {
    name?: string;
    amount?: number;
    category?: string;
    transaction_type?: TransactionType;
    description?: string | null;
    transaction_date?: string;
    merchant?: string | null;
}


