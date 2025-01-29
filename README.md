<p align="center">
  <img src="images/logo/square_logo.png" alt="Logo of VerFishD">
</p>

**VerFishD** is a library to do vertical fish distribution simulations influenced by physical stimuli.
It is still in development and not yet ready for production.

## Concept
The library uses `PhysicalFactor` which influence the movement of the fish.
They can be created by implement this base class for your own physical factors like temperature, light, oxygen, et cetera.
The next step would be to load a `StimuliProfile` which is a collection of concrete stimuli values.

## Example

https://github.com/marine-data-science/verfishd/blob/752e3501ce62ffe1b563d25e3a7783d529d1aba2/Examples/simple_simulation.py#L5-L46

## Installation

```bash
pip install verfishd
```
