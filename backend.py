from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/analytics")
def get_analytics():

    try:

        with open(
            "analytics.json",
            "r"
        ) as f:

            return json.load(f)

    except:

        return 
        {
            "error": "analytics.json not found"
        }