import { useState, type SubmitEvent } from "react";

import { createTransaction } from "../api/transactions";
import type {
  Transaction,
  TransactionType,
} from "../types/transactions";

interface CreateTransactionFormProps {
  onTransactionCreated: (transaction: Transaction) => void;
}

function CreateTransactionForm({
  onTransactionCreated,
}: CreateTransactionFormProps) {
  const [name, setName] = useState("");
  const [amount, setAmount] = useState("");
  const [category, setCategory] = useState("");
  const [transactionType, setTransactionType] = useState<TransactionType>("expense");
  const [description, setDescription] = useState("");
  const [merchant, setMerchant] = useState("");
  const [transactionDate, setTransactionDate] = useState(() => new Date().toISOString().split("T")[0]);

  async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault();

    const newTransaction = await createTransaction({
      name: name,
      amount: Number(amount),
      category: category,
      transaction_type: transactionType,
      description: description || null,
      transaction_date: transactionDate,
      merchant: merchant || null,
    });

    onTransactionCreated(newTransaction);
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Create Transaction</h2>

      <input
        type="text"
        placeholder="Name"
        value={name}
        onChange={(event) => setName(event.target.value)}
      />

      <input
        type="number"
        placeholder="Amount"
        value={amount}
        onChange={(event) => setAmount(event.target.value)}
      />

      <input
        type="text"
        placeholder="Category"
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
        placeholder="Description"
        value={description}
        onChange={(event) => setDescription(event.target.value)}
      />

      <input
        type="text"
        placeholder="Merchant"
        value={merchant}
        onChange={(event) => setMerchant(event.target.value)}
      />

      <button type="submit">Create Transaction</button>
    </form>
  );
}

export default CreateTransactionForm;