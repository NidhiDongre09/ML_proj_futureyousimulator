from pathlib import Path
import sys

import joblib
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from utils.preprocessing import BURNOUT_LABELS, FEATURE_COLUMNS, clamp  # noqa: E402

PRODUCTIVITY_MODEL_PATH = ROOT / "model" / "productivity_model.pkl"
BURNOUT_MODEL_PATH = ROOT / "model" / "burnout_model.pkl"


def _load_models():
    productivity_model = joblib.load(PRODUCTIVITY_MODEL_PATH)
    burnout_model = joblib.load(BURNOUT_MODEL_PATH)
    return productivity_model, burnout_model


def _to_frame(habits):
    return pd.DataFrame([{column: habits[column] for column in FEATURE_COLUMNS}])


def predict_state(habits):
    productivity_model, burnout_model = _load_models()
    frame = _to_frame(habits)

    productivity = float(productivity_model.predict(frame)[0])
    burnout_code = int(burnout_model.predict(frame)[0])

    probabilities = None
    if hasattr(burnout_model, "predict_proba"):
        probabilities = burnout_model.predict_proba(frame)[0].tolist()

    return {
        "productivity_score": round(clamp(productivity, 0, 100), 1),
        "burnout_risk": BURNOUT_LABELS[burnout_code],
        "burnout_code": burnout_code,
        "burnout_probabilities": probabilities,
    }


def simulate_future(habits, days=180, seed=7):
    productivity_model, burnout_model = _load_models()
    rng = np.random.default_rng(seed)

    current = habits.copy()
    rows = []

    for day in range(1, days + 1):
        current["sleep_hours"] = clamp(
            rng.normal(current["sleep_hours"], 0.18), 4, 10
        )
        current["study_hours"] = clamp(
            rng.normal(current["study_hours"], 0.25), 0, 10
        )
        current["screen_time"] = clamp(
            rng.normal(current["screen_time"], 0.25), 1, 10
        )
        current["exercise"] = clamp(rng.normal(current["exercise"], 0.1), 0, 3)
        current["social_time"] = clamp(
            rng.normal(current["social_time"], 0.15), 0, 5
        )

        if day % 30 == 0:
            if current["sleep_hours"] >= 7 and current["exercise"] >= 1:
                current["screen_time"] = clamp(current["screen_time"] - 0.15, 1, 10)
            if current["screen_time"] > 8 or current["sleep_hours"] < 5:
                current["study_hours"] = clamp(current["study_hours"] - 0.2, 0, 10)

        frame = _to_frame(current)
        productivity = float(productivity_model.predict(frame)[0])
        burnout_code = int(burnout_model.predict(frame)[0])

        rows.append(
            {
                "day": day,
                "month": round(day / 30, 1),
                "productivity_score": round(clamp(productivity, 0, 100), 1),
                "burnout_risk": BURNOUT_LABELS[burnout_code],
            }
        )

    return pd.DataFrame(rows)


def compare_future(habits, improved_habits, days=180):
    baseline = simulate_future(habits, days=days, seed=11)
    improved = simulate_future(improved_habits, days=days, seed=11)
    baseline["scenario"] = "Current habits"
    improved["scenario"] = "Improved habits"
    return pd.concat([baseline, improved], ignore_index=True)


def build_improved_habits(habits):
    improved = habits.copy()
    improved["sleep_hours"] = clamp(max(improved["sleep_hours"], 7.5), 4, 10)
    improved["screen_time"] = clamp(min(improved["screen_time"], 5.0), 1, 10)
    improved["exercise"] = clamp(max(improved["exercise"], 1.0), 0, 3)
    return improved


def generate_advice(habits, prediction):
    advice = []

    if prediction["burnout_risk"] == "HIGH":
        advice.append("Protect sleep first: aim for at least 7 hours tonight.")
    if habits["screen_time"] > 6:
        advice.append("Cut screen time by 60 minutes and rerun the simulation.")
    if habits["exercise"] < 1:
        advice.append("Add a short daily workout or walk to stabilize energy.")
    if habits["study_hours"] > 8 and habits["sleep_hours"] < 6:
        advice.append("Your study load is high for your sleep level. Rebalance it.")
    if not advice:
        advice.append("Your habits are balanced. Try small improvements, not big shocks.")

    return advice
