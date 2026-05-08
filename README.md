# Future You Simulator

An interactive behavior-to-outcome predictor. Users enter daily habits, then the app predicts productivity, burnout risk, and a six-month trajectory.

## Setup

```powershell
cd future-you-simulator
pip install -r requirements.txt
python model/generate_data.py
python model/train.py
streamlit run app/app.py
```

On this machine, the app can also be started with:

```powershell
.\run_app.ps1
```

Then open http://localhost:8501.

## Inputs

- Sleep hours
- Study hours
- Screen time
- Exercise hours
- Social time

## Outputs

- Productivity score from 0 to 100
- Burnout risk: LOW, MEDIUM, or HIGH
- Six-month projection graph
- Improved-habits comparison
- Simple advice generator
