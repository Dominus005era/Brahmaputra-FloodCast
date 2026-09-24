# FloodSense AI — Brahmaputra Flood Early Warning System (EWS)

> **Know the risk. Act before the flood.**  
> Real-Time AI-Powered Hydrological Forecasting & Multi-Tier Disaster Risk Escalation for the Brahmaputra River Basin.

---

## 🌊 Overview

**FloodSense AI** is an operational flood early warning system engineered specifically for vulnerable flood-prone regions in Assam, India. Anchored at the **Tangni River** gauge station (`NH15 Crossing Fakirpara Tangni`) in **Darrang District**, FloodSense AI integrates ground river telemetry and real-time Copernicus GloFAS hydrology models to forecast critical high-water surges **6 hours in advance** with **99.1% F1-Score**.

The platform translates predictive probabilities into actionable **Disaster Management Risk Categories** (`LOW`, `MODERATE`, `HIGH`, `CRITICAL`) and automated **Escalation Tiers** (`LOCAL`, `DISTRICT`, `STATE`) to assist emergency response teams and the Assam State Disaster Management Authority (ASDMA).

---

## 🚀 Key Features

- **6-Hour Advance Warning**: Predicts impending river level breaches 6 hours before dangerous inundation occurs.
- **Dual-Stream Telemetry Ingestion**:
  - *Primary Ground Stream*: Direct API connection to Government National Water Data Portal (NWDP / NWIC).
  - *Hydrology Bridge Fallback*: Real-time streamflow estimation combining ECMWF Copernicus GloFAS river discharge, high-resolution precipitation, and a local channel hydraulic rating curve.
- **Automated Source Priority & Deduplication**: Real-time ground sensor updates automatically override derived estimates with strict timestamp deduplication.
- **Trained Machine Learning Engine**: 200-tree Random Forest classifier evaluating 19 engineered lag, moving-average, and rate-of-rise features.
- **Emergency Command Center UI**:
  - Live circular probability gauge and animated critical-risk pulsing alerts.
  - Interactive GIS Leaflet map centered at gauge coordinates (`26.5083° N, 92.1164° E`).
  - 6h, 12h, and 24h interactive historical trend charts.
  - Interactive operator simulation sandbox to evaluate custom stage scenarios.
  - Filterable telemetry log with one-click CSV audit export.
- **Hybrid Database Persistence**: Microsoft SQL Server (`FloodSenseDB`) with automatic SQLite fallback for zero-setup cloud deployments (Render, Railway, etc.).

---

## 🏗️ System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                        DATA INGESTION LAYER                            │
│  Primary: India Govt NWDP / NWIC Telemetry API (Hourly Gauge Data)     │
│  Fallback: Hydrology Bridge (Copernicus GloFAS River Discharge +      │
│            Open-Meteo Hourly Precipitation + Channel Rating Curve)     │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      MACHINE LEARNING INFERENCE                        │
│  • 19 Engineered Hydrological Features (Lags, Rolling Stats, Deltas)   │
│  • Calibrated Random Forest Classifier (200 Trees, 99.1% F1-Score)    │
│  • Risk & Escalation Rules Engine (LOW / MODERATE / HIGH / CRITICAL)   │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   BACKEND & DATABASE (FastAPI + SQL)                   │
│  • FastAPI REST Server with asynchronous background ingestion worker   │
│  • Microsoft SQL Server / SQLite with source-priority & deduplication  │
│  • Endpoints: /health, /api/stations, /api/flood/current, /history,    │
│               /predict-custom (Simulation Mode)                        │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   FRONTEND EMERGENCY COMMAND CENTER                    │
│  • Single-Page Web App (Tailwind CSS, Leaflet Maps, Chart.js)          │
│  • Live Status Dashboard, 24h Trend Analysis & Critical Pulse Alerts   │
│  • Interactive Operator Simulation Sandbox & Full Historical Export    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Model Performance

Evaluated on strict chronological holdout test sets without future lookahead leakage:

| Metric | Score |
| :--- | :--- |
| **Accuracy** | **98.56%** |
| **Precision** | **98.36%** |
| **Recall** | **99.92%** |
| **F1-Score** | **99.13%** |

---

## 🚦 Risk Categories & Disaster Escalation

| Risk Level | Trigger Threshold | Escalation Level | Action Protocol |
| :--- | :--- | :--- | :--- |
| **LOW** | Probability $< 30\%$ | `NONE` | Routine hydrological monitoring |
| **MODERATE** | Probability $30\% - 60\%$ | `LOCAL` | Circle Officer / Panchayat advisory alert |
| **HIGH** | Probability $60\% - 85\%$ | `DISTRICT` | DDMA emergency notification & asset mobilization |
| **CRITICAL** | Probability $\ge 85\%$ or Stage $\ge 50\text{m}$ | `STATE` | ASDMA state disaster response & evacuation activation |

---

## 🛠️ Technology Stack

- **Backend**: FastAPI, Uvicorn, Pydantic v2, SQLAlchemy 2.0
- **Database**: Microsoft SQL Server / SQLite (hybrid auto-fallback)
- **Machine Learning**: Scikit-Learn, Pandas, NumPy, Joblib
- **Frontend**: Vanilla HTML5/ES6+, Tailwind CSS, Leaflet.js, Chart.js, Lucide Icons
- **APIs**: NWDP / NWIC CKAN API, Copernicus GloFAS, Open-Meteo

---

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Dominus005era/Brahmaputra-FloodCast.git
cd Brahmaputra-FloodCast
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
- **Windows (One-Click)**: Double-click `start_floodsense.bat`
- **Manual (Terminal)**:
  ```bash
  python backend/run_server.py
  ```

Access the dashboard at: [http://localhost:8000](http://localhost:8000)  
Interactive Swagger API documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Testing

Run the automated integration test suite:
```bash
python backend/test_backend.py
python backend/test_source_priority.py
python scripts/fetch/test_live_system.py
```

---

## 📄 License

This project is licensed under the MIT License.
