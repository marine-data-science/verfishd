# VerFishD
<p align="center">
  <img src="/images/logo/square_logo.png" alt="Logo of VerFishD">
</p>

**VerFishD** is a library for simulating vertical fish distribution under the influence of physical stimuli.

![PyPI - Version](https://img.shields.io/pypi/v/verfishd)
![Tests - Status](https://github.com/marine-data-science/verfishd/actions/workflows/pytest.yml/badge.svg)

## Concept

VerFishD uses `PhysicalFactor` objects to influence fish movement. You can implement this base class to define your own physical factors, such as temperature, light, oxygen, etc. The next step is to load a `StimuliProfile`, which represents a collection of specific stimulus values. The migration speed function determines the final vertical movement of the fish. The sign of this function determines the movement direction, while the absolute value indicates the percentage of fish that will move. These values are combined to simulate the vertical distribution of fish over time.

## Installation

VerFishD is available on PyPI and can be installed using Poetry or pip:

```bash
poetry add verfishd
```

or with pip:

```bash
pip install verfishd
```

## Usage

Here is a simple example of how to use VerFishD:

https://github.com/marine-data-science/verfishd/blob/752e3501ce62ffe1b563d25e3a7783d529d1aba2/Examples/simple_simulation.py#L5-L46

https://github.com/marine-data-science/verfishd/blob/752e3501ce62ffe1b563d25e3a7783d529d1aba2/Examples/simple_simulation.py#L5-L50

This example defines a temperature factor, creates a stimuli profile with temperature data over depth, initializes the model with this profile and factor, runs a simulation over 800 time steps, and finally plots the results.

## Features

- **Modularity**: Implement custom physical factors that influence fish movement.
- **Flexibility**: Load different stimuli profiles to simulate various environmental conditions.
- **Visualization**: Plot functions to display simulation results.

## Example Plot

![Example plot of the simulation](images/example_plot.png)

## Running Tests

To run tests, use:

```bash
pytest
```

## Ideas for the future
- [ ] Combine multiple Stimuli Profiles to do a simulation for a whole day
- [ ] Algorithm to determine if simulation can end?


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
