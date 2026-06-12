import sqlite3
import pandas as pd

def show_my_analytics():
    
    conn = sqlite3.connect("retail_intelligence.db")
    
    
    query = "SELECT * FROM customer_analytics"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if df.empty:
        print("📁 Database is emoty now! First run core_cv.py so that the data can be saved.")
        return

    print("\n==================================================")
    print("🏬 LUXE RETAIL - DATA SCIENCE ANALYTICS REPORT")
    print("==================================================")
    
    print(f"\n📊 Total Saved Records (Frames Logged): {len(df)}")
    print("\n📋 Latest 5 Entries in Database:")
    print(df.tail(5).to_string(index=False))
    
    print("\n😊 Customer Mood Distribution (Total Breakdown):")
    
    mood_counts = df['dominant_mood'].value_counts()
    print(mood_counts.to_string())
    
    print("\n📈 Average Customer Density in Store:")
    avg_customers = df['customer_count'].mean()
    
    print(f"{round(avg_customers)} Customers per log interval")
    print("==================================================\n")

if __name__ == "__main__":
    show_my_analytics()