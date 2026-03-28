# 💠 FitPulse — Health Anomaly Detection from Fitness Devices

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

**A multi-milestone Streamlit analytics platform for detecting health anomalies in Fitbit wearable data using machine learning.**

[📊 Data Explorer](#milestone-1--data-explorer) · [🔬 Intelligence Lab](#milestone-2--intelligence-lab) · [🚨 Anomaly Detector](#milestone-3--anomaly-detector)

</div>

---

## 📌 Overview

FitPulse is an end-to-end health analytics web application built with Streamlit. It ingests raw Fitbit fitness-device data, performs exploratory data analysis, applies machine learning-based clustering and time-series forecasting, and finally detects health anomalies across heart rate, sleep, and step-count signals — all within an immersive dark-themed, interactive dashboard.

**Dataset:** 2016 Fitbit Public Dataset — 35 users · 31 days · 174,000+ heart-rate records

---

## ✨ Key Features

- **Interactive Multi-Page Dashboard** with a custom dark-themed sidebar navigation
- **EDA & Preprocessing** — automated cleaning, feature engineering, and 8+ chart types
- **Time-Series Forecasting** using Facebook Prophet
- **Feature Extraction** via TSFresh for biomechanical signal analysis
- **User Segmentation** via K-Means / DBSCAN clustering
- **Anomaly Detection** across Heart Rate, Sleep, and Step signals with 90%+ simulated accuracy
- **Structural Outlier Detection** using DBSCAN
- Fully responsive, dark-mode UI with Plotly and Matplotlib visualizations

---

## 🗂️ Project Structure

```
FitPulse/
│
├── Home.py                     # Main entry point — landing dashboard
│
├── pages/
│   ├── 1preprocessing.py       # Milestone 1 · Data Explorer & EDA
│   ├── 2clustring.py           # Milestone 2 · Intelligence Lab (TSFresh, Prophet, Clustering)
│   └── 3anomaly_detector.py    # Milestone 3 · Anomaly Detection Observatory
│
├── preprocessing.py            # Core preprocessing & EDA utility functions
│
└── requirements.txt            # Python dependencies
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/MandapakaGanesh/FitPulse-Health-Anomaly-Detection-from-Fitness-Devices.git
   cd FitPulse-Health-Anomaly-Detection-from-Fitness-Devices
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**

   ```bash
   streamlit run Home.py
   ```

4. Open your browser at `http://localhost:8501`

---

## 📂 Dataset

The application uses the **2016 Fitbit Fitness Tracker Dataset** (publicly available on Kaggle).

Place the following CSV files in the project root or upload them via the app UI:

| File | Description |
|------|-------------|
| `dailyActivity_merged.csv` | Daily activity summaries per user |
| `hourlySteps_merged.csv` | Hourly step counts |
| `hourlyIntensities_merged.csv` | Hourly intensity metrics |
| `sleepDay_merged.csv` | Daily sleep records |
| `heartrate_seconds_merged.csv` | Second-level heart rate readings |
| `minuteHeartrate_merged.csv` | Minute-level heart rate data |

> **Dataset stats:** 35 users · 31 days · 174,000+ HR records · 10 ML features

---

## 🧩 Milestones

### Milestone 1 · Data Explorer

> `pages/1preprocessing.py`

The Data Explorer provides full exploratory analysis of the Fitbit dataset.

- Upload and validate CSV data
- Automated preprocessing and null-value handling
- 8+ interactive chart types (distribution plots, correlation heatmaps, trend lines, boxplots)
- Per-user and aggregate statistics
- Dark-themed Matplotlib/Seaborn visualizations

### Milestone 2 · Intelligence Lab

> `pages/2clustring.py`

The Intelligence Lab applies advanced ML techniques for deeper signal analysis.

| Section | Method | Purpose |
|---------|--------|---------|
| Overview | Descriptive stats | Dataset KPIs and summaries |
| TSFresh | Feature extraction | Automated biomechanical feature generation from time series |
| Prophet | Forecasting | Facebook Prophet for step/activity trend forecasting |
| Clustering | K-Means / Segmentation | User behavioral segmentation |

### Milestone 3 · Anomaly Detector

> `pages/3anomaly_detector.py`

The Anomaly Detection Observatory identifies health anomalies using statistical and ML-based methods.

| Section | Signal | Method |
|---------|--------|--------|
| Heart Rate | BPM time series | Z-score / IQR anomaly flagging |
| Sleep | Sleep duration & efficiency | Threshold-based detection |
| Steps | Daily step counts | Statistical outlier detection |
| DBSCAN | Multi-feature | Density-based structural outlier detection |
| Accuracy | Simulation | 90%+ accuracy validation |

---

## 🛠️ Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend / UI** | Streamlit, Custom HTML/CSS, Google Fonts (Sora, Space Mono) |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly, Matplotlib, Seaborn |
| **Machine Learning** | scikit-learn (K-Means, DBSCAN), TSFresh, Facebook Prophet |
| **Language** | Python 3.9+ |

---

## 📈 Statistics at a Glance

| Metric | Value |
|--------|-------|
| Users in Dataset | 35 |
| Observation Period | 31 Days |
| Heart Rate Records | 174,000+ |
| ML Features Engineered | 10+ |
| Anomaly Detection Accuracy | 90%+ |
| Dashboard Pages | 3 Milestones |
| Chart Types | 8+ |

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature-name`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature-name`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Mandapaka Ganesh**
- GitHub: [@MandapakaGanesh](https://github.com/MandapakaGanesh)

---

<div align="center">

*FitPulse · 2016 Fitbit Dataset · Built with ❤️ using Streamlit · 2026*

</div>
