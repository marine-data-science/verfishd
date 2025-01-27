from __future__ import annotations
from os import PathLike

import numpy
import pandas as pd
from typing import Dict, Any


class StimuliProfile:
    """A class for managing tabular stimuli data with a required 'depth' index."""

    columns: numpy.array
    data: pd.DataFrame

    def __init__(self, data: pd.DataFrame):
        """
        Initialize the StimuliTable with given data.

        Parameters
        ----------
        data: Dict[str, Any]
            The stimuli profile data
        """
        if 'depth' not in data.columns:
            raise ValueError("'depth' must be included as a column.")

        self.columns = data.columns
        self.data = data.set_index('depth')

    def add_entry(self, depth: float, data: Dict[str, Any]) -> None:
        """
        Add a row of data, indexed by 'depth'.

        :param depth: The depth value for this row.
        :param data: A dictionary of column values (excluding 'depth').
        """
        if not all(col in self.columns for col in data.keys()):
            raise ValueError(f"Invalid columns in data. Expected columns: {self.columns}")

        self.data.loc[depth] = data

    @classmethod
    def read_from_file(cls, file_path: str | PathLike[str], file_type: str = "csv") -> StimuliProfile:
        """
        Read stimuli data from a file and populate the table.

        :param file_path: The path to the file.
        :param file_type: The file type ('csv', 'excel'). Default is 'csv'.
        :raises ValueError: If the file type is unsupported.
        """
        if file_type == "csv":
            df = pd.read_csv(file_path)
        elif file_type == "excel":
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file type. Use 'csv' or 'excel'.")

        return cls(df)
