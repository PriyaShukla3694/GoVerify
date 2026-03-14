import os
import sys
import subprocess

def ensure_dependencies():
    required = {"numpy", "pandas", "scikit-learn", "joblib"}
    try:
        import numpy # type: ignore
        import pandas # type: ignore
        import sklearn # type: ignore
        import joblib # type: ignore
    except ImportError:
        print("Required ML libraries not found. Auto-installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *required])

ensure_dependencies()

import numpy as np # type: ignore
import pandas as pd # type: ignore
from sklearn.linear_model import LogisticRegression # type: ignore
import joblib # type: ignore

os.makedirs(os.path.dirname(__file__), exist_ok=True)
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'exported_model.joblib')

def generate_synthetic_data(samples=3000):
    """
    Generates synthetic typing metric data for low and high literacy profiles.
    Returns X (features), y (labels).
    Features: [typing_speed (CPM), error_rate (percentage), pause_time (ms)]
    """
    print(f"Generating {samples} synthetic telemetry records...")
    
    # Generate Low Literacy (Struggling) Users (~40% of data)
    low_n = int(samples * 0.4)
    low_speed = np.random.normal(loc=15.0, scale=8.0, size=low_n).clip(min=2.0)
    low_err = np.random.normal(loc=0.35, scale=0.15, size=low_n).clip(max=0.9, min=0.1)
    low_pause = np.random.normal(loc=9000.0, scale=3000.0, size=low_n).clip(min=3000.0)
    low_labels = ['low'] * low_n

    # Generate Medium Literacy Users (~30% of data)
    med_n = int(samples * 0.3)
    med_speed = np.random.normal(loc=45.0, scale=12.0, size=med_n).clip(min=25.0)
    med_err = np.random.normal(loc=0.15, scale=0.08, size=med_n).clip(max=0.3, min=0.05)
    med_pause = np.random.normal(loc=4000.0, scale=1500.0, size=med_n).clip(min=2000.0)
    med_labels = ['medium'] * med_n

    # Generate High Literacy Users (~30% of data)
    high_n = samples - low_n - med_n
    high_speed = np.random.normal(loc=120.0, scale=30.0, size=high_n).clip(min=60.0)
    high_err = np.random.normal(loc=0.05, scale=0.03, size=high_n).clip(max=0.1, min=0.0)
    high_pause = np.random.normal(loc=1500.0, scale=600.0, size=high_n).clip(min=300.0)
    high_labels = ['high'] * high_n

    X = np.vstack([
        np.column_stack([low_speed, low_err, low_pause]),
        np.column_stack([med_speed, med_err, med_pause]),
        np.column_stack([high_speed, high_err, high_pause])
    ])
    
    y = np.array(low_labels + med_labels + high_labels)
    
    return X, y

def train_and_export():
    X, y = generate_synthetic_data(samples=4000)
    
    print("Training Logistic Regression Model...")
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X, y)
    
    print(f"Model Training Accuracy: {clf.score(X, y):.4f}")
    
    print(f"Exporting model artifact to {MODEL_PATH}")
    joblib.dump(clf, MODEL_PATH)

if __name__ == "__main__":
    train_and_export()
    print("Model pipeline completed successfully.")