# OptiCrop Data Flow Diagram

The following diagram shows each major component and how data moves through the system.

```mermaid
flowchart TD
    subgraph Browser
        A[User] --> B[React Frontend]
    end

    subgraph Backend
        direction TB
        B1[Auth Route (/api/auth/*)]
        B2[Crop Rec Route (/api/prediction/recommend-crop)]
        B3[Yield Route (/api/prediction/yield)]
        B4[Disease Route (/api/disease/detect)]
        B5[Weather Route (/api/weather/*)]
        B6[Market Route (/api/market/*)]
        B1 --> S[SQLite DB]
        B2 --> S
        B3 --> S
        B4 --> S
    end

    subgraph Services
        direction TB
        S1[Auth Service]
        S2[Crop Recommendation Service]
        S3[Yield Service]
        S4[Disease Service]
        S5[Weather Service]
        S6[Market Service]
    end

    subgraph ML Models
        direction TB
        M1[Crop Rec Model <br/>ml_models/crop_recommendation]
        M2[Yield Model <br/>ml_models/yield_prediction]
        M3[Disease Model <br/>ml_models/disease_detection]
    end

    subgraph External_API
        direction TB
        E1[Weather API / Fallback]
        E2[Market API / Fallback]
    end

    B -->|login/register| B1
    B -->|recommend crop| B2
    B -->|predict yield| B3
    B -->|detect disease| B4
    B -->|request weather| B5
    B -->|request market| B6

    B1 --> S1
    B2 --> S2
    B3 --> S3
    B4 --> S4
    B5 --> S5
    B6 --> S6

    S2 -->|load model/scaler| M1
    S3 -->|load model| M2
    S4 -->|load CNN or fallback| M3
    S5 -->|external weather or fallback| E1
    S6 -->|external market or fallback| E2

    S1 -->|read/write user data| S
    S2 -->|store/retrieve history| S
    S3 -->|store/retrieve history| S
    S4 -->|store/retrieve history| S

    S -->|history/results| B
    S2 -->|prediction result| B
    S3 -->|prediction result| B
    S4 -->|disease result| B
    S5 -->|weather data| B
    S6 -->|market data| B
    B -->|display results| A
```

## Key steps

1. User interacts with the React frontend.
2. The frontend calls a Flask backend route.
3. Backend routes delegate work to a service module.
4. Service modules load models or external data.
5. Results are stored in/retrieved from SQLite when needed.
6. The frontend receives results and displays them to the user.
