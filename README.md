# OptiCrop 🌾

OptiCrop is a full-stack, ML-powered precision agriculture platform. It helps
farmers make data-driven decisions across four core areas:

- **Crop Recommendation** — suggests the best crop for a plot based on soil (N, P, K, pH) and climate (temperature, humidity, rainfall).
- **Yield Prediction** — estimates expected yield (tons/hectare) from crop, area, rainfall and fertilizer usage.
- **Disease Detection** — classifies crop leaf images as healthy or diseased (CNN-based).
- **Market Price Forecasting** — forecasts short-term commodity prices from historical trends.

## Stack

| Layer      | Tech                                   |
|------------|-----------------------------------------|
| Frontend   | React (Vite), Recharts, Fetch API       |
| Backend    | Flask (Python), REST API, JWT auth      |
| ML Models  | scikit-learn (RandomForest), Keras/TF CNN |
| Database   | SQLite (dev) / PostgreSQL-ready schema  |

## Quickstart

### 1. Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python database/db.py          # initializes SQLite schema
python app.py                  # runs on http://localhost:5000
```

### 2. Train the ML models (optional — pretrained pkl/h5 already included)

```bash
cd ml_models/crop_recommendation && python train.py
cd ../yield_prediction && python train.py
cd ../disease_detection && python train.py
cd ../market_forecasting && python train.py
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev                    # runs on http://localhost:5173
```

The frontend expects the backend at `http://localhost:5000` (see `frontend/src/services/api.js`).

## Project Structure

- `frontend/` — React + Vite user interface
- `backend/` — Flask API, auth, ML inference, database layer
- `ml_models/` — training scripts and serialized model artifacts
- `datasets/` — CSV input data and sample datasets
- `api/` — external data wrappers and API fallback helpers
- `deployment/` — Docker, nginx, and Kubernetes manifests
- `docs/` — architecture, API docs, user guide, planning, testing, and demo notes
- `tests/` — backend and frontend test coverage

## Documentation

See `docs/` for the full project documentation:

- `docs/Brainstorming.md`
- `docs/Requirements.md`
- `docs/Design.md`
- `docs/Planning.md`
- `docs/Development.md`
- `docs/Testing.md`
- `docs/Demonstration.md`
- `docs/API_Documentation.md`
- `docs/Architecture.md`
- `docs/User_Guide.md`
- `docs/Deployment.md`
- `docs/README_OVERVIEW.md`

## License

MIT — see [LICENSE](LICENSE).
