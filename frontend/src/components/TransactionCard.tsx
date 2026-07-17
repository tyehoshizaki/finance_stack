import { useState, type SubmitEvent } from "react";

import type {
  Transaction,
  TransactionType,
  TransactionUpdate,
} from "../types/transactions";
import "./TransactionCard.css";

interface TransactionCardProps {
  transaction: Transaction;

  onUpdate: (
    transactionId: number,
    updatedTransaction: TransactionUpdate,
  ) => Promise<void>;

  onDelete: (transactionId: number) => void;
}

function TransactionCard({
  transaction,
  onUpdate,
  onDelete,
}: TransactionCardProps) {
  const [isEditing, setIsEditing] = useState(false);

  const [name, setName] = useState(transaction.name);
  const [amount, setAmount] = useState(String(transaction.amount));
  const [category, setCategory] = useState(transaction.category);
  const [transactionType, setTransactionType] = useState<TransactionType>(transaction.transaction_type);
  const [description, setDescription] = useState(transaction.description ?? "");
  const [transactionDate, setTransactionDate] = useState(transaction.transaction_date);
  const [merchant, setMerchant] = useState(transaction.merchant ?? "");

  const amountClass =
    transaction.transaction_type === "income"
      ? "transaction-amount income"
      : transaction.transaction_type === "expense"
        ? "transaction-amount expense"
        : "transaction-amount transfer";

  function handleEditClick() {
    setName(transaction.name);
    setAmount(String(transaction.amount));
    setCategory(transaction.category);
    setTransactionType(transaction.transaction_type);
    setDescription(transaction.description ?? "");
    setTransactionDate(transaction.transaction_date);
    setMerchant(transaction.merchant ?? "");

    setIsEditing(true);
  }

  function handleDeleteClick() {
    const confirmDelete = window.confirm(
      `Are you sure you want to delete this transaction? (${transaction.name})`,
    );
    if (confirmDelete) {
      onDelete(transaction.id);
    }
  }

  async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault();

    await onUpdate(transaction.id, {
      name,
      amount: Number(amount),
      category,
      transaction_type: transactionType,
      description: description || null,
      transaction_date: transactionDate,
      merchant: merchant || null,
    });

    setIsEditing(false);
  }

  if (isEditing) {
    return (
      <form className="transaction-card" onSubmit={handleSubmit}>
        <input
          type="text"
          value={name}
          onChange={(event) => setName(event.target.value)}
        />

        <input
          type="number"
          value={amount}
          onChange={(event) => setAmount(event.target.value)}
        />

        <input
          type="text"
          value={category}
          onChange={(event) => setCategory(event.target.value)}
        />

        <select
          value={transactionType}
          onChange={(event) =>
            setTransactionType(event.target.value as TransactionType)
          }
        >
          <option value="expense">Expense</option>
          <option value="income">Income</option>
          <option value="transfer">Transfer</option>
        </select>

        <input
          type="date"
          value={transactionDate}
          onChange={(event) => setTransactionDate(event.target.value)}
        />

        <input
          type="text"
          value={description}
          placeholder="Description"
          onChange={(event) => setDescription(event.target.value)}
        />

        <input
          type="text"
          value={merchant}
          placeholder="Merchant"
          onChange={(event) => setMerchant(event.target.value)}
        />

        <button type="submit">Save</button>

        <button type="button" onClick={() => setIsEditing(false)}>
          Cancel
        </button>
      </form>
    );
  }

  return (
    <div className="transaction-card">
      <div className="transaction-info">
        <h2>{transaction.name}</h2>
        <p>{transaction.category}</p>
        <p>{transaction.transaction_date}</p>
      </div>

      <p className={amountClass}>{transaction.amount}</p>
      <button onClick={handleEditClick}>Edit</button>
      <button onClick={handleDeleteClick}>Delete</button>
    </div>
  );
}

export default TransactionCard;
