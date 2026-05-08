import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from model.predict import (  # noqa: E402
    build_improved_habits,
    compare_future,
    generate_advice,
    predict_state,
)


st.set_page_config(
    page_title="Future You Simulator",
    layout="wide",
)


RISK_COLORS = {
    "LOW": "#1f9d55",
    "MEDIUM": "#d97706",
    "HIGH": "#dc2626",
}


st.markdown(
    """
    <style>
    .main {
        background: #f7f7f4;
    }
    .block-container {
        padding-top: 2rem;
        max-width: 1180px;
    }
    .metric-panel {
        border: 1px solid #dedbd2;
        border-radius: 8px;
        padding: 18px;
        background: #ffffff;
        min-height: 132px;
    }
    .metric-label {
        color: #56534d;
        font-size: 0.88rem;
        margin-bottom: 0.3rem;
    }
    .metric-value {
        color: #181816;
        font-size: 2.4rem;
        font-weight: 760;
        line-height: 1;
    }
    .risk-pill {
        display: inline-block;
        border-radius: 999px;
        color: #ffffff;
        font-weight: 760;
        letter-spacing: 0;
        padding: 8px 14px;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("Future You Simulator")
st.caption("Adjust daily habits and watch a six-month projection update.")

with st.sidebar:
    st.header("Daily habits")
    sleep_hours = st.slider("Sleep hours", 4.0, 10.0, 6.0, 0.5)
    study_hours = st.slider("Study hours", 0.0, 10.0, 5.0, 0.5)
    screen_time = st.slider("Screen time", 1.0, 10.0, 7.0, 0.5)
    exercise = st.slider("Exercise hours", 0.0, 3.0, 0.5, 0.25)
    social_time = st.slider("Social time", 0.0, 5.0, 2.0, 0.5)
    st.divider()
    show_compare = st.toggle("Compare with improved habits", value=True)

habits = {
    "sleep_hours": sleep_hours,
    "study_hours": study_hours,
    "screen_time": screen_time,
    "exercise": exercise,
    "social_time": social_time,
}

prediction = predict_state(habits)
improved_habits = build_improved_habits(habits)

left, middle, right = st.columns(3)
with left:
    st.markdown(
        f"""
        <div class="metric-panel">
            <div class="metric-label">6-month productivity score</div>
            <div class="metric-value">{prediction["productivity_score"]}%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with middle:
    st.markdown(
        f"""
        <div class="metric-panel">
            <div class="metric-label">Burnout risk</div>
            <span class="risk-pill" style="background:{RISK_COLORS[prediction["burnout_risk"]]}">
                {prediction["burnout_risk"]}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
with right:
    improved_prediction = predict_state(improved_habits)
    delta = improved_prediction["productivity_score"] - prediction["productivity_score"]
    st.markdown(
        f"""
        <div class="metric-panel">
            <div class="metric-label">What-if improvement</div>
            <div class="metric-value">+{delta:.1f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.subheader("Future projection")

if show_compare:
    trend = compare_future(habits, improved_habits)
    chart_data = trend.pivot(
        index="day", columns="scenario", values="productivity_score"
    )
else:
    trend = compare_future(habits, habits)
    chart_data = trend[trend["scenario"] == "Current habits"].set_index("day")[
        ["productivity_score"]
    ]

st.line_chart(chart_data, height=360)

advice_col, habits_col = st.columns([1.1, 0.9])

with advice_col:
    st.subheader("Future advice")
    for item in generate_advice(habits, prediction):
        st.write(f"- {item}")

with habits_col:
    st.subheader("Improved scenario")
    comparison = pd.DataFrame(
        [
            {
                "Habit": "Sleep",
                "Current": sleep_hours,
                "Improved": improved_habits["sleep_hours"],
            },
            {
                "Habit": "Study",
                "Current": study_hours,
                "Improved": improved_habits["study_hours"],
            },
            {
                "Habit": "Screen",
                "Current": screen_time,
                "Improved": improved_habits["screen_time"],
            },
            {
                "Habit": "Exercise",
                "Current": exercise,
                "Improved": improved_habits["exercise"],
            },
            {
                "Habit": "Social",
                "Current": social_time,
                "Improved": improved_habits["social_time"],
            },
        ]
    )
    st.dataframe(comparison, hide_index=True, use_container_width=True)
