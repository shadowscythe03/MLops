from fastapi import FastAPI, Query
import pandas as pd
import os

app = FastAPI()

DATA_PATH = "data/predictions/latest_predictions.csv"

@app.get("/")
def read_root():
    return {"message": "Welcome to TrendLens API!"}

@app.get("/predictions/")
def get_predictions(limit: int = Query(10, ge=1, le=100)):
    if not os.path.exists(DATA_PATH):
        return {"error": "No prediction data found."}
    df = pd.read_csv(DATA_PATH)
    return df.head(limit).to_dict(orient="records")