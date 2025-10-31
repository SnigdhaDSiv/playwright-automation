document.getElementById("transactionForm").addEventListener("submit", (event) => {
    event.preventDefault();

    const userId = document.getElementById("userId").value.trim();
    const recipientId = document.getElementById("recipientId").value.trim();
    const amount = parseFloat(document.getElementById("amount").value);
    const type = document.getElementById("type").value;
    const messageDiv = document.getElementById("message");

    messageDiv.classList.add("hidden");

    // Basic validation
   /* if (!userId || !recipientId || !amount || amount <= 0) {
      showMessage("All fields are required and amount must be positive!", "error");
      return;
    }*/

    // Simulated API call (mock backend)
    setTimeout(() => {
       if (!userId || !recipientId || !amount || amount <= 0) {
      showMessage("All fields are required and amount must be positive!", "error");
      return;
    }

      if (userId === recipientId)
         {
        showMessage("Cannot transfer to the same user!", "error");
        return;
      }

      if (amount > 10000) {
        showMessage("Amount exceeds transfer limit!", "error");
        return;
      }

      showMessage(
        `Transaction created successfully! [User: ${userId} → Recipient: ${recipientId}, $${amount.toFixed(2)}]`,
        "success"
      );
      document.getElementById("transactionForm").reset();
    }, 800);
  });

  function showMessage(message, type) {
    const messageDiv = document.getElementById("message");
    messageDiv.textContent = message;
    messageDiv.className = type; // reset classes
    messageDiv.classList.remove("hidden"); // make it visible
  }