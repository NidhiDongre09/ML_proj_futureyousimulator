# Future You Simulator

Future You Simulator is an interactive machine learning project that predicts a user's future productivity and burnout risk from daily habits. The app lets users adjust lifestyle inputs such as sleep, study time, screen time, exercise, and social time, then visualizes a possible six-month future trajectory.

The goal of this project is not only to make a prediction, but to create a simple "future self" simulation experience. Users can change one habit, such as increasing sleep or reducing screen time, and immediately see how the projected outcome improves.

**Live Link: https://mlprojfutureyousimulator.streamlit.app/**

Project Overview
The system accepts daily habit values as input and produces:

- A productivity score from 0 to 100
- A burnout risk label: LOW, MEDIUM, or HIGH
- A six-month productivity projection graph
- A comparison between current habits and improved habits
- Simple future advice based on the predicted risk
This makes the project useful for academic demonstrations, beginner machine learning practice, and interactive storytelling around health, productivity, and behavior change.

**Machine Learning Approach:**
The project uses synthetic data because a direct public dataset for this exact habit-to-future-outcome problem is not commonly available. The synthetic dataset is generated using rule-based logic that reflects realistic assumptions:

- More sleep generally improves productivity.
- More focused study or work time improves productivity.
- Regular exercise improves energy and productivity.
- Excessive screen time reduces productivity.
- Very low sleep and high screen time increase burnout risk.
- Imbalanced routines create medium or high burnout risk.

Two machine learning models are trained:
- RandomForestRegressor predicts the productivity score.
- RandomForestClassifier predicts the burnout risk category.
The trained models are saved as .pkl files and loaded by the Streamlit app during prediction.


