<div align="center">

# 🏠 House Price Prediction

**A full-stack Machine Learning web application that predicts house prices using a tuned Random Forest model.**

Built with Flask · scikit-learn · HTML/CSS/JS

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1+-000000?style=flat&logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4+-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

</div>

---

## Overview

This project provides an end-to-end ML pipeline — from exploratory data analysis to a deployed web dashboard — for predicting residential property prices in King County, USA.

Users enter property details (bedrooms, sqft, condition, etc.) into a dashboard interface and receive an instant price prediction from a trained Random Forest model.

## Features

- **Dashboard UI** — Dark-themed, responsive interface with real-time predictions
- **REST API** — Flask backend with health check, schema, and prediction endpoints
- **ML Pipeline** — Full training pipeline in Jupyter notebooks with EDA, preprocessing, and hyperparameter tuning
- **19 Features** — Including engineered features like `house_age`, `was_renovated`, and `total_rooms`

## Tech Stack

| Layer     | Technology                              |
|-----------|-----------------------------------------|
| Frontend  | HTML5, CSS3, JavaScript                 |
| Backend   | Python, Flask, Flask-CORS               |
| ML        | scikit-learn (Random Forest Regressor)  |
| Data      | pandas, NumPy, Matplotlib, Seaborn      |
| Notebooks | Jupyter Notebook                        |

## Project Structure

```
house-price-prediction/
│
├── frontend/                           # Client-side application
│   ├── index.html                      # Dashboard UI
│   ├── style.css                       # Styling (dark theme)
│   └── script.js                       # API integration & form logic
│
├── backend/                            # Server-side application
│   ├── app.py                          # Flask API server
│   └── model/                          # ML artifacts (generated)
│       ├── model.pkl
│       ├── scaler.pkl
│       └── feature_columns.json
│
├── notebook/                           # Jupyter notebooks
│   ├── EDA_and_Preprocessing.ipynb     # Data analysis & cleaning
│   └── Model_Training_and_Export.ipynb # Model training & export
│
├── data/
│   ├── dataset.csv                     # Raw dataset (21,613 records)
│   └── cleaned_dataset.csv            # Preprocessed dataset (generated)
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/Pratham-bit800/house-price-prediction.git
cd house-price-prediction
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Train the model**

Run the notebooks in order to generate the ML artifacts:

```bash
jupyter nbconvert --to notebook --execute notebook/EDA_and_Preprocessing.ipynb
jupyter nbconvert --to notebook --execute notebook/Model_Training_and_Export.ipynb
```

Or open them manually in Jupyter Notebook:

```bash
jupyter notebook
```

Then run `EDA_and_Preprocessing.ipynb` first, followed by `Model_Training_and_Export.ipynb` (**Cell → Run All**).

**4. Start the application**

```bash
python backend/app.py
```

**5. Open in browser**

```
http://127.0.0.1:5000
```

## API Reference

### `GET /`

Returns the dashboard UI.

### `GET /api/health`

Health check endpoint.

```json
{
  "status": "ok",
  "model": "Random Forest (Tuned)"
}
```

### `GET /api/features`

Returns the input field schema with types, ranges, and defaults.

### `POST /api/predict`

Predicts house price from property features.

**Request Body:**

```json
{
  "bedrooms": 3,
  "bathrooms": 2,
  "sqft_living": 2000,
  "sqft_lot": 5000,
  "floors": 1,
  "waterfront": 0,
  "view": 0,
  "condition": 3,
  "grade": 7,
  "sqft_above": 1500,
  "sqft_basement": 0,
  "sqft_living15": 1800,
  "sqft_lot15": 5000,
  "yr_built": 2000,
  "yr_renovated": 0,
  "sale_year": 2015,
  "sale_month": 6
}
```

**Response:**

```json
{
  "predicted_price": 613878.5,
  "formatted_price": "$613,878.50",
  "model": "Random Forest (Tuned)",
  "features_used": 19
}
```

## Model Performance

Trained and evaluated on the King County House Sales dataset (21,613 records).

| Model                    | R² Score |
|--------------------------|----------|
| Random Forest (Tuned) ⭐ | 0.8495   |
| Random Forest            | 0.8464   |
| KNN                      | 0.7680   |
| Decision Tree            | 0.7170   |
| Linear Regression        | 0.6972   |
| SVR                      | -0.0633  |

## Dataset

[King County House Sales — Kaggle](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction)

21,613 house sale records from King County, Washington (2014–2015) with 21 features including price, square footage, bedrooms, bathrooms, condition, grade, and more.

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

**Pratham Sindkar** — [@Pratham-bit800](https://github.com/Pratham-bit800)

---

<div align="center">
If you found this project useful, consider giving it a ⭐
</div>