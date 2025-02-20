import os
from verfishd import StimuliProfile, migration_speed_with_demographic_noise, VerFishDModel
from Examples.real_example.example_factors import Oxygen, Temperature
from matplotlib import pyplot as plt

data_file = f"{os.path.dirname(__file__)}/example.cnv"
profile = StimuliProfile.read_from_cnv(data_file)

factors = [Temperature('tv290C', 0.48), Oxygen('oxygen_ml_L', 0.52)]

model = VerFishDModel('Example', profile, migration_speed_with_demographic_noise, factors)

model.simulate(2000)

model.plot()

plt.show()
