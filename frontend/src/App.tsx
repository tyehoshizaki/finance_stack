import { useCallback, useEffect, useState } from "react";

import { 
  getTransactions,
  updateTransaction,
  deleteTransaction,
 } from "./api/transactions";
import type { 
  Transaction,
  TransactionUpdate,
 } from "./types/transactions";
import TransactionCard from "./components/TransactionCard";
import CreateTransactionForm from "./components/CreateTransactionForm";

function App() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [hasNext, setHasNext] = useState(false);
  const [hasPrevious, setHasPrevious] = useState(false);
  const [pageSize, setPageSize] = useState(10);

  const loadTransactions = useCallback(async () => {
    try {
      const data = await getTransactions(page, pageSize);
      setTransactions(data.items);
      setTotalPages(data.total_pages);
      setHasNext(data.has_next);
      setHasPrevious(data.has_previous);
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("Something went wrong");
      }
    } finally {
      setLoading(false);
    }
  }, [page, pageSize]);

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
