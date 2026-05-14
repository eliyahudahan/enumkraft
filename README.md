# EnumKraft – Hybrid Physics‑ML for Grid Stability

**Real-time frequency monitoring + Swing equation + LightGBM load forecasting**

EnumKraft is a research project that combines physical modeling (Swing equation) with machine learning to predict grid instability, focusing on **Dunkelflaute** events in the German power grid.

---

## 🔍 Problem statement

Germany has a structural **north-south transmission bottleneck**:  
wind generation in the north, industrial load in the south (Bavaria, Baden-Württemberg).  
During **Dunkelflaute** (low wind + low solar), the southern grid faces both local generation shortfall and import constraints.

**Evidence:**  
- NEP 2037/2045 (official TSO planning document)  
- TenneT grid booster `Kupferzell` (250 MW, operational 2025) – a "virtual transmission line"

---

## 📊 Key results

| Metric | Value | Comment |
|--------|-------|---------|
| LightGBM MAE (Pm → Load) | 4,352 MW | baseline |
| LightGBM MAE (with time features: hour, day_of_week, month, weekend) | **261 MW** | ~0.4% error on average load |
| Weekend load reduction | 12,952 MW | weekday 50,472 MW → weekend 37,520 MW |
| Swing equation fallback | 50 Hz | used due to temporal alignment gap |
| Frequency pipeline | active (Gridradar API, 5s resolution) | ready for real‑time data |

---

## 🧠 What is inside

- **Data collection** – real‑time frequency from Gridradar API (token, `.env`, automatic hourly backup)  
- **Swing equation** – discrete implementation (`H=5`, `P_base=50000 MW`, `dt=0.25 h`)  
- **Machine learning** – LightGBM with time features (hour, day_of_week, month, weekend)  
- **Fallback strategy** – transparent due to lack of temporal overlap between frequency and generation/load data  
- **Visualization** – sine wave (50Hz), actual vs predicted load, hourly load patterns, weekday/weekend comparison  

---

## 📂 Repository structure
enumkraft/
├── data/ # CSV files (ignored by Git)
├── notebooks/
│ └── 02_swing_with_freq.ipynb # main analysis
├── scripts/
│ ├── gridradar_fetcher.py # fetch frequency from Gridradar API
│ └── collect_freq_daily.py # wrapper for hourly backup (cron ready)
├── evidence.md # north‑south bottleneck documentation
├── requirements.txt
├── .env # local – not committed (Gridradar token)
└── README.md


---

## 🚀 How to run

1. Clone the repository  
2. Create virtual environment: `python3 -m venv venv && source venv/bin/activate`  
3. Install dependencies: `pip install -r requirements.txt`  
4. Add your Gridradar token to `.env`: `GRIDRADAR_TOKEN=...`  
5. Run the notebook: `jupyter notebook notebooks/02_swing_with_freq.ipynb`  

---

## 📌 Limitations (transparent)

- No temporal overlap between `gen_df` (27.04–03.05) and Gridradar frequency (04.05 onward)  
- Swing equation uses fallback 50 Hz for demonstration  
- No merge performed – the model uses generation + time features instead of frequency alignment.

## 📚 References

- Li (2025, TU Delft) – *Dunkelflaute events: characterization, prediction and future projection*  
- ENTSO-E Transparency Platform  
- Gridradar API  
- Power Grid Frequency Database (OSF)

---

## 🤝 Feedback from experts (welcome)

If you have suggestions for improvement, especially regarding feature engineering or inertia parameter `H`, please open an issue or contact me.

---

**Eli Dahan** – independent ML practitioner  
[GitHub](https://github.com/eliyahudahan/enumkraft) | [LinkedIn](https://www.linkedin.com/in/eliyahu-dahan-684b22294/)