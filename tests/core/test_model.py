import pytest
import pandas as pd
from unittest.mock import Mock
from verfishd  import VerFishDModel, PhysicalFactor, StimuliProfile


@pytest.fixture
def verfishd_model_fixture(temperature_factor_fixture, temperature_stimuli_fixture, migration_speed_fixture):
    # Instantiate VerFishDModel
    model = VerFishDModel(
        stimuli_profile=temperature_stimuli_fixture,
        migration_speed=migration_speed_fixture,
        factors=[temperature_factor_fixture]
    )

    return model, temperature_stimuli_fixture, migration_speed_fixture, [temperature_factor_fixture]


def test_steps_initialization(verfishd_model_fixture):
    model, stimuli_profile_mock, migration_speed_mock, factors = verfishd_model_fixture

    # Check that steps are initialized to 1
    assert (model.steps["t=0"] == 1.0).all(), "All steps should be initialized to 1.0"


def test_factors_are_initialized_correctly(verfishd_model_fixture):
    model, stimuli_profile_mock, migration_speed_mock, factors = verfishd_model_fixture

    # Test that the factors are correctly assigned
    assert model.factors == factors, "Factors should be assigned correctly"


def test_stimuli_profile_is_assigned(verfishd_model_fixture):
    model, stimuli_profile_mock, migration_speed_mock, factors = verfishd_model_fixture

    # Test that the stimuli_profile is correctly assigned
    assert model.stimuli_profile == stimuli_profile_mock, "StimuliProfile should be assigned correctly"


def test_factor_not_in_stimuli_profile_should_throw(temperature_stimuli_fixture, migration_speed_fixture):
    class ExampleFactor(PhysicalFactor):
        def __init__(self, weight: float):
            super().__init__("example", weight)

        def _calculate(self, value: float) -> float:
            return value * 2

    my_factor = ExampleFactor(1.0)

    with pytest.raises(ValueError):
        VerFishDModel(temperature_stimuli_fixture, migration_speed_fixture, [my_factor])


def test_throw_when_factor_is_not_subclass_of_PhysicalFactor(temperature_stimuli_fixture, migration_speed_fixture):
    class ExampleFactor:
        def __init__(self, weight: float):
            self.weight = weight

        def _calculate(self, value: float) -> float:
            return value * 2

    my_factor = ExampleFactor(1.0)

    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        VerFishDModel(temperature_stimuli_fixture, migration_speed_fixture, [my_factor])
