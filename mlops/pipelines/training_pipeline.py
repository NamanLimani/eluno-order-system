import os
import joblib
from steps.ingest_data import ingest_data
from steps.train_xgboost import train_model
from steps.evaluate_model import evaluate_model

def run_training_pipeline():
    print("🚀 Starting Modular ML Training Pipeline...")
    
    # Step 1
    df = ingest_data("mlops/data/historical_orders.csv")
    
    # Step 2
    print("🧠 Training XGBoost Model...")
    model_pipeline, X_test, y_test = train_model(df)
    
    # Step 3
    print("📈 Evaluating Model...")
    evaluate_model(model_pipeline, X_test, y_test)
    
    # Save the model
    os.makedirs("backend/services/ml_models", exist_ok=True)
    model_save_path = "backend/services/ml_models/sla_predictor.pkl"
    joblib.dump(model_pipeline, model_save_path)
    print(f"💾 Model saved to {model_save_path}")