import pytest

from app.ml.prediction import get_sample_prediction


@pytest.fixture
def prediction():
    return get_sample_prediction()
