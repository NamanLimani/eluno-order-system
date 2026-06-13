# Eluno AI Order Management Engine - Architecture Note
**Candidate:** Naman Limani
**Role:** AI Product Engineer

## 1. System Overview
The Eluno Order Management Engine is a decoupled, microservice-style architecture designed to handle eyewear order routing, inventory tracking, operations monitoring, and AI-driven Service Level Agreement (SLA) breach predictions. 

**Live Demo URLs:**
* **Frontend Dashboard:** https://eluno-dashboard.onrender.com
* **Backend API Docs:** https://eluno-backend-api.onrender.com/docs
> *⚠️ Note on Deployment: This application is hosted on Render's free tier. If the service has been inactive for 15 minutes, the containers spin down. Please allow 45-60 seconds for a "cold boot" when first clicking the links. Thank you for your patience!*

---

## 2. Core Technology Stack & Trade-off Analysis

### Backend: FastAPI
* **The Choice:** FastAPI
* **The Alternatives Rejected:** Flask, Django
* **Justification:** FastAPI was selected for its native asynchronous capabilities and automatic data validation via Pydantic. Unlike Django, which is heavily opinionated and monolithic, FastAPI allows for a lightweight microservice architecture. Unlike Flask, FastAPI's async nature allows the backend to execute heavy machine learning predictions and send SMTP alerts as `BackgroundTasks` without blocking the main event loop or slowing down the operations dashboard.

### Frontend: Streamlit
* **The Choice:** Streamlit
* **The Alternatives Rejected:** React, Vue.js
* **Justification:** Streamlit is the most efficient framework for building data-heavy, interactive internal tools in pure Python. Building a React frontend would require a separate JavaScript build step and context switching. Streamlit allows data scientists and backend engineers to own the entire stack. To ensure a production-grade UI, the frontend was completely decoupled from the backend utilizing an `api_client.py` for all HTTP requests, ensuring Separation of Concerns (SoC).

### Database: PostgreSQL (Supabase) + JSONB
* **The Choice:** PostgreSQL with `JSONB` columns
* **The Alternatives Rejected:** MongoDB (Pure NoSQL), standard relational tables
* **Justification:** Eyewear orders require a hybrid data approach. Core tracking data (status, store location, timestamps) requires the strict ACID compliance of a relational database. However, prescription details (spheres, cylinders, coatings) are highly variable. Instead of building a rigid, sparse SQL table with dozens of NULL columns, a Postgres `JSONB` column was utilized for the `lens_details`. This provides the exact flexibility of MongoDB while maintaining relational integrity for the broader order lifecycle. 

---

## 3. AI & MLOps Strategy

### Module 1: Deterministic vs. Probabilistic Logic
* **The Choice:** Rule-Based Engine
* **The Alternative Rejected:** Agentic LLM (Large Language Model)
* **Justification:** For "In-House" inventory tracking, stock routing requires 100% mathematical accuracy. Using a probabilistic generative model (like an LLM) introduces unnecessary latency, cost, and hallucination risks for basic CRUD verifications. Hard-coded rules guarantee precision for operations.

### Module 3: SLA Breach Prediction 
* **The Choice:** XGBoost
* **The Alternative Rejected:** Deep Learning / Neural Networks
* **Justification:** To predict SLA breaches based on categorical order features and time elapsed, an `XGBoost` classification model was trained. XGBoost remains the industry gold standard for tabular data, vastly outperforming Deep Learning on structured datasets in both training speed and inference cost, while remaining highly interpretable for operations audits.

### MLOps Infrastructure
* **The Choice:** Modular Scikit-Learn / Joblib Pipelines ("ZenML-Ready")
* **The Alternative Rejected:** Full ZenML / ClearML deployment for the demo
* **Justification:** To guarantee a frictionless, zero-setup local demo for the review team, the MLOps infrastructure was intentionally kept lightweight. Forcing the reviewer to configure a local ZenML tracking server introduces a high risk of local failure. However, the `mlops` directory is strictly modularized (`ingest_data.py`, `train_xgboost.py`, `evaluate_model.py`), making the pipeline immediately ready to be wrapped in **ZenML** `@step` decorators for enterprise artifact tracking in a true production environment.

---

## 4. Security, Alerting & Deployment

* **Alerting Mechanism:** The AI alerting system natively integrates with Python's `smtplib` to trigger real-time emails to the Operations Team when breach probability exceeds 80%. This was chosen over Twilio/WhatsApp APIs to ensure immediate, zero-cost verifiability for the reviewer. A fallback "mock" mechanism is implemented to catch authentication errors, preventing server crashes if credentials rotate.
* **Secret Management:** All credentials and Supabase database URIs are vaulted in `.env` files and securely injected into the isolated Docker containers at runtime, ensuring zero credential leakage in version control.
* **Cloud Infrastructure:** Render and Supabase (Shared Pooler Transaction Mode over IPv4) were selected to provide a reliable, containerized cloud deployment without the complex overhead of raw AWS EC2 provisioning.