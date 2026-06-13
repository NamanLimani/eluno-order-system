
#  Eluno AI Order Management Engine

**Candidate:** Naman Limani

**Role:** AI Product Engineer Assessment

##  Live Cloud Deployment

This architecture is fully containerized and deployed to the cloud via Render and Supabase.

* **Frontend Operations Dashboard:** [https://eluno-dashboard.onrender.com](https://eluno-dashboard.onrender.com)
* **Backend API Swagger Docs:** [https://eluno-backend-api.onrender.com/docs](https://www.google.com/search?q=https://eluno-backend-api.onrender.com/docs)

>  **Reviewer Note:** This application is hosted on Render's free tier. If the service has been inactive for 15 minutes, the containers spin down to conserve resources. **Please allow 45-60 seconds for a "cold boot"** when first clicking the links above. Thank you for your patience!

---

##  Project Overview

The Eluno Order Management Engine is a decoupled, microservice-style architecture built to manage eyewear fulfillment. It handles intelligent inventory routing, human-in-the-loop operations monitoring, and predictive Machine Learning alerts to prevent Service Level Agreement (SLA) breaches.

### Core Modules Implemented

1. **Module 1 (Intake & Routing):** A deterministic, rule-based engine that checks incoming prescriptions against live warehouse inventory to flag orders as "In-House Fast Track" or "External Processing."
2. **Module 2 (Operations Dashboard):** A decoupled Streamlit UI allowing warehouse managers to filter active orders, update operational statuses, and log text-based delay reasons.
3. **Module 3 (AI SLA Prediction):** An XGBoost machine learning model running as an asynchronous FastAPI Background Task. It evaluates order features (lens type, coatings, stage, time elapsed) and triggers an automated SMTP Email Alert to management if the probability of an SLA breach exceeds 80%.

---

##  Technology Stack

* **Backend:** FastAPI, Python 3.11, Pydantic, SQLAlchemy
* **Frontend:** Streamlit, Pandas, Requests
* **Database:** PostgreSQL (Supabase) leveraging `JSONB` for flexible prescription storage
* **Machine Learning:** XGBoost, Scikit-Learn, Joblib
* **Infrastructure:** Docker, Docker Compose

---

##  Repository Structure & File Blueprint

```text
eluno_order_system/
├── docker-compose.yml       # Orchestrates local deployment of FastAPI, Streamlit, and Postgres
├── architecture_note.md     # 1-page defense of technical choices and stack selection
│
├── backend/                 # 🧠 Module 1 & 3: FastAPI Logic & API Endpoints
│   ├── Dockerfile           # Builds the isolated Linux container for the backend
│   ├── requirements.txt     # Backend-specific dependencies (FastAPI, XGBoost, SQLAlchemy)
│   ├── main.py              # Application entry point; registers routers
│   ├── database.py          # PostgreSQL connection pool and SQLAlchemy ORM setup
│   ├── schemas.py           # Pydantic models for strict API request/response validation
│   ├── routers/
│   │   ├── orders.py        # Endpoints for order creation and status updates
│   │   └── inventory.py     # Endpoints for the warehouse team to manage physical stock
│   └── services/
│       └── alerts.py        # Asynchronous background service for ML prediction and Email alerts
│
├── frontend/                # 🖥️ Module 2: Streamlit Operations UI
│   ├── Dockerfile           # Builds the isolated Linux container for the frontend
│   ├── requirements.txt     # Frontend-specific dependencies (Streamlit, Pandas)
│   ├── app.py               # Main dashboard UI and patience warning implementation
│   ├── api_client.py        # Decoupled HTTP requests fetching data from FastAPI
│   └── components/
│       ├── order_table.py   # Renders the filterable Pandas dataframe UI
│       └── status_form.py   # Renders the update form and triggers backend PUT requests
│
└── mlops/                   # 🤖 Model Training & Pipeline Infrastructure
    ├── requirements.txt     # Data Science dependencies for local training
    ├── run_pipeline.py      # Entry point to execute the full model training lifecycle
    ├── data/
    │   └── generate_mock_orders.py  # Synthesizes 1,000 realistic historical orders with SLA logic
    ├── pipelines/
    │   └── training_pipeline.py     # ZenML-ready orchestrator that chains ML steps together
    └── steps/
        ├── ingest_data.py   # Safely loads the CSV data
        ├── train_xgboost.py # Performs One-Hot Encoding and trains the XGBoost Classifier
        └── evaluate_model.py# Calculates accuracy and prints classification reports

```

---

##  Local Development Setup

If you wish to run this architecture locally rather than using the cloud links, follow these steps.

### 1. Prerequisites

* [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running.
* Git installed.

### 2. Environment Variables

Create a file named `.env` in the root directory. You must supply your own database and email credentials to run the alerting system locally:

```env
# Database (Use a local Postgres URI or Supabase IPv4 Pooler)
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/eluno_db

# Email Alert Configuration (Gmail App Passwords recommended)
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_16_character_app_password
EMAIL_RECEIVER=warehouse_manager_email@example.com

```

### 3. Build and Run via Docker

Open your terminal in the project root and run:

```bash
docker-compose up --build -d

```

* **Backend API Docs:** `http://localhost:8000/docs`
* **Frontend Dashboard:** `http://localhost:8501`

---

##  How to Test the Application

1. **Seed the Inventory (Module 1):** Go to the Backend API Docs and use the `POST /inventory/` endpoint to add a physical lens to the warehouse.
2. **Create an Order (Module 1):** Use the `POST /orders/` endpoint. If the requested lens matches your inventory, it will route to "In-House". Otherwise, it routes to "External Processing".
3. **Monitor & Update (Module 2):** Open the Frontend Dashboard to view the live order. Use the UI to change the status (e.g., to "QC Failed") and log a delay reason.
4. **Trigger the AI Alert (Module 3):** When you click "Update Order" in the UI, the FastAPI backend evaluates the time elapsed against the XGBoost model. *Note: For demonstration purposes, the codebase artificially injects an 80-hour time penalty during the update to guarantee the AI predicts an SLA breach and fires the Email alert.*

---

*Developed by Naman Limani for Eluno.*