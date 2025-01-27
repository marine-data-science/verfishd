import pytest
from VerFishD import PhysicalFactor


class ExampleFactor(PhysicalFactor):
    def __init__(self, weight: float):
        super().__init__("example", weight)

    def _calculate(self, value: float) -> float:
        return value * 2


def test_throw_when_weight_is_not_number():
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        ExampleFactor("not a number")


def test_throw_when_calculate_is_called_with_non_number():
    factor = ExampleFactor(1.0)
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        factor.calculate("not a number")


def test_return_a_value_when_calculate_is_called():
    factor = ExampleFactor(1.0)
    result = factor.calculate(1)
    assert isinstance(result, float), ".calculate() should return a float"
    assert result == 2.0, ".calculate() should return the correct value"
