FEATURE_COLUMNS = [
    "sleep_hours",
    "study_hours",
    "screen_time",
    "exercise",
    "social_time",
]

BURNOUT_LABELS = {
    0: "LOW",
    1: "MEDIUM",
    2: "HIGH",
}


def clamp(value, lower, upper):
    return max(lower, min(upper, value))

