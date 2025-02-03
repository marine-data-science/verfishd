from verfishd import StimuliProfile, PhysicalFactor, migration_speed_with_demographic_noise, VerFishDModel

profile = StimuliProfile.read_from_cnv("Examples/example.cnv")

class Temperature(PhysicalFactor):
    def __init__(self, weight: float):
        super().__init__("tv290C", weight)

    def _calculate(self, value: float) -> float:
        match value:
            case _ if value > 5:
                return 0.0
            case _ if value < 4:
                return -1.0
            case _:
                return value - 5.0

class Oxygen(PhysicalFactor):
    def __init__(self, weight: float):
        super().__init__("oxygen_ml_L", weight)

    def _calculate(self, value: float) -> float:
        match value:
            case _ if value > 0.7:
                return 0.0
            case _ if value < 0.2:
                return 1.0
            case _:
                return -value + 1.2

factors = [Temperature(0.48), Oxygen(0.52)]

model = VerFishDModel(profile, migration_speed_with_demographic_noise, factors)

model.simulate(500)
# model.save_result("Examples/results.csv")

model.plot(True)
