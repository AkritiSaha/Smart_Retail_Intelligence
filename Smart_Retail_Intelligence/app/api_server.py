from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from app.churn_model import train_churn_model, predict_customer_status

app = FastAPI(title="Luxe Retail Vision AI - Backend API Engine")

print("🔄 Initializing Machine Learning Core...")
ml_model = train_churn_model()
print(" ML Core Active!")


class CustomerProfile(BaseModel):
    total_visits: int
    avg_time_spent: int
    items_purchased: float
    sad_mood_ratio: float

@app.get("/")
def root():
    return {"status": "Online", "message": "Welcome to Smart Retail Intelligence API Server"}

@app.get("/api/live-stats")
def get_live_stats():
    try:
        conn = sqlite3.connect("retail_intelligence.db")
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, customer_count, dominant_mood FROM customer_analytics ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "latest_update": row[0],
                "live_customer_count": row[1],
                "dominant_mood": row[2]
            }
        return {"message": "No real-time data found in DB yet. Run core_cv first!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/predict-churn")
def predict_churn(profile: CustomerProfile):
    try:
        
        status = predict_customer_status(
            ml_model, 
            profile.total_visits, 
            profile.avg_time_spent, 
            profile.items_purchased, 
            profile.sad_mood_ratio
        )
        return {
            "customer_analytics_status": status,
            "action_recommended": "Trigger 20% discount coupon" if "Risk" in status else "Maintain standard engagement"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))