# OptiCrop — API Documentation

Base URL (local dev): `http://localhost:5000/api`

All responses follow the envelope:
```json
{ "success": true, "message": "OK", "data": { ... } }
```
Errors:
```json
{ "success": false, "message": "Description of what went wrong" }
```

## Auth

### POST `/auth/register`
Body: `{ "name": "...", "email": "...", "password": "...", "location": "optional" }`
Returns: `{ token, user }`

### POST `/auth/login`
Body: `{ "email": "...", "password": "..." }`
Returns: `{ token, user }`

### GET `/auth/me`
Header: `Authorization: Bearer <token>`
Returns the authenticated user's profile.

## Crops

### GET `/crops/`
Returns the static crop catalog (season, water need, ideal temp/pH).

### GET `/crops/<crop_name>`
Returns details for a single crop, or 404 if not found.

## Weather

### GET `/weather/current?city=Hyderabad` or `?lat=..&lon=..`
Returns current temperature, humidity, condition, wind, rainfall.

### GET `/weather/forecast?city=Hyderabad`
Returns a 5-day outlook.

## Prediction

### POST `/prediction/recommend-crop`
Body: `{ nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall }`
Returns: `{ recommended_crop, confidence, top_3: [{crop, confidence}, ...] }`

### POST `/prediction/yield`
Body: `{ crop, area_hectares, rainfall_mm, fertilizer_kg }`
Returns: `{ crop, predicted_yield_tons }`

### GET `/prediction/history` (auth required)
Returns the authenticated user's past recommendations and yield predictions.

## Disease Detection

### POST `/disease/detect`
`multipart/form-data` with field `image` (jpg/jpeg/png).
Returns: `{ predicted_label, confidence, is_healthy, image }`

## Market

### GET `/market/prices?crop=rice`
Returns current prices per market for a crop (or all crops if omitted).

### GET `/market/forecast?crop=rice&days=7`
Returns a day-by-day forecast of predicted price per quintal.

## Health

### GET `/health`
Simple liveness check — `{ status: "ok" }`.
