import joblib
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 1. Load the trained XGBoost Pipeline
MODEL_PATH = "services/ml_models/sla_predictor.pkl"
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"⚠️ Warning: ML model not found at {MODEL_PATH}. Predictions disabled.")

# 2. The Core AI Evaluation Function
def check_sla_and_alert(order_id: int, lens_type: str, coating: str, store_location: str, current_stage: str, time_elapsed_hours: float):
    if model is None:
        return

    input_data = pd.DataFrame([{
        "lens_type": lens_type,
        "coating": coating,
        "store_location": store_location,
        "current_stage": current_stage,
        "time_elapsed_hours": time_elapsed_hours
    }])

    probability = model.predict_proba(input_data)[0][1]

    if probability >= 0.80:
        # Trigger the new Email alert!
        send_email_alert(order_id, current_stage, probability)

# 3. The Real Email Mechanism
def send_email_alert(order_id: int, stage: str, prob: float):
    # Grab credentials from environment variables (or put a dummy email here just for the terminal fallback)
    # WARNING: Never hardcode real passwords in your code!
    sender_email = os.getenv("EMAIL_SENDER", "eluno.demo@gmail.com")
    sender_password = os.getenv("EMAIL_PASSWORD", "your_app_password") 
    receiver_email = os.getenv("EMAIL_RECEIVER", "warehouse_manager@eluno.com")

    subject = f"🚨 CRITICAL: SLA Breach Risk for Order #{order_id}"
    body = f"""
    Hello Eluno Operations Team,

    This is an automated AI alert from the Eluno Order Management Engine.

    Order #{order_id} is at high risk of missing its Service Level Agreement (SLA).
    - Current Stage: {stage}
    - AI Breach Probability: {prob * 100:.1f}%

    Please intervene immediately to fast-track this order.

    Best,
    Eluno AI System
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # 4. Attempt to send the real email, fallback to terminal if no credentials exist
    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() # Secure the connection
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print(f"\n✅ REAL EMAIL ALERT SENT to {receiver_email} for Order #{order_id}!\n")
    except Exception as e:
        # The Safety Net: If it fails (e.g., bad password), mock it in the terminal so the demo survives
        print("\n" + "📧" * 25)
        print(" [EMAIL API MOCKED] - CREDENTIALS NOT SET")
        print(f" To: {receiver_email}")
        print(f" Subject: {subject}")
        print(body)
        print("📧" * 25 + "\n")