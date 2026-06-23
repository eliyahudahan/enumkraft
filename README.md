# EnumKraft 2.0 – Grid Stability Monitoring with Physics + ML

**Real‑time frequency monitoring + Swing equation + LightGBM load forecasting**

EnumKraft 2.0 is a production‑ready system that combines physical modeling (Swing equation) with machine learning (LightGBM) and live data feeds to detect **Dunkelflaute** events and assess grid stability in Germany.

---

## 🎯 Key Features

- **Live frequency** – from Gridradar API (with TTL caching, 60s)
- **Physics‑based fallback** – Swing equation calculates frequency when live data is unavailable
- **Load forecasting** – LightGBM (MAE **261 MW**, ~0.5% error)
- **Dunkelflaute detection** – based on Strnad et al. (2026): CF < 0.06 over 48h
- **Weather data** – DWD (official German weather service) via Open‑Meteo
- **REST API** – 4 endpoints (health, macro forecast, micro frequency, grid stability)
- **Containerized** – Docker image ready for deployment

---

## 📊 Architecture
┌─────────────────────────────────────────────────────────────┐
│ FastAPI (4 endpoints) │
├─────────────┬───────────────────┬───────────────────────────┤
│ Macro │ Micro │ Grid Stability │
│ Forecast │ Frequency │ (Combined Status) │
└──────┬──────┴────────┬──────────┴──────────────┬────────────┘
│ │ │
▼ ▼ ▼
┌─────────────┐ ┌──────────────┐ ┌──────────────────────────┐
│ LightGBM │ │ Gridradar │ │ DWD + SMARD │
│ (Load MW) │ │ (Live Freq) │ │ (Weather + Load Data) │
└─────────────┘ └──────┬───────┘ └────────────┬─────────────┘
│ │
▼ ▼
┌───────────────┐ ┌────────────────────┐
│ Swing Equation│ │ Dunkelflaute │
│ (Fallback) │ │ Detection (CF) │
└───────────────┘ └────────────────────┘


---

## 🚀 Quick Start

### 1. Clone and setup
```bash
git clone https://github.com/eliyahudahan/enumkraft.git
cd enumkraft
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Add your Gridradar token
Create a .env file:

bash
GRIDRADAR_TOKEN=your_token_here

3. Run with Docker
bash
docker build -t enumkraft:2.0 .
docker run -p 8000:8000 --env-file .env enumkraft:2.0

4. Test the API
bash
curl http://localhost:8000/
curl http://localhost:8000/api/v1/macro/forecast
curl http://localhost:8000/api/v1/micro/frequency
curl http://localhost:8000/api/v1/grid/stability

📡 API Endpoints
Endpoint	Description	Example Response
/	Health check	{"project":"EnumKraft 2.0","status":"running"}
/api/v1/macro/forecast	Load forecast + CF	{"load_mw":50000,"cf_48h":0.004}
/api/v1/micro/frequency	Live frequency (Gridradar / Swing)	{"frequency":49.98,"source":"Gridradar (Live)"}
/api/v1/grid/stability	Combined stability status	{"stability_status":"NORMAL","dunkelflaute_detected":false}

📂 Repository Structure
enumkraft/
├── app/
│   ├── main.py                    # FastAPI endpoints
│   ├── macro_tier.py              # LightGBM + DWD
│   ├── micro_tier.py              # Gridradar + Swing Eq
│   ├── physics_bridge.py          # Resampling + Swing step
│   ├── dunkelflaute.py            # CF < 0.06 detection
│   ├── dwd_fetcher.py             # DWD weather (Open‑Meteo)
│   ├── gridradar_client.py        # Gridradar API with TTL cache
│   └── smard_fetcher.py           # SMARD load data (Germany)
├── models/
│   └── lightgbm_model.pkl         # Trained model (MAE 261 MW)
├── notebooks/
│   └── 02_swing_with_freq.ipynb   # Model training & analysis
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md

🧪 Validation
Metric	Value	Source
Frequency	49.98 ± 0.05 Hz	Gridradar / Swing Eq
Load MAE	261 MW	LightGBM
Dunkelflaute CF	< 0.06	Strnad et al. (2026)
Weather	24h forecast	DWD (Open‑Meteo)

📚 References
Strnad et al. (2026) – Assessing the risk of future Dunkelflaute events for Germany

DWD (2024) – Climate change unlikely to increase Dunkelflaute events

Gridradar API – Live frequency data

SMARD – German electricity market data (Bundesnetzagentur)

🤝 Feedback & Contributions
Open an issue or contact:
Eli Dahan – GitHub | LinkedIn
