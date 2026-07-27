import { useState } from "react";

import type { Transaction } from "./types/transactions";

import TransactionList from "./components/TransactionList";
import CreateTransactionForm from "./components/CreateTransactionForm";

function App() {
  const [refreshVersion, setRefreshVersion] = useState(0);

  function handleCreatedTransaction(_transaction: Transaction) {
    setRefreshVersion((currentVersion) => currentVersion + 1);
  }

  return (
    <main>
      <h1>Finance Tracker</h1>

      <CreateTransactionForm
        onTransactionCreated={handleCreatedTransaction}
      />

      <TransactionList refreshVersion={refreshVersion} />
    </main>
  );
}

export default App;