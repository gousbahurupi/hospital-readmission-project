"""Sample prediction used by the demo page and tests.

In production the prediction comes from your readmission model. Send that
output to POST /agent/ask together with the user's question. Replace or
delete this module once the real model is wired in.
"""


def get_sample_prediction() -> dict:
    return {
        "readmission_prediction": "LIKELY",
        "risk_probability": 72,
        "risk_level": "HIGH",
        "top_contributing_factors": [
            "A1C result",
            "Number of diagnoses",
            "Time in hospital",
            "Medication-related factors",
        ],
    }
