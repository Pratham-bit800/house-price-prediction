/**
 * script.js — HousePriceAI Dashboard Logic
 */

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------
const API_BASE_URL = "/api";

// ---------------------------------------------------------------------------
// DOM Elements
// ---------------------------------------------------------------------------
const form = document.getElementById("prediction-form");
const predictBtn = document.getElementById("predict-btn");
const resultCard = document.getElementById("result-card");
const priceAmount = document.getElementById("price-amount");
const errorCard = document.getElementById("error-card");
const errorMessage = document.getElementById("error-message");
const sidebar = document.getElementById("sidebar");
const menuToggle = document.getElementById("menu-toggle");

// ---------------------------------------------------------------------------
// Mobile Sidebar Toggle
// ---------------------------------------------------------------------------
if (menuToggle) {
  menuToggle.addEventListener("click", () => {
    sidebar.classList.toggle("open");
  });

  // Close sidebar when clicking outside on mobile
  document.addEventListener("click", (e) => {
    if (
      sidebar.classList.contains("open") &&
      !sidebar.contains(e.target) &&
      !menuToggle.contains(e.target)
    ) {
      sidebar.classList.remove("open");
    }
  });
}

// ---------------------------------------------------------------------------
// Form Submission
// ---------------------------------------------------------------------------
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  hideError();
  resetResult();

  const formData = collectFormData();
  const validationError = validateInput(formData);
  if (validationError) {
    showError(validationError);
    return;
  }

  setLoading(true);

  try {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || `Server error (${response.status})`);
    }

    showResult(data);
  } catch (error) {
    if (
      error.message.includes("Failed to fetch") ||
      error.message.includes("NetworkError")
    ) {
      showError("Cannot connect to the API. Make sure the Flask server is running.");
    } else {
      showError(error.message);
    }
  } finally {
    setLoading(false);
  }
});

// ---------------------------------------------------------------------------
// Collect Form Data
// ---------------------------------------------------------------------------
function collectFormData() {
  const fields = [
    "bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors",
    "waterfront", "view", "condition", "grade",
    "sqft_above", "sqft_basement",
    "sqft_living15", "sqft_lot15",
    "yr_built", "yr_renovated", "sale_year", "sale_month",
  ];

  const data = {};
  fields.forEach((field) => {
    const el = document.getElementById(field);
    if (el) data[field] = parseFloat(el.value);
  });
  return data;
}

// ---------------------------------------------------------------------------
// Validation
// ---------------------------------------------------------------------------
function validateInput(data) {
  for (const [key, value] of Object.entries(data)) {
    if (isNaN(value)) return `Invalid value for "${key}". Enter a valid number.`;
  }
  if (data.bedrooms < 0 || data.bedrooms > 33) return "Bedrooms must be 0-33.";
  if (data.sqft_living < 200) return "Living area must be at least 200 sqft.";
  if (data.grade < 1 || data.grade > 13) return "Grade must be 1-13.";
  if (data.condition < 1 || data.condition > 5) return "Condition must be 1-5.";
  if (data.sale_month < 1 || data.sale_month > 12) return "Month must be 1-12.";
  if (data.yr_built < 1900) return "Year built must be 1900 or later.";
  return null;
}

// ---------------------------------------------------------------------------
// Result Display
// ---------------------------------------------------------------------------
function showResult(data) {
  priceAmount.textContent = data.formatted_price;
  priceAmount.classList.add("active");
  resultCard.classList.add("has-result");

  // Scroll result into view on mobile
  setTimeout(() => {
    resultCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }, 150);
}

function resetResult() {
  priceAmount.textContent = "--.--";
  priceAmount.classList.remove("active");
  resultCard.classList.remove("has-result");
}

// ---------------------------------------------------------------------------
// Error Display
// ---------------------------------------------------------------------------
function showError(msg) {
  errorMessage.textContent = msg;
  errorCard.classList.remove("hidden");
  setTimeout(() => {
    errorCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }, 100);
}

function hideError() {
  errorCard.classList.add("hidden");
}

// ---------------------------------------------------------------------------
// Loading State
// ---------------------------------------------------------------------------
function setLoading(isLoading) {
  if (isLoading) {
    predictBtn.classList.add("loading");
    predictBtn.disabled = true;
  } else {
    predictBtn.classList.remove("loading");
    predictBtn.disabled = false;
  }
}
