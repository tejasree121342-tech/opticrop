"""
Thin client for a soil-data provider (e.g. ISRIC SoilGrids). SoilGrids is
free and keyless for basic queries, so this wrapper works without an API key
by default; set SOIL_API_KEY if you switch to a commercial provider.
"""
import os
import requests

API_KEY = os.environ.get("SOIL_API_KEY", "")
SOILGRIDS_URL = "https://rest.isric.org/soilgrids/v2.0/properties/query"


def get_soil_properties(lat: float, lon: float, properties=None) -> dict:
    """Fetch soil properties (e.g. phh2o, nitrogen, soc) for a coordinate."""
    properties = properties or ["phh2o", "nitrogen", "soc"]
    params = {
        "lon": lon,
        "lat": lat,
        "property": properties,
        "depth": "0-5cm",
        "value": "mean",
    }
    resp = requests.get(SOILGRIDS_URL, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    import json
    print(json.dumps(get_soil_properties(17.385, 78.4867), indent=2))
