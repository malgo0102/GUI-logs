# Log viewer and visualizer

- Reads log files in csv format-like
- Represents them in GUI
- Includes search engine
- Includes statistics: max and min value 
- Visualizes data in a form of a plot

Test log files are provided in "root/logs".

## In the configuration file: 
- The separator must be surrounded by quotes "
"Separators longer than 1 character and different from '\s+' will be interpreted as regular expressions and will also force the use of the Python parsing engine." https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
- Labels must be stored in a list.

I used Tkinter standard GUI package (it is built into standard Python library), Pandas, Matplotlib Pyplot and Configparser.

1. Install Matplotlib:
    - https://matplotlib.org/users/installing.html

2. Install Pandas:
    - https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html

3. Run the program in the root directory: 
    - python main.py

//malg0102



