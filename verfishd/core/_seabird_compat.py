"""Compatibility helpers for seabird on setuptools versions without pkg_resources."""

from __future__ import annotations

from importlib import import_module
from importlib.metadata import PackageNotFoundError, distribution
from importlib.resources import files
from pathlib import PurePosixPath
import sys
from types import ModuleType
from typing import Any


def _resource(package_or_requirement: str, resource_name: str) -> Any:
    module = import_module(package_or_requirement)
    anchor = module if hasattr(module, "__path__") else module.__package__
    if anchor is None:
        raise TypeError(f"Cannot resolve resources for {package_or_requirement!r}")

    return files(anchor).joinpath(*PurePosixPath(resource_name).parts)


def _resource_string(package_or_requirement: str, resource_name: str) -> bytes:
    """Implement pkg_resources.resource_string via importlib.resources."""
    return _resource(package_or_requirement, resource_name).read_bytes()


def _resource_listdir(package_or_requirement: str, resource_name: str) -> list[str]:
    """Implement pkg_resources.resource_listdir via importlib.resources."""
    return [entry.name for entry in _resource(package_or_requirement, resource_name).iterdir()]


def load_fcnv() -> Any:
    """Load seabird.fCNV without requiring the removed pkg_resources module."""
    try:
        from seabird import fCNV
    except ModuleNotFoundError as error:
        if error.name != "pkg_resources":
            raise

        compatibility_module = ModuleType("pkg_resources")
        compatibility_module.DistributionNotFound = PackageNotFoundError
        compatibility_module.get_distribution = distribution
        compatibility_module.resource_listdir = _resource_listdir
        compatibility_module.resource_string = _resource_string
        sys.modules["pkg_resources"] = compatibility_module

        try:
            from seabird import fCNV
        finally:
            if sys.modules.get("pkg_resources") is compatibility_module:
                del sys.modules["pkg_resources"]

    return fCNV
