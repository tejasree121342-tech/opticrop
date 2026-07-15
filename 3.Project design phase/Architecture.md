# OptiCrop — Architecture

## Overview

OptiCrop is a three-tier application:

```
┌─────────────┐      REST/JSON       ┌──────────────┐      joblib/keras     ┌──────────────┐
│   Frontend   │  ───────────────▶   │   Backend    │  ──────────────────▶  │  ML Models    │
│  React+Vite  │  ◀───────────────   │  Flask API   │  ◀──────────────────  │ (sklearn/CNN) │
└─────────────┘                      └──────┬───────┘                       └──────────────┘
                                             │
                                     ┌───────┴────────┐
                                     │  SQLite / DB   │
                                     └────────────────┘
```

## Components

### Frontend (`frontend/`)
React SPA built with Vite. Pages correspond to each feature (crop recommendation,
yield prediction, disease detection, market prices, weather). `services/api.js`
centralizes all HTTP calls to the backend; `context/AuthContext.jsx` manages
JWT-based auth state.

### Backend (`backend/`)
Flask REST API organized by domain:
- `routes/` — HTTP endpoints (thin controllers)
- `services/` — business logic, including the ML inference bridge (`ml_service.py`)
  and external API wrappers (`weather_service.py`, `market_service.py`)
- `models/` — data-access layer over SQLite
- `database/` — schema + connection helper
- `middleware/` — cross-cutting concerns (request logging)

### ML Models (`ml_models/`)
Each subdirectory is self-contained with a `train.py` (regenerates the dataset if
missing, trains, and serializes the model) and a `predict.py` (CLI for standalone
inference). The backend loads the serialized artifacts (`.pkl`/`.h5`) lazily and
caches them in memory.

| Model                | Algorithm                | Inputs                                             | Output                       |
|-----------------------|---------------------------|-----------------------------------------------------|-------------------------------|
| Crop Recommendation  | RandomForestClassifier    | N, P, K, temperature, humidity, pH, rainfall        | Crop label + confidence       |
| Yield Prediction     | GradientBoostingRegressor | crop, area, rainfall, fertilizer                    | Yield (tons)                  |
| Disease Detection    | CNN (Keras) / heuristic fallback | Leaf image                                   | Disease label + confidence    |
| Market Forecasting   | RandomForestRegressor     | crop, day offset                                    | Price/quintal per day         |

### External integrations (`api/`)
Wrappers for third-party data sources (OpenWeatherMap, SoilGrids, market price
APIs, NASA POWER for satellite/agroclimatology data), each with local fallbacks
so the app runs without live API keys.

## Data flow example — Crop Recommendation

1. User submits soil/climate readings via `CropRecommendation.jsx`.
2. `api.recommendCrop()` POSTs to `/api/prediction/recommend-crop`.
3. `routes/prediction.py` validates input and calls `services/ml_service.recommend_crop()`.
4. The service loads `ml_models/crop_recommendation/{model,scaler}.pkl`, scales
   the input, and returns the top-3 crop predictions with confidence scores.
5. The response is rendered as `RecommendationCard` components.

## Deployment

`deployment/` contains a `Dockerfile` for the Flask API, `Dockerfile.frontend`
for the static React build served via nginx, a `docker-compose.yml` for local
multi-container orchestration, and Kubernetes manifests for production.
