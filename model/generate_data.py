from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "synthetic_data.csv"


def calculate_productivity(sleep, study, screen, exercise, social, rng):
    score = (
        study * 8
        + sleep * 5
        + exercise * 6
        - screen * 4
        - social * 2
        + rng.normal(0, 7)
    )

    if 6.5 <= sleep <= 8.5:
        score += 8
    elif sleep < 5:
        score -= 12

    if study > 8 and sleep < 6:
        score -= 10

    return float(np.clip(score, 0, 100))


def calculate_burnout(sleep, study, screen, exercise, social):
    pressure = 0

    if sleep < 5:
        pressure += 2
    elif sleep < 6:
        pressure += 1

    if screen > 7:
        pressure += 2
    elif screen > 5:
        pressure += 1

    if study > 8:
        pressure += 1

    if exercise < 0.5:
        pressure += 1

    if social < 0.5 or social > 4.5:
        pressure += 1

    if sleep < 5 and screen > 7:
        return 2
    if pressure >= 4:
        return 2
    if pressure >= 2:
        return 1
    return 0


def generate_dataset(rows=2000, seed=42):
    rng = np.random.default_rng(seed)
    records = []

    for _ in range(rows):
        sleep = rng.uniform(4, 10)
        study = rng.uniform(0, 10)
        screen = rng.uniform(1, 10)
        exercise = rng.uniform(0, 3)
        social = rng.uniform(0, 5)

        productivity = calculate_productivity(
            sleep, study, screen, exercise, social, rng
        )
        burnout = calculate_burnout(sleep, study, screen, exercise, social)

        records.append(
            {
                "sleep_hours": round(sleep, 2),
                "study_hours": round(study, 2),
                "screen_time": round(screen, 2),
                "exercise": round(exercise, 2),
                "social_time": round(social, 2),
                "productivity_score": round(productivity, 2),
                "burnout_risk": burnout,
            }
        )

    return pd.DataFrame(records)


def main():
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = generate_dataset()
    df.to_csv(DATA_PATH, index=False)
    print(f"Generated {len(df)} rows at data/synthetic_data.csv")


if __name__ == "__main__":
    main()
