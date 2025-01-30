from pathlib import Path

import pytest
import pandas as pd

from verfishd import StimuliProfile


@pytest.fixture
def dataframe_stimuli_fixture():
    return pd.DataFrame({'depth': [0, 1, 2, 3, 4, 5], 'temperature': [7.0, 6.0, 5.0, 4.5, 4.0, 3.9]})


def test_initialization_with_dataframe(dataframe_stimuli_fixture):
    stimuli_profile = StimuliProfile(dataframe_stimuli_fixture)
    assert stimuli_profile.columns.to_list() == ['depth',
                                                 'temperature'], ("StimuliProfile should be initialized with the "
                                                                  "correct DataFrame")


def test_add_entry_for_depth_3dot5_should_end_up_at_index_loc_3dot5(dataframe_stimuli_fixture):
    stimuli_profile = StimuliProfile(dataframe_stimuli_fixture)
    stimuli_profile.add_entry(3.5, {'temperature': 4.25})
    assert stimuli_profile.data['temperature'].loc[3.5] == 4.25, "StimuliProfile should add a new entry for depth 3.5"


def test_throw_an_error_when_add_entry_is_called_with_unknown_column(dataframe_stimuli_fixture):
    stimuli_profile = StimuliProfile(dataframe_stimuli_fixture)
    with pytest.raises(ValueError):
        stimuli_profile.add_entry(3.5, {'pressure': 4.25})


def test_throw_an_error_when_initialized_with_an_dataframe_without_depth():
    with pytest.raises(ValueError):
        StimuliProfile(pd.DataFrame({'temperature': [7.0, 6.0, 5.0, 4.5, 4.0, 3.9]}))


def test_create_a_profile_from_file():
    csv_file = Path(__file__).parent / "fixtures" / "temperature_stimuli.csv"
    stimuli_profile = StimuliProfile.read_from_tabular_file(csv_file)
    assert isinstance(stimuli_profile, StimuliProfile), "StimuliProfile should be created from a file"
