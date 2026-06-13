from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
import pandas as pd

def train_model(df: pd.DataFrame):
    # Separate features (X) from target (y)
    X = df.drop(columns=['order_id', 'breached_sla'])
    y = df['breached_sla']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define categorical columns for One-Hot Encoding
    categorical_features = ['lens_type', 'coating', 'store_location', 'current_stage']
    
    preprocessor = ColumnTransformer(
        transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)],
        remainder='passthrough'
    )

    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', XGBClassifier(n_estimators=100, learning_rate=0.1, random_state=42))
    ])

    model_pipeline.fit(X_train, y_train)
    return model_pipeline, X_test, y_test