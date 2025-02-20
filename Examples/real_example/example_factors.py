from verfishd import PhysicalFactor

class Temperature(PhysicalFactor):
    def __init__(self, name: str, weight: float):
        super().__init__(name, weight)

    def _calculate(self, value: float) -> float:
        match value:
            case _ if value > 5:
                return 0.0
            case _ if value < 4:
                return -1.0
            case _:
                return value - 5.0

class Oxygen(PhysicalFactor):
    def __init__(self, name: str, weight: float):
        super().__init__(name, weight)

    def _calculate(self, value: float) -> float:
        match value:
            case _ if value > 0.7:
                return 0.0
            case _ if value < 0.2:
                return 1.0
            case _:
                return -value + 1.2

class Light(PhysicalFactor):
    def __init__(self, name: str, weight: float):
        super().__init__(name, weight)

    def _calculate(self, value: float) -> float:
        match value:
            case _ if value < 0.005:
                return 1.0
            case _ if value >= 0.005 and value < 0.1:
                return -200/19 * value + 20/19
            case _ if value >= 0.1 and value < 10:
                return 0.0
            case _ if value >= 10 and value < 200:
                return -1/190 * value + 1/19
            case _:
                return -1.0

class TemperatureGradient(PhysicalFactor):
    def __init__(self, name: str, weight: float):
        super().__init__(name, weight)

    def _calculate(self, value: float) -> float:
        match value:
            case _ if value < -4:
                return -1.0
            case _ if value > -1.5:
                return 0
            case _:
                return 0.4 * value + 0.6
