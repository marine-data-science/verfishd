import pytest
from verfishd import PhysicalFactor


@pytest.fixture
def temperature_factor_fixture():
    # Define a custom PhysicalFactor
    class Temperature(PhysicalFactor):
        """
        A class representing a temperature factor.

        Parameters
        ----------
        weight : float
            The weight is used to scale the factor's contribution to the evaluation function E.
        """

        def __init__(self, weight: float):
            super().__init__("temperature", weight)

        def _calculate(self, value: float) -> float:
            match value:
                case _ if value > 5:
                    return 0.0
                case _ if value < 4:
                    return -1.0
                case _:
                    return value - 5.0

    return lambda weight: Temperature(weight)

@pytest.fixture
def pressure_factor_fixture():
    # Define a custom PhysicalFactor
    class Pressure(PhysicalFactor):
        """
        A class representing a pressure factor.

        Parameters
        ----------
        weight : float
            The weight is used to scale the factor's contribution to the evaluation function E.
        """

        def __init__(self, weight: float):
            super().__init__("pressure", weight)

        def _calculate(self, value: float) -> float:
            match value:
                case _ if value > 1000:
                    return 1.0
                case _ if value < 980:
                    return -1.0
                case _:
                    return 0

    return lambda weight: Pressure(weight)
