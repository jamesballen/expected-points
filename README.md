# README

This is a Python3 project for football analytics. It involves processing data from two CSV files: one containing expected goals (xG) shot data for arsenal fixtures, and one containing Arsenal's Premier League results. The script calculates the total xG for both Arsenal and their opponents in each match and compares it to the actual goals scored to determine if Arsenal over- or underperformed relative to their xG.

## Libraries Used

- `pandas`: used for data manipulation and analysis.
- `random`: used to simulate matches by generating random numbers.

## Guide

### Getting Started

- Clone the repository to your local machine.
- Open your terminal and navigate to the project directory.
- Run `python3 app.py` to start the script.
- When prompted, enter the file path for the xG shot data file, the Arsenal results data file and the number of match simulations you would like to run. See "Input Data" section for details.

### Functions

- `validate_xg_shot_data`: a function that checks that the provided xg_shots_data file is in the correct format and has the correct columns and datatypes.
- `validate_results_data`: a function that checks that the provided arsenal_results_data file is in the correct format and has the correct columns and datatypes.
- `create_dict`: a function that takes a group of rows from the shot_data dataframe and returns a dictionary of shot_xG values grouped by team_shot.
- `get_home_xg`: a function that takes a row from the results_data dataframe and returns a list of shot_xG values for the home team.
- `get_away_xg`: a function that takes a row from the results_data dataframe and returns a list of shot_xG values for the away team.
- `sum_list`: a function that takes a list of numbers and returns the sum of those numbers.
- `simulate_match`: a function that takes a row from the results_data dataframe and simulates a match by generating random numbers and comparing them to the shot_xG values for each team. It returns the expected points for the home and away teams.

### Workflow

- The `shot_data` dataframe is grouped by `matchweek`, `team_home`, `team_away`, and `team_shot`, and a list of `shot_xG` values is created for each group.
- The `shot_xG` values are then grouped by `matchweek`, `team_home`, and `team_away`, and a dictionary of `shot_xG` values is created for each group.
- The `shot_xG` values for the home and away teams are extracted from the `shot_xG` dictionary for each row in the `results_data` dataframe using the `get_home_xg` and `get_away_xg` functions.
- The total xG values for the home and away teams are calculated by summing the `shot_xG` values for each team.
- The `shot_xG` dictionary column is dropped from the `results_data` dataframe.
- Each row (match) in the `results_data` dataframe is simulated using the `simulate_match` function, and the expected points for the home and away teams are extracted and added to the dataframe.
- The results dataframe is filtered to only include matches where the home team is Arsenal.
- The column names in the filtered `results_data` dataframe are renamed to make it more readable.
- Actual results are merged onto the results dataframe.
- Variance and cumulative variance columns are calculated to track actual vs expected performance of Arsenal by `matchweek`.

### Output

The output of this code is a tab separate CSV file that contains a summary of Arsenal's season so far and the expected results and points total versus what actually happened. The file consists of 22 columns. Below is a brief description of each column in the dataframe:

- `Index`: Index column of DataFrame
- `matchweek`: Premier League Matchweek as per FBREF
- `opponent`: Team faced on that matchweek
- `xG`: Total expected Goals Arsenal achieved in the match
- `xGA`: Total expected Goals Arsenal conceded in the match
- `xPoints`: Expected points Arsenal should have achieved based on simulations
- `G`: Actual goals scored by Arsenal
- `GA`: Actual goals scored against Arsenal
- `points`: Actual points won by Arsenal
- `date`: Date the match took place
- `points_var`: `points` - `xPoints`
- `G_var`: `G` - `xG`
- `GA_var`: `GA` - `xGA`
- `cum_xPoints`: Cumulative sum of `xPoints` by `date`
- `cum_points`:  Cumulative sum of `points` by `date`
- `cum_points_var`:  Cumulative sum of `points_var` by `date`
- `cum_xG`:  Cumulative sum of `xG` by `date`
- `cum_G`:  Cumulative sum of `G` by `date`
- `cum_G_var`:  Cumulative sum of `G_var` by `date`
- `cum_xGA`:  Cumulative sum of `xGA` by `date`
- `cum_GA`:  Cumulative sum of `GA` by `date`
- `cum_GA_var`:  Cumulative sum of `GA_var` by `date`

Users can interpret the results by reviewing the expected values versus actual values. The variance columns help you to judge whether you feel Arsenal have been over- or underperforming. Ideally this code will be improved to factor in more matches between other teams to compare Arsena's actual position in the table to an "expected points position".

## Data

### Input Data

Sample data is included in the [data](https://github.com/jamesballen/expected-points/tree/main/data) folder of this repository. The following files are included:

- `xg_shot_data.csv`: a CSV file containing shot data, with columns for matchweek, team_home, team_away, team_shot (which team attempted the shot) and expected_goals (the xG value of each shot). 
    - team_home, team_away and team_shot columns must contain string values. 
    - expected_goals column must contain float values. 
    - matchweek column must contain integer values.
- `arsenal_results_data.csv`: a CSV file containing results data for Arsenal, with columns for matchweek, opponent, G (goals), GA (goals against), Points and date.
    - The matchweek, G, GA, and points columns must contain integer values.
    - The opponent column must contain string values.
    - The date column must contain date values.

Please download the sample data and place it in the same folder as the project code to run the code.

### Data Source

The data used in this project was sourced from [FBref](https://fbref.com/en/), a website that provides comprehensive football (soccer) statistics. Specifically, the data used in this project was obtained from FBref's Arsenal team statistics page, which contains detailed information on the performance of Arsenal Football Club in various competitions.

FBref collects its data from multiple sources, including official match reports, club websites, and public databases. The data is then processed and cleaned to ensure accuracy and consistency.

### Data Usage

The data used in this project is made publicly available by FBref under the terms of the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) License](https://creativecommons.org/licenses/by-nc-sa/4.0/).

Users of this data are free to use, distribute, and adapt the data for non-commercial purposes, provided they give proper attribution to FBref and share their modifications under the same license. It is the responsibility of the user to ensure they are complying with the terms of the license.

Note that while FBref strives to provide accurate and reliable data, errors and omissions may occur. Users of this data should exercise caution and verify the data before making decisions based on it.