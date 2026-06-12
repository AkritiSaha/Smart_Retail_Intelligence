# Multimodal Smart Retail Analytics & Security Intelligence System

An end-to-end, production-grade AI backend platform that unifies real-time **Computer Vision (YOLOv8)** edge streaming with predictive **Tabular Machine Learning (XGBoost)**. The entire system architecture is structured as a decoupled microservice powered by an asynchronous **FastAPI** server and a persistent **SQLite3** relational data tier.

---

## 🛠️ System Architecture & Core Modules

The engine is engineered using modular, decoupled Python layers designed for high throughput and reliable asynchronous background database writing:

### 1. 👁️ Edge Computer Vision & Geofencing Core (`core_cv.py`)
* **Object Detection & Tracking:** Leverages state-of-the-art **YOLOv8** weights to monitor live customer density, path coordinates, and crowd flow within the camera frame.
* **Region of Interest (ROI) Geofencing:** Implements strict mathematical coordinate tracking over a designated sub-section of the frame (`STAFF ONLY ZONE`). If customer boundary pixels intersect with the coordinate box, the system dynamically upgrades the threat level, changes bounding boxes to red, and triggers a `SECURITY BREACH` live alert banner.
* **Anomalous Sentiment Profiling:** Dynamically maps face dimensions over time frames to classify expressions into metadata states (`Happy`, `Neutral`, `Sad`) as underlying metrics for consumer behavioral analysis.

### 2. 🗄️ Relational Ledger Tier (`database.py`)
* Integrates a local **SQLite3 database** layer. A background logging daemon intercepts telemetry packets from the live CV frame loop and persists structural time-series metrics (`timestamp`, `customer_count`, `dominant_mood`) at calibrated intervals without blocking frame processing.

### 3. 🧠 Tabular Predictive Machine Learning (`churn_model.py`)
* Employs an optimized **XGBoost Classifier** pipeline trained on feature-engineered historical store vectors, mapping metrics such as absolute visit frequencies, dwell time, purchase distribution, and consumer negativity ratios.
* **Performance:** Achieved an production-optimal **97.00% Evaluation Accuracy Score** for proactive customer churn risk tracking and retention assessment.

### 4. 🔗 Production API Gateway REST Layer (`api_server.py`)
* Engineered with **FastAPI** and served via **Uvicorn** to distribute clean REST endpoints (`/api/live-stats` and `/api/predict-churn`). This creates a scalable microservice architecture, allowing independent frontend clients (Web/Mobile wrappers) to effortlessly consume core database tables and real-time model inference via an interactive Swagger UI.

---

## 📂 Project Directory Structure


Smart_Retail_Intelligence/
├── app/
│   ├── __init__.py
│   ├── api_server.py       # FastAPI Production Microservice Engine
│   ├── check_results.py    # Time-Series Database Analytical Reporter
│   ├── churn_model.py      # XGBoost Behavioral Predictive Pipeline (97% Acc)
│   ├── core_cv.py          # YOLOv8 Geofencing & Edge Computer Vision Core
│   └── database.py         # SQLite3 Automatic Background Relational Data Logger
├── data/
│   └── Store_video.mp4     # Input Local Stream Processing Asset
├── requirements.txt        # Enterprise Python Environment Specifications
└── retail_intelligence.db  # Persistent Binary SQL DB Warehouse
