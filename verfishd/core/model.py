from .physical_factor import PhysicalFactor
from .physical_stimuli_profile import StimuliProfile
from collections.abc import  Callable
from itertools import repeat
from matplotlib import pyplot as plt
from os import PathLike
import numpy as np
import pandas as pd


class VerFishDModel:
    """
    A class representing a model that manages multiple PhysicalFactors.
    """

    steps: pd.DataFrame
    result: pd.Series

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
            raise ValueError(f"All factor names must be present in the stimuli profile columns. Present columns: {stimuli_profile.columns}")

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
        Simulate the model for a given number of steps, continuing from the last recorded step.

        Parameters
        ----------
        number_of_steps: int, optional
            The number of steps to simulate the model for.
        """
        if not hasattr(self, 'steps') or self.steps.empty:
            raise ValueError("Simulation cannot continue without initial state.")

        # Determine starting point
        last_step_index = self.steps.shape[1] - 1
        steps_list = [self.steps.iloc[:, -1].copy()]

        # Precompute migration speeds for all depths
        migration_speeds = np.vectorize(self.migration_speed)(self.weighted_sum.values)

        for _ in repeat(None, number_of_steps):
            current = steps_list[-1]
            next_step = pd.Series(0.0, index=current.index)

            # Compute migration changes first
            migrated_up = np.zeros_like(current.values)
            migrated_down = np.zeros_like(current.values)

            up_mask = (migration_speeds > 0)
            down_mask = (migration_speeds < 0)

            migrated_values = np.abs(migration_speeds) * current.values

            migrated_up[:-1] += migrated_values[1:] * up_mask[1:]
            migrated_up[1:] -= migrated_values[1:] * up_mask[1:]

            migrated_down[1:] += migrated_values[:-1] * down_mask[:-1]
            migrated_down[:-1] -= migrated_values[:-1] * down_mask[:-1]

            # Apply migration
            next_step += current + migrated_up + migrated_down

            # Normalize total mass to conserve population
            total_current = next_step.sum()
            if total_current > 0:
                next_step *= current.sum() / total_current

            steps_list.append(next_step)

        # Append results to existing DataFrame
        new_steps = pd.concat(steps_list[1:], axis=1)
        new_steps.columns = [f"t={t}" for t in range(last_step_index + 1, last_step_index + number_of_steps + 1)]

        self.steps = pd.concat([self.steps, new_steps], axis=1)

        self.result = self.steps.iloc[:, -1]
        self.result.name = "Fish Probability"

    def plot(self, dry_out: bool = False) -> None:
        """
        Plot the simulation result.
        """
        simulation_result = self.result
        if dry_out:
            # TODO: This is a temporary fix
            simulation_result = simulation_result[simulation_result >= 1e-3].iloc[::10] # pyright: ignore

        plt.figure(figsize=(8, 5))
        plt.plot(simulation_result.to_numpy(), -simulation_result.index, label="Depth Values", color='b')
        plt.ylabel("Depth")
        plt.xlabel("Fish Probability")
        plt.title("Simulation Result")
        plt.legend()
        plt.grid(True, which="both", linestyle="--", linewidth=0.5)

        plt.show()

    def save_result(self, file_path: str | PathLike[str]) -> None:
        """
        Save the simulation result to a file.

        Parameters
        ----------
        file_path: str
            The path to the file.
        """
        self.result.to_csv(file_path)
