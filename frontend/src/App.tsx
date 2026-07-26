import { useCallback, useEffect, useState } from "react";

import { 
  getTransactions,
  updateTransaction,
  deleteTransaction,
 } from "./api/transactions";

import type { 
  Transaction,
  TransactionSort,
  TransactionSortOrder,
  TransactionUpdate,
 } from "./types/transactions";
 
import TransactionCard from "./components/TransactionCard";
import CreateTransactionForm from "./components/CreateTransactionForm";

function App() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);

  const [sortBy, setSortBy] = useState<TransactionSort>({ sort_by: "transaction_date" });
  const [sortOrder, setSortOrder] = useState<TransactionSortOrder>({ sort_order: "desc" });

  const [totalPages, setTotalPages] = useState(1);
  const [hasNext, setHasNext] = useState(false);
  const [hasPrevious, setHasPrevious] = useState(false);
  const [pageSize, setPageSize] = useState(10);

  const loadTransactions = useCallback(async () => {

    console.log("1. loadTransactions started");

    try {
      console.log("2. About to call getTransactions", page, pageSize);

      const data = await getTransactions(page, pageSize, sortBy, sortOrder);

      setTransactions(data.items);
      setTotalPages(data.total_pages);
      setHasNext(data.has_next);
      setHasPrevious(data.has_previous);

      console.log("3. Transactions loaded successfully", data.items);

    } catch (error) {

      console.error("Error fetching transactions:", error);

      if (error instanceof Error) {
        setError(error.message);

      } else {
        setError("Something went wrong");

      }
    } finally {
      setLoading(false);
      
    }
  }, [page, pageSize, sortBy, sortOrder]);

  async function handleCreatedTransaction(_transaction: Transaction) {
    await loadTransactions();
  }

  async function handleUpdateTransaction(
    transactionId: number,
    updatedTransaction: TransactionUpdate,
  ) {
    try {
      await updateTransaction(transactionId, updatedTransaction);
      await loadTransactions();
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("Something went wrong");
      }
    }
  }

  async function handleDeletedTransaction(transactionId: number) {
    try {
      await deleteTransaction(transactionId);
      await loadTransactions();
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("Something went wrong");
      }
    }
  }

  useEffect(() => {
    loadTransactions();
  }, [loadTransactions]);

  if (loading) {
    return <p>Loading transactions...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  return (
    <main>
      <h1>Finance Tracker</h1>

      <CreateTransactionForm onTransactionCreated={handleCreatedTransaction} />

      <h2>Transactions</h2>

      <div>
        <select
        value={sortBy.sort_by}
        onChange={(event) => {
          setSortBy({ sort_by: event.target.value as TransactionSort["sort_by"] });
        }}
      >
        <option value="transaction_date">Date</option>
        <option value="name">Name</option>
        <option value="amount">Amount</option>
        <option value="category">Category</option>
        <option value="transaction_type">Type</option>
      </select>
      </div>

      <div>
        <select
          value={sortOrder.sort_order}
          onChange={(event) => {
            setSortOrder({ sort_order: event.target.value as TransactionSortOrder["sort_order"] });
          }}
        >
          <option value="asc">Ascending</option>
          <option value="desc">Descending</option>
        </select>
      </div>

      {transactions.map((transaction) => (
        <TransactionCard 
        key={transaction.id}
        transaction={transaction}
        onUpdate={handleUpdateTransaction}
        onDelete={handleDeletedTransaction}
         />
      ))}

      <div>
        <select
          value={pageSize}
          onChange={(event) => {
            setPageSize(Number(event.target.value));
            setPage(1);
          }}
        >
          <option value="10">10 per page</option>
          <option value="25">25 per page</option>
          <option value="50">50 per page</option>
          <option value="100">100 per page</option>
        </select>

        <button
          onClick={() => setPage((currentPage) => currentPage - 1)}
          disabled={!hasPrevious}
        >
          Previous
        </button>

        <span>
          Page {page} of {totalPages}
        </span>

        <button
          onClick={() => setPage((currentPage) => currentPage + 1)}
          disabled={!hasNext}
        >
          Next
        </button>
      </div>
    </main>
  );
}

export default App;
