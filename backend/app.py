"""
app.py - Flask API for House Price Prediction

Loads the trained Random Forest model and serves predictions
via a REST API. Feature engineering is handled server-side so
the frontend only needs to send raw property details.

Usage:
    cd backend/
    python app.py
"""

import os
import json

import numpy as np
import pandas as pd
import joblib
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# ---------------------------------------------------------------------------
# App Setup
# ---------------------------------------------------------------------------
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
app = Flask(__name__, static_folder=FRONTEND_DIR)
CORS(app)

# ---------------------------------------------------------------------------
# Load Model Artifacts
# ---------------------------------------------------------------------------
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")

model = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))

with open(os.path.join(MODEL_DIR, "feature_columns.json"), "r") as f:
    feature_columns = json.load(f)

print(f"Model loaded. Expected features ({len(feature_columns)}): {feature_columns}")


# ---------------------------------------------------------------------------
# Input Schema — what the frontend sends
# ---------------------------------------------------------------------------
INPUT_SCHEMA = {
    "bedrooms":       {"type": "int",   "min": 0,    "max": 33,      "default": 3,      "label": "Bedrooms"},
    "bathrooms":      {"type": "float", "min": 0,    "max": 8,       "default": 2.0,    "label": "Bathrooms"},
    "sqft_living":    {"type": "int",   "min": 200,  "max": 14000,   "default": 2000,   "label": "Living Area (sqft)"},
    "sqft_lot":       {"type": "int",   "min": 500,  "max": 1700000, "default": 5000,   "label": "Lot Size (sqft)"},
    "floors":         {"type": "float", "min": 1,    "max": 3.5,     "default": 1.0,    "label": "Floors"},
    "waterfront":     {"type": "int",   "min": 0,    "max": 1,       "default": 0,      "label": "Waterfront"},
    "view":           {"type": "int",   "min": 0,    "max": 4,       "default": 0,      "label": "View Rating"},
    "condition":      {"type": "int",   "min": 1,    "max": 5,       "default": 3,      "label": "Condition"},
    "grade":          {"type": "int",   "min": 1,    "max": 13,      "default": 7,      "label": "Grade"},
    "sqft_above":     {"type": "int",   "min": 200,  "max": 10000,   "default": 1500,   "label": "Above Ground (sqft)"},
    "sqft_basement":  {"type": "int",   "min": 0,    "max": 5000,    "default": 0,      "label": "Basement (sqft)"},
    "sqft_living15":  {"type": "int",   "min": 300,  "max": 7000,    "default": 1800,   "label": "Neighbor Living Area (sqft)"},
    "sqft_lot15":     {"type": "int",   "min": 600,  "max": 900000,  "default": 5000,   "label": "Neighbor Lot Size (sqft)"},
    "yr_built":       {"type": "int",   "min": 1900, "max": 2015,    "default": 2000,   "label": "Year Built"},
    "yr_renovated":   {"type": "int",   "min": 0,    "max": 2015,    "default": 0,      "label": "Year Renovated (0 = never)"},
    "sale_year":      {"type": "int",   "min": 2014, "max": 2026,    "default": 2015,   "label": "Sale Year"},
    "sale_month":     {"type": "int",   "min": 1,    "max": 12,      "default": 6,      "label": "Sale Month"},
}


# ---------------------------------------------------------------------------
# Helper: Compute engineered features
# ---------------------------------------------------------------------------
def compute_engineered_features(data):
    """
    Compute the same derived features used during training:
    - house_age
    - was_renovated
    - years_since_renovation
    - total_rooms
    """
    data["house_age"] = data["sale_year"] - data["yr_built"]
    data["was_renovated"] = int(data["yr_renovated"] > 0)
    data["years_since_renovation"] = (
        data["sale_year"] - data["yr_renovated"]
        if data["was_renovated"] == 1
        else data["house_age"]
    )
    data["total_rooms"] = data["bedrooms"] + data["bathrooms"]
    return data


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def home():
    """Serve the frontend."""
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:filename>")
def serve_static(filename):
    """Serve frontend static files (CSS, JS)."""
    return send_from_directory(FRONTEND_DIR, filename)


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "model": "Random Forest (Tuned)"})


@app.route("/api/features", methods=["GET"])
def get_features():
    """Return the input schema so the frontend can build the form dynamically."""
    return jsonify(INPUT_SCHEMA)


@app.route("/api/predict", methods=["POST"])
def predict():
    """
    Predict house price from raw property features.

    Expects JSON body with raw house features (see INPUT_SCHEMA).
    Computes engineered features server-side, scales, and returns prediction.
    """
    try:
        body = request.get_json()

        if not body:
            return jsonify({"error": "Request body is empty. Send JSON with house features."}), 400

        # Validate and extract input features
        input_data = {}
        missing = []
        for field, meta in INPUT_SCHEMA.items():
            if field not in body:
                missing.append(field)
            else:
                value = body[field]
                # Type conversion
                if meta["type"] == "int":
                    input_data[field] = int(value)
                else:
                    input_data[field] = float(value)

        if missing:
            return jsonify({"error": f"Missing required fields: {missing}"}), 400

        # Compute engineered features
        input_data = compute_engineered_features(input_data)

        # Remove raw fields not in the model's feature list
        for field in ["yr_built", "yr_renovated"]:
            if field in input_data and field not in feature_columns:
                del input_data[field]

        # Build DataFrame in the exact column order the model expects
        input_df = pd.DataFrame([input_data])[feature_columns]

        # Scale and predict
        input_scaled = scaler.transform(input_df)
        predicted_price = model.predict(input_scaled)[0]

        return jsonify({
            "predicted_price": round(float(predicted_price), 2),
            "formatted_price": f"${predicted_price:,.2f}",
            "model": "Random Forest (Tuned)",
            "features_used": len(feature_columns),
        })

    except ValueError as e:
        return jsonify({"error": f"Invalid input value: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("\nStarting House Price Prediction API...")
    print("Endpoints:")
    print("  GET  /api/health   - Health check")
    print("  GET  /api/features - Input schema")
    print("  POST /api/predict  - Predict house price")
    print()
    app.run(debug=True, port=5000)
