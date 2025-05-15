
import os
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()
model = None
encoders = None


@app.on_event("startup")
def load_assets():
    global model, encoders
    base_dir = os.path.dirname(__file__)
    model_path = os.path.join(base_dir, "trained_model", "model.pkl")
    encoders_path = os.path.join(base_dir, "trained_model", "encoders.pkl")
    model = joblib.load(model_path)
    encoders = joblib.load(encoders_path)
    print("Model and encoders loaded")


class MatchInput(BaseModel):
    team_1: str
    team_2: str
    toss_winner: str
    toss_decision: str
    venue: str
    match_type: str
    home_team: str


@app.get("/")
def home():
    return {"message": "Welcome to the Match Winner Prediction API 🚀"}


@app.post("/predict")
def predict_winner(data: MatchInput):
    team_encoder = encoders['team_1']
    teams = sorted([data.team_1, data.team_2])
    team_1 = teams[0]
    team_2 = teams[1]

    input_dict = {
        "team_1": team_encoder.transform([team_1])[0],
        "team_2": team_encoder.transform([team_2])[0],
        "toss_winner": team_encoder.transform([data.toss_winner])[0],
        "home_team": team_encoder.transform([data.home_team])[0],
        "venue": encoders['venue'].transform([data.venue])[0],
        "match_type": encoders['match_type'].transform([data.match_type])[0],
        "toss_decision": encoders['toss_decision'].transform([data.toss_decision])[0]
    }

    X = np.array([list(input_dict.values())])
    pred = model.predict(X)[0]
    predicted_team = team_encoder.inverse_transform([pred])[0]

    return {"predicted_winner": predicted_team}
