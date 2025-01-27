from typing import List
from collections.abc import  Callable
from .physical_factor import PhysicalFactor
from .physical_stimuli_profile import StimuliProfile
import pandas as pd


class VerFishDModel:
    """A class representing a model that manages multiple PhysicalFactors."""

    def __init__(
            self,
            stimuli_profile: StimuliProfile,
            migration_speed: Callable[[float], float],
            factors: List[PhysicalFactor]
    ):
        """
        Initialize the VerFishDModel with optional PhysicalFactor instances.

        Parameters
        ----------
        stimuli_profile: panda dataframe
            a dataframe with depth specific physical stimuli information
        migration_speed: Callable[[float], float]
            the migration speed function for the current model. For example
            .. math::
                w_{fin} = w_{max} * w_{beh} = \frac{(\zeta_d + E)|\zeta_d + E|}{h + (\zeta_d + E)^2}
        factors : list of PhysicalFactor, optional
            A list of PhysicalFactor instances (optional).
        """
        self.migration_speed = migration_speed
        self.__check_factors(factors, stimuli_profile)
        self.__init_steps()

    def __init_steps(self):
        self.steps = pd.DataFrame(index=self.stimuli_profile.data.index)
        self.steps['t=0'] = 1.0

    def __check_factors(self, factors: List[PhysicalFactor], stimuli_profile: StimuliProfile):
        if not all(isinstance(factor, PhysicalFactor) for factor in factors):
            raise TypeError("All elements in 'factors' must be instances of PhysicalFactor.")

        if not all(factor.name in stimuli_profile.columns for factor in factors):
            raise ValueError("All factor names must be present in the stimuli profile columns.")

        self.factors = factors
        self.stimuli_profile = stimuli_profile

    def calculate_all(self, value: float) -> List[float]:
        """
        Calculate results for all factors with the given value.

        Parameters
        ----------
        value:  float
            A numeric input for the calculations.

        Returns
        -------
        List[float]
            A list of calculation results.
        """
        return [factor.calculate(value) for factor in self.factors]
