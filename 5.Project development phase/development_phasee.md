# OptiCrop Project Development Phase

## 1. Overview
This document outlines the development phase for OptiCrop, a precision agriculture platform combining a Flask backend, React frontend, and machine learning models for crop recommendation, yield prediction, disease detection, weather insights, and market pricing.

## 2. Goals
- Build the complete production-ready application architecture.
- Integrate backend APIs, frontend UI, and ML inference services.
- Deliver secure, testable, and deployable application components.
- Prepare Docker and deployment manifests for local and cloud deployment.

## 3. Key Deliverables
1. Backend implementation
   - Flask REST API with modular controllers, routes, models, and services
   - JWT authentication and authorization
   - Database persistence for predictions, users, and admin operations
   - External API adapters for weather, soil, and market data
   - Prediction logging and analytics endpoints
2. Frontend implementation
   - React + Vite single-page application
   - Auth flows, dashboard, crop recommendation, weather, market, disease, and yield pages
   - Responsive UI components and charts
   - API integration with backend services
3. ML integration
   - Crop recommendation model packaged under `ml_models/crop_recommendation`
   - Yield prediction model under `ml_models/yield_prediction`
   - Disease detection model under `ml_models/disease_detection`
   - Market forecasting and sample models under `ml_models/market_forecasting` and `ml_models/sample_model`
   - Inference wrapper modules and model metadata endpoints
4. Deployment and ops
   - Docker Compose and Dockerfiles for backend/frontend
   - Kubernetes manifests under `deployment/kubernetes`
   - Nginx reverse proxy and production-ready config
5. Documentation and testing
   - Project docs in `docs/`
   - Automated tests in `tests/`
   - Health checks, logging, and CI-ready structure

## 4. Development Milestones
- Milestone 1: Backend API and data models
  - Implement backend routes and services for recommendation, suitability, prediction, weather, market, and disease
  - Create database schema, repository interfaces, and persistence logic
  - Add authentication and admin controls
- Milestone 2: Frontend feature pages
  - Build main user flows: home, dashboard, crop recommendation, market prices, weather forecast, disease detection, yield prediction
  - Implement reusable UI components (cards, charts, sidebar, navbar)
  - Connect frontend to backend API with auth support
- Milestone 3: Machine learning integration
  - Verify ML model loading and prediction pipelines
  - Create model selection and evaluation support
  - Add endpoints for model metadata and retraining status
- Milestone 4: Security and validation
  - Add CSRF protection, input validation, and rate limiting
  - Secure admin routes and harden API error handling
- Milestone 5: Deployment and documentation
  - Build Docker images and compose stack
  - Add deployment docs and runbook guidance
  - Finalize README, architecture, and planning docs

## 5. Development Phase Tasks
### 5.1 Backend
- `backend/app.py` and `backend/config.py` setup
- `backend/routes/*.py` for feature-specific APIs
- `backend/controllers/*.py` to separate request handling
- `backend/services/*.py` for business logic and predictions
- `backend/database/db.py` and `backend/database/schema.sql`
- `backend/models/*` for prediction and user schemas
- `backend/middleware/logger.py` for request/response logging
- `backend/utils/helpers.py` for IP hashing, validation helpers, and shared utilities

### 5.2 Frontend
- `frontend/src/pages/*` pages for each app section
- `frontend/src/components/*` reusable UI cards and widgets
- `frontend/src/services/api.js` for fetching backend APIs
- `frontend/src/context/AuthContext.jsx` for user session state
- `frontend/src/hooks/useAsync.js` for asynchronous data loading
- `frontend/src/utils/format.js` for formatting values and dates

### 5.3 ML Services
- `ml_models/crop_recommendation/train.py`, `predict.py`
- `ml_models/yield_prediction/train.py`, `predict.py`
- `ml_models/disease_detection/train.py`, `predict.py`
- `ml_models/market_forecasting/train.py`
- Create inference wrappers that load models and scalers safely
- Add metadata and compatibility handling for legacy SKLearn/TensorFlow models

### 5.4 Data and External APIs
- Use `datasets/` for core CSV data sources: crop, market, soil, weather, yield
- `api/weather_api.py`, `api/soil_api.py`, `api/market_api.py` for external data fetching
- Backend should normalize API responses and handle missing data gracefully
- Add caching or retry logic for external service failure cases

### 5.5 Testing and Quality
- Add `tests/conftest.py` shared fixtures for Flask app and mocked services
- Write route, service, repository, validator, and model tests
- Add property-based tests if possible for input validation and persistence
- Ensure developer environment can run `pytest tests/`

## 6. Architecture Alignment
- Three-tier architecture:
  - Presentation: React frontend and Flask routes/templates
  - Business logic: Flask controllers/services, ML services
  - Data access: SQLite database, CSV datasets, model files
- Decouple ML logic from API controllers to make models replaceable
- Use config-driven environment variables for secrets, DB path, API keys, and model paths

## 7. Project-specific Notes
- OptiCrop focuses on actionable crop recommendations using soil, weather, and market signals.
- The platform should support easy extension by adding new crop models and dataset sources.
- Admin features are important for model management, training metadata, and logs.
- Documentation must be stored in the repo under `docs/` and linked from `README.md`.

## 8. Recommended Folder Placement
- Keep this file at `docs/project_development_phase/development_phase.md`
- Keep related docs in:
  - `docs/requirement_analysis/`
  - `docs/project_design_phase/`
  - `docs/project_planning_phase/`

## 9. Follow-up Actions
- If you want, I can also create a matching `README` section or update `README.md` with links to these docs.
- I can also summarize the development phase into a shorter project board style if needed.
