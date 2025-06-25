import matplotlib.pyplot as plt
import os

from Examples.real_example.example_factors import Oxygen, Temperature, TemperatureGradient, Light
from verfishd import VerFishDModel, StimuliProfile, migration_speed_with_demographic_noise

data_file = f"{os.path.dirname(__file__)}/aggregated_data_8A.csv"
profile = StimuliProfile.read_from_tabular_file(data_file)

model = VerFishDModel(
    'Hol 8A',
    profile,
    migration_speed_with_demographic_noise,
    [
        Oxygen('oxygen', 0.52),
        Temperature('temperature', 0.14),
        TemperatureGradient('temperature_gradient', 0.14),
        Light('light', 0.2)]
)

model.simulate(800)

model.plot()
plt.show()
