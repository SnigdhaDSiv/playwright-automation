document.getElementById("userForm").addEventListener("submit", (event) => {
  event.preventDefault();

  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const accountType = document.getElementById("accountType").value;

  const messageDiv = document.getElementById("message");
  messageDiv.classList.add("hidden");

  // Simple front-end validation
  if (!name || !email || !accountType) {
    showMessage("All fields are required!", "error");
    return;
  }

  // Simulate async request (mock)
  setTimeout(() => {
  
    if (email.endsWith("@example.com")) {
      showMessage("User created successfully!", "success");
      document.getElementById("userForm").reset();
    } else {
      showMessage("Invalid email domain. Use @example.com.", "error");
    }
  }, 800);
});

function showMessage(message, type) {
  const messageDiv = document.getElementById("message");
  messageDiv.textContent = message;
  messageDiv.className = type;
}
