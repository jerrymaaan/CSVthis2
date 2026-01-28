# CSVthis: Can Someone Visualize this?

___

A graphical user interface for analysing data from CSV files.
Primarily dedicated to the project Oelek.

Author: Jeremias Friedel

Version: 2.0.3

___

## Dependencies

- ``pandas``
- ``dash``
- ``plotly``

## How to use

1. Install all required dependencies.
2. Start the application by running `app.py`.
3. Adapt `config.json` to match your CSV file structure.
   For supported time formats, see the Python documentation
   [here](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior).
   If the time column contains only a sequential number (e.g. `1, 2, 3, ...`),
   set the time format to `null`.
4. Select the file you want to plot (e.g. `test_data.csv`).
   Files with the extension `.txt` or without any file extension may also work.
5. Use the dropdown menus to choose which data should be displayed.

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
