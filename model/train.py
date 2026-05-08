from pathlib import Path
import sys

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from utils.preprocessing import FEATURE_COLUMNS  # noqa: E402

DATA_PATH = ROOT / "data" / "synthetic_data.csv"
PRODUCTIVITY_MODEL_PATH = ROOT / "model" / "productivity_model.pkl"
BURNOUT_MODEL_PATH = ROOT / "model" / "burnout_model.pkl"
METRICS_PATH = ROOT / "model" / "metrics.txt"


def train():
    df = pd.read_csv(DATA_PATH)

    x = df[FEATURE_COLUMNS]
    y_productivity = df["productivity_score"]
    y_burnout = df["burnout_risk"]

    x_train, x_test, yp_train, yp_test, yb_train, yb_test = train_test_split(
        x,
        y_productivity,
        y_burnout,
        test_size=0.2,
        random_state=42,
        stratify=y_burnout,
    )

    productivity_model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "regressor",
                RandomForestRegressor(
                    n_estimators=180,
                    random_state=42,
                    min_samples_leaf=3,
                ),
            ),
        ]
    )

    burnout_model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=180,
                    random_state=42,
                    class_weight="balanced",
                    min_samples_leaf=2,
                ),
            ),
        ]
    )

    productivity_model.fit(x_train, yp_train)
    burnout_model.fit(x_train, yb_train)

    productivity_predictions = productivity_model.predict(x_test)
    burnout_predictions = burnout_model.predict(x_test)

    metrics = {
        "productivity_mae": mean_absolute_error(yp_test, productivity_predictions),
        "productivity_r2": r2_score(yp_test, productivity_predictions),
        "burnout_accuracy": accuracy_score(yb_test, burnout_predictions),
    }

    joblib.dump(productivity_model, PRODUCTIVITY_MODEL_PATH)
    joblib.dump(burnout_model, BURNOUT_MODEL_PATH)

    METRICS_PATH.write_text(
        "\n".join(f"{key}: {value:.4f}" for key, value in metrics.items()),
        encoding="utf-8",
    )

    return metrics


def main():
    metrics = train()
    print("Training complete")
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}")


if __name__ == "__main__":
    main()
