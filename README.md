# CSVthis: Can Someone Visualize this?

___

A graphical user interface for analysing data from CSV files.
Primarily dedicated to the project Oelek.

Author: Jeremias Friedel

Version: 2.0.3

___

## Requirements

- ``pandas``
- ``dash``
- ``plotly``

## How to use

1. Install all requirements.
2. Start ``app.py``.
3. Choose your file to be plotted (e.g. ``test_data.csv``). Extension ``.txt`` or no file extension may also work.
4. Use the dropdown menus to choose which data to display.

## Own calculations

Check ``calculation.py`` to create your own calculations on your data.
Every function you add must:

- take ``df`` (type: ``pandas.DataFrame``) as its only parameter
- return a value with the same length as the dataframe

The return value can be one of the following types:

- ``pandas.Series``
- ``numpy.ndarray``
- ``list``
- ``int`` or ``str`` (used to fill all rows with the same value)
