# Design

## Architecture Overview

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

- Frontend: React SPA built with Vite, with pages for crop recommendation, yield prediction, disease detection, market prices, weather, and profile.
- Backend: Flask REST API organized by blueprints in `backend/routes/`, business logic in `backend/services/`, data models in `backend/models/`, and persistence in `backend/database/`.
- ML Models: Serialized model files and training scripts under `ml_models/` for crop recommendation, yield prediction, disease detection, and market forecasting.
- External integrations: `api/` wrappers for weather, soil, market, and satellite data, with local fallback data when external keys are unavailable.

## Dependency Notes

- Backend runtime dependencies are defined in `requirements.txt` and `backend/requirements.txt`.
- Disease detection uses `Pillow` for image loading and optionally uses TensorFlow/Keras if installed.
- ML inference uses `scikit-learn`, `joblib`, and model artifact files stored in `ml_models/`.

## Backend Architecture

- `backend/app.py` initializes Flask, CORS, JWT, and blueprint registration.
- `backend/routes/` contains endpoint handlers for auth, prediction, weather, market, crops, and disease detection.
- `backend/services/` contains the core application logic and ML bridging functions.
- `backend/models/` encapsulates database interactions and user history storage.
- `backend/database/` contains schema creation and SQLite connection helpers.

## ML Flow

- Crop recommendation loads a trained RandomForest model and scaler from `ml_models/crop_recommendation/`.
- Yield prediction loads a GradientBoosting regressor from `ml_models/yield_prediction/`.
- Disease detection attempts to load `ml_models/disease_detection/cnn_model.h5`; if TensorFlow is not available, the backend falls back to a lightweight heuristic.
- Market forecasting uses a RandomForest model from `ml_models/market_forecasting/`.

## Data Flow

1. User sends data from the UI to the backend via `/api/` endpoints.
2. Backend validates input and routes requests to service layer logic.
3. Services load or cache ML models, call prediction code, or fetch external/fallback data.
4. Backend responds with a consistent JSON envelope.
5. Frontend renders results and stores authenticated state via `AuthContext.jsx`.
