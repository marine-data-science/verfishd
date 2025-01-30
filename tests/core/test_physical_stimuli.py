from pathlib import Path

import pytest
import pandas as pd

from verfishd import StimuliProfile


@pytest.fixture
def dataframe_stimuli_fixture():
    return pd.DataFrame({
        'depth': [0, 1, 2, 3, 4, 5],
        'temperature': [7.0, 6.0, 5.0, 4.5, 4.0, 3.9]
    })


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


@pytest.mark.parametrize("stimuli, expected_exception", [
    (pd.Series([0.0, 0.1, 0.2, 0.3, 0.4, 0.5], index=[0, 1, 2, 3, 4, 5], name='oxygen'), None),  # Valid case
    (pd.Series([0.0, 0.1, 0.2, 0.3, 0.4, 0.5], index=[0, 1, 2, 3, 5, 6], name='oxygen'), ValueError("Stimuli series 'depth' values must match the existing data.")),  # Mismatched index
])
def test_add_stimuli(dataframe_stimuli_fixture, stimuli, expected_exception):
    stimuli_profile = StimuliProfile(dataframe_stimuli_fixture)
    if expected_exception:
        with pytest.raises(type(expected_exception)) as exec_info:
            stimuli_profile.add_stimuli(stimuli)
        assert str(exec_info.value) == str(expected_exception)
    else:
        stimuli_profile.add_stimuli(stimuli)
        assert 'oxygen' in stimuli_profile.data.columns
        assert (stimuli_profile.data['oxygen'] == stimuli).all()
