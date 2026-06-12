import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb

def generate_mock_customer_data():
    
    np.random.seed(42)
    num_customers = 500
    
    
    total_visits = np.random.randint(1, 30, num_customers)      
    avg_time_spent = np.random.randint(10, 90, num_customers)    
    items_purchased = total_visits * np.random.uniform(0.5, 3.0, num_customers)
    sad_mood_ratio = np.random.uniform(0.0, 1.0, num_customers) 
    
    
    churn_probability = (sad_mood_ratio * 0.6) - (total_visits * 0.02) - (avg_time_spent * 0.005) + 0.3
    churn = (churn_probability > 0.4).astype(int)
    
    
    df = pd.DataFrame({
        'total_visits': total_visits,
        'avg_time_spent': avg_time_spent,
        'items_purchased': items_purchased,
        'sad_mood_ratio': sad_mood_ratio,
        'churn': churn 
    })
    return df

def train_churn_model():
    print(" Data is getting load and cleaned...")
    df = generate_mock_customer_data()
    
    
    X = df.drop(columns=['churn'])
    y = df['churn']
    
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(" XGBoost Model is getting trained...")
    model = xgb.XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42)
    model.fit(X_train, y_train)
    
    # Model Evaluation
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    print("\n📊 --- MODEL PERFORMANCE METRICS ---")
    print(f"✅ Accuracy Score: {accuracy * 100:.2f}%")
    print("\n📝 Classification Report:")
    print(classification_report(y_test, predictions))
    
    return model


def predict_customer_status(model, total_visits, avg_time, items, sad_ratio):
    
    input_data = pd.DataFrame([[total_visits, avg_time, items, sad_ratio]], 
                              columns=['total_visits', 'avg_time_spent', 'items_purchased', 'sad_mood_ratio'])
    prediction = model.predict(input_data)[0]
    return "⚠️ High Risk (Churn)" if prediction == 1 else "💚 Loyal Customer"

if __name__ == "__main__":
    trained_model = train_churn_model()
    
    print("\n🔮 Mock Prediction Check:")
    result = predict_customer_status(trained_model, total_visits=3, avg_time=15, items=1, sad_ratio=0.85)
    print(f"Customer Profile Status: {result}")