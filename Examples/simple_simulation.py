import pandas as pd
from verfishd import VerFishDModel, PhysicalFactor, StimuliProfile


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


# Create a Stimuli Profile including depth and temperature
stimuli = StimuliProfile(pd.DataFrame({ 'depth': [0.0, 1.0, 2.0, 3.0, 4.0, 5.0], 'temperature': [7.0, 6.0, 5.0, 5.4, 4.0, 3.9] }))

# Create a VerFishDModel with the temperature factor
temperature_factor = Temperature(1.0)

# Define a very simple migration speed function
migration_speed = lambda x: x

# Create the model
model = VerFishDModel(stimuli, migration_speed, [temperature_factor])

# Simulate the model for 30 steps
model.simulate(30)

print(model.steps['t=30'])
