from sklearn.metrics import accuracy_score, classification_report

def evaluate_model(model_pipeline, X_test, y_test):
    y_pred = model_pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"✅ Accuracy: {accuracy * 100:.2f}%")
    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    return accuracy