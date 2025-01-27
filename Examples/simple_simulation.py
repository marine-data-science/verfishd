from VerFishD import VerFishDModel, PhysicalFactor, StimuliProfile


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
stimuli = StimuliProfile(['depth', 'temperature'])
stimuli.add_entry(0.0, {'temperature': 7.0})
stimuli.add_entry(1.0, {'temperature': 6.0})
stimuli.add_entry(2.0, {'temperature': 5.0})
stimuli.add_entry(3.0, {'temperature': 4.5})
stimuli.add_entry(4.0, {'temperature': 4.0})
stimuli.add_entry(5.0, {'temperature': 3.9})

# Create a VerFishDModel with the temperature factor
temperature_factor = Temperature(1.0)
migration_speed = lambda x: x*2
model = VerFishDModel(stimuli, migration_speed, [temperature_factor])

print(model.steps['t=0'])
