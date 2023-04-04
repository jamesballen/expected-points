## README

This code reads in two CSV files, one containing shot data and the other containing results data for Arsenal. It then calculates expected points for Arsenal using a simulation approach, based on the shot data.

### Libraries Used
- `pandas`: used for data manipulation and analysis.
- `random`: used to simulate matches by generating random numbers.

### Functions
- `create_dict`: a function that takes a group of rows from the shot_data dataframe and returns a dictionary of shot_xG values grouped by team_shot.
- `get_home_xg`: a function that takes a row from the results_data dataframe and returns a list of shot_xG values for the home team.
- `get_away_xg`: a function that takes a row from the results_data dataframe and returns a list of shot_xG values for the away team.
- `sum_list`: a function that takes a list of numbers and returns the sum of those numbers.
- `simulate_match`: a function that takes a row from the results_data dataframe and simulates a match by generating random numbers and comparing them to the shot_xG values for each team. It returns the expected points for the home and away teams.

### Workflow
- The shot_data dataframe is grouped by matchweek, team_home, team_away, and team_shot, and a list of shot_xG values is created for each group.
- The shot_xG values are then grouped by matchweek, team_home, and team_away, and a dictionary of shot_xG values is created for each group.
- The shot_xG values for the home and away teams are extracted from the shot_xG dictionary for each row in the results_data dataframe using the get_home_xg and get_away_xg functions.
- The total xG values for the home and away teams are calculated by summing the shot_xG values for each team.
- The shot_xG dictionary column is dropped from the results_data dataframe.
- Each row (match) in the results_data dataframe is simulated using the simulate_match function, and the expected points for the home and away teams are extracted and added to the dataframe.
- The results dataframe is filtered to only include matches where the home team is Arsenal.
- The column names in the filtered results_data dataframe are renamed to make it more readable.
- Actual results are merged onto the results dataframe.
- Variance and cumulative variance columns are calculated to track actual vs expected performance of Arsenal by matchweek.

### Input Data
Sample data is included in the `data` folder of this repository. The following files are included:

- `xg_shot_data.csv`: a CSV file containing shot data, with columns for matchweek, team_home, team_away, team_shot (which team attempted the shot) and expected_goals (the xG value of each shot). team_home, team_away and team_shot columns must contain string values. expected_goals column must contain float values. matchweek column must contain integer values.
- `arsenal_results_data.csv`: a CSV file containing results data for Arsenal, with columns for matchweek, opponent, G (goals), GA (goals against), Points and date.

Please download the sample data and place it in the same folder as the project code to run the code.
