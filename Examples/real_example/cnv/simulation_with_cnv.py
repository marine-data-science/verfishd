from verfishd import StimuliProfile, migration_speed_with_demographic_noise, VerFishDModel
from ..example_factors import Temperature, Oxygen

profile = StimuliProfile.read_from_cnv("Examples/example.cnv")

factors = [Temperature('tv290C', 0.48), Oxygen('oxygen_ml_L', 0.52)]

model = VerFishDModel('Example', profile, migration_speed_with_demographic_noise, factors)

model.simulate(18000)
# model.save_result("Examples/results.csv")

model.plot()
