from pathlib import Path

import pytest
from verfishd import StimuliProfile


@pytest.fixture
def temperature_stimuli_fixture() -> StimuliProfile:
    csv_file = Path(__file__).parent / "temperature_stimuli.csv"
    stimuli_profile = StimuliProfile.read_from_file(csv_file)

    return stimuli_profile
