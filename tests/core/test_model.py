import pytest
import pandas as pd
import numpy as np
from verfishd  import VerFishDModel, PhysicalFactor


@pytest.fixture
def verfishd_model_fixture(temperature_factor_fixture, temperature_stimuli_fixture, migration_speed_fixture):
    temperature_factor = temperature_factor_fixture(1.0)
    # Instantiate VerFishDModel
    model = VerFishDModel(
        stimuli_profile=temperature_stimuli_fixture,
        migration_speed=migration_speed_fixture,
        factors=[temperature_factor]
    )

    return model, temperature_stimuli_fixture, migration_speed_fixture, [temperature_factor]


def test_steps_initialization(verfishd_model_fixture):
    model, _, _, _ = verfishd_model_fixture

    # Check that steps are initialized to 1
    assert (model.steps["t=0"] == 1.0).all(), "All steps should be initialized to 1.0"


def test_factors_are_initialized_correctly(verfishd_model_fixture):
    model, _, _, factors = verfishd_model_fixture

    # Test that the factors are correctly assigned
    assert model.factors == factors, "Factors should be assigned correctly"


def test_stimuli_profile_is_assigned(verfishd_model_fixture):
    model, stimuli_profile_mock, _, _ = verfishd_model_fixture

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
        VerFishDModel(temperature_stimuli_fixture, migration_speed_fixture, [my_factor]) # type: ignore

def test_weighted_sum_is_calculated_during_initialisation(temperature_stimuli_fixture, migration_speed_fixture, temperature_factor_fixture, pressure_factor_fixture):
    model = VerFishDModel(
        stimuli_profile=temperature_stimuli_fixture,
        migration_speed=migration_speed_fixture,
        factors=[temperature_factor_fixture(0.4), pressure_factor_fixture(0.6)]
    )

    expected_result = pd.Series(data=[0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.4, 0.28, 0.2, 0.2], index=model.weighted_sum.index)

    assert model.weighted_sum.index.name == expected_result.index.name, "Index name should be the same"
    assert model.weighted_sum.dtype == expected_result.dtype, "Data type should be the same"
    assert np.allclose(model.weighted_sum, expected_result, atol=1e-8), "Weighted sum should be calculated during initialization"

def test_do_the_simulation_correctly_for_a_single_step(temperature_stimuli_fixture, migration_speed_fixture, temperature_factor_fixture):
    nr_of_steps = 1
    model = VerFishDModel(
        stimuli_profile=temperature_stimuli_fixture,
        migration_speed=migration_speed_fixture,
        factors=[temperature_factor_fixture(1.0)]
    )

    model.simulate(number_of_steps=nr_of_steps)

    expected_result = pd.Series(data=[1, 1, 1, 1, 1, 1, 1, 0.5, 0.7, 0.8, 2.0], index=model.steps.index)

    assert model.steps.index.name == expected_result.index.name, "Index name should be the same"
    assert np.allclose(model.steps[f"t={nr_of_steps}"], expected_result, atol=1e-8), "Simulation should be correct for a single step"

def test_convert_to_reasonable_result_for_a_several_step(temperature_stimuli_fixture, migration_speed_fixture, temperature_factor_fixture):
    nr_of_steps = 30
    model = VerFishDModel(
        stimuli_profile=temperature_stimuli_fixture,
        migration_speed=migration_speed_fixture,
        factors=[temperature_factor_fixture(1.0)]
    )

    model.simulate(number_of_steps=nr_of_steps)

    expected_result = pd.Series(data=[1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 4.0], index=model.steps.index)

    assert model.steps.index.name == expected_result.index.name, "Index name should be the same"
    assert np.allclose(model.steps[f"t={nr_of_steps}"], expected_result, atol=1e-8), "Simulation should be correct for a single step"
