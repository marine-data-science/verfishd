from collections.abc import  Callable
from .physical_factor import PhysicalFactor
from .physical_stimuli_profile import StimuliProfile
import pandas as pd


class VerFishDModel:
    """
    A class representing a model that manages multiple PhysicalFactors.
    """

    def __init__(
            self,
            stimuli_profile: StimuliProfile,
            migration_speed: Callable[[float], float],
            factors: list[PhysicalFactor]
    ):
        """
        A class representing a model that manages multiple PhysicalFactors.

        Parameters
        ----------
        stimuli_profile : pandas.DataFrame
            A dataframe with depth-specific physical stimuli information.
        migration_speed : Callable[[float], float]
            The migration speed function for the current model. For example:

            .. math::

                w_{fin} = w_{max} * w_{beh} = \\frac{{(\\zeta_d + E)|\\zeta_d + E|}}{{h + (\\zeta_d + E)^2}}

        factors : list of PhysicalFactor, optional
            A list of PhysicalFactor instances (optional).
        """
        self.migration_speed = migration_speed
        self.__check_factors(factors, stimuli_profile)
        self.__init_steps()
        self.weighted_sum = self.__calculate_weighted_sum()

    def __init_steps(self):
        self.steps = pd.DataFrame(index=self.stimuli_profile.data.index)
        self.steps['t=0'] = 1.0

    def __check_factors(self, factors: list[PhysicalFactor], stimuli_profile: StimuliProfile):
        """
        Validate factors and initialize the stimuli profile.

        Parameters
        ----------
        factors : List[PhysicalFactor]
            A list of PhysicalFactor instances.
        stimuli_profile : StimuliProfile
            The stimuli profile containing relevant data.

        Raises
        ------
        TypeError
            If any element in 'factors' is not an instance of PhysicalFactor.
        ValueError
            If the factor names are not in the stimuli profile columns.
        ValueError
            If the sum of all factor weights is not equal to 1.
        """
        if not all(isinstance(factor, PhysicalFactor) for factor in factors):
            raise TypeError("All elements in 'factors' must be instances of PhysicalFactor.")

        if not all(factor.name in stimuli_profile.columns for factor in factors):
            raise ValueError("All factor names must be present in the stimuli profile columns.")

        total_weight = sum(factor.weight for factor in factors)
        if not abs(total_weight - 1.0) < 1e-6:  # floating point comparison
            raise ValueError(f"The sum of all factor weights must be 1.0, but got {total_weight:.6f}.")

        self.factors = factors
        self.stimuli_profile = stimuli_profile

    def __calculate_weighted_sum(self):
        """
        Calculate the weighted sum of the factors for each depth.

        Returns
        -------
        pd.Series
            The weighted sum for each depth.
        """
        weighted_sum = pd.Series(0.0, index=self.stimuli_profile.data.index)

        for depth, row in self.stimuli_profile.data.iterrows():
            total = 0.0
            for factor in self.factors:
                value = row[factor.name]
                total += factor.weight * factor.calculate(float(value))
            weighted_sum[depth] = total

        return weighted_sum

    def simulate(self, number_of_steps: int = 1000):
        """
        Simulate the model for a given number of steps.

        Parameters
        ----------
        number_of_steps: int, optional
            The number of steps to simulate the model for.
        """
        for step in range(0, number_of_steps):
            current = self.steps[f"t={step}"]
            next_step = pd.Series(0.0, index=current.index)

            for depth in current.index:
                weight_sum = self.weighted_sum[depth]
                migration_speed = self.migration_speed(float(weight_sum))

                if migration_speed > 0 and depth - 1 in current.index:
                    # move upwards
                    migrated_value = migration_speed * current[depth]
                    next_step[depth] += current[depth] - migrated_value
                    next_step[depth - 1] += migrated_value
                elif migration_speed < 0 and depth + 1 in current.index:
                    # move downwards
                    migrated_value = abs(migration_speed) * current[depth]
                    next_step[depth] += current[depth] - migrated_value
                    next_step[depth + 1] += migrated_value
                else:
                    # no migration
                    next_step[depth] += current[depth]

            # normalize the overall mass
            total_current = next_step.sum()
            if total_current > 0:
                next_step = next_step / total_current * current.sum()

            self.steps[f"t={step+1}"] = next_step
