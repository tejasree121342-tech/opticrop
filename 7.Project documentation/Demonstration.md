# Demonstration

## How to Run

1. Start the backend:

```bash
cd backend
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python database/db.py
python app.py
```

2. Start the frontend:

```bash
cd frontend
npm install
npm run dev
```

3. Open the app at `http://localhost:5173`.

## Sample User

- Email: `nanin_agendra@gmail.com`
- Password: `tejuN@63054`

## Core Flows

- Crop Recommendation: collect soil and climate inputs and submit for the top crop suggestions.
- Yield Prediction: enter crop, area, rainfall, fertilizer and get an estimated yield.
- Disease Detection: upload a leaf image and receive a disease prediction.
- Market Prices: review current prices and short-term forecasts.
- Weather Forecast: search by city and view local weather data.
