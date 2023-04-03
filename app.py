import random
import pandas as pd

# Read in the CSV file containing the shot data
df = pd.read_csv('~/Downloads/xg_shot_data.csv')

# Read in CSV file containing shot data
df2 = pd.read_csv('~/Downloads/arsenal_results_data.csv')

# Define a function to create a dictionary of shot_xG values grouped by team_shot
def create_dict(group):
    return {row['team_shot']: row['shot_xG'] for _, row in group.iterrows()}

# Define a function to get the shot_xG values for the home team
def get_home_xg(row):
    home = row['team_home']
    shot_xG_dict = row['shot_xG']
    if home in shot_xG_dict:
        return shot_xG_dict[home][:]
    else:
        return None

# Define a function to get the shot_xG values for the away team
def get_away_xg(row):
    away = row['team_away']
    shot_xG_dict = row['shot_xG']
    if away in shot_xG_dict:
        return shot_xG_dict[away][:]
    else:
        return None

# Define a function to calculate the sum of a list of values
def sum_list(lst):
    return sum(lst)

# Define a function to simulate matches
def simulate_match(row, n=10000):
    if not isinstance(n, int):
        raise ValueError("n must be an integer.")

    # Extract the xG and xGA values for the home and away teams from the row.
    xG = row['shot_xG_home']
    xGA = row['shot_xG_away']

    # Initialize variables to keep track of the number of wins, losses, and draws.
    win = 0
    loss = 0
    draw = 0

    # Seed the random number generator to ensure reproducibility.
    random.seed(1048)

    # Run n simulations of the match.
    for i in range(n):
        goals_for = 0
        goals_against = 0

        # Simulate the home team's goals.
        for j in range(len(xG)):
            x = random.random()
            if x < xG[j]:
                goals_for += 1

        # Simulate the away team's goals.
        for k in range(len(xGA)):
            y = random.random()
            if y < xGA[k]:
                goals_against += 1

        # Update the win, loss, and draw counters.
        if goals_for > goals_against:
            win += 1
        elif goals_for < goals_against:
            loss += 1
        else:
            draw += 1

    # Calculate the expected points for the home and away teams based on the simulations.
    xPointsHome = ((win * 3) + draw) / n
    xPointsAway = ((loss * 3) + draw) / n

    # Return the expected points for the home and away teams.
    return xPointsHome, xPointsAway

# Group the data by matchweek, home team, away team, and team_shot, and create a list of expected_goals values for each group
df = df.groupby(['matchweek', 'team_home', 'team_away', 'team_shot'])[
    'expected_goals'].apply(list).reset_index(name='shot_xG')

# Group the data by matchweek, home team, and away team, and create a dictionary of shot_xG values for each group
df = df.groupby(['matchweek', 'team_home', 'team_away']).apply(
    create_dict).reset_index(name='shot_xG')

# Add columns to the dataframe for the home team's shot_xG values and away team's shot_xG values
df['shot_xG_home'] = df.apply(get_home_xg, axis=1)
df['shot_xG_away'] = df.apply(get_away_xg, axis=1)

# Add columns to the dataframe for the home team's total xG and away team's total xG
df['xG_home'] = df['shot_xG_home'].apply(sum_list)
df['xG_away'] = df['shot_xG_away'].apply(sum_list)

# Drop the dict column: shot_xG
df.drop('shot_xG', axis=1, inplace=True)

# Iterate over each row (match) in the dataframe.
for index, row in df.iterrows():
    # Simulate the match using the 'simulate_match' function and extract the expected points for the home and away teams.
    xPointsHome, xPointsAway = simulate_match(row)

    # Update the 'xPointsHome' and 'xPointsAway' columns in the dataframe with the expected points.
    df.at[index, 'xPointsHome'] = xPointsHome
    df.at[index, 'xPointsAway'] = xPointsAway

# Select columns from the DataFrame where the 'team_home' column is 'Arsenal'
home = df[['matchweek', 'team_away', 'xG_home', 'xG_away',
           'xPointsHome']][df['team_home'] == 'Arsenal']

# Rename the selected columns to match the format used in the StatsBomb data
home = home.rename(columns={
    'team_away': 'opponent',  # Change 'team_away' to 'opponent'
    'xG_home': 'xG',         # Change 'xG_home' to 'xG'
    'xG_away': 'xGA',        # Change 'xG_away' to 'xGA'
    'xPointsHome': 'xPoints'  # Change 'xPointsHome' to 'xPoints'
})

# Select the rows where Arsenal played away
away = df[['matchweek', 'team_home', 'xG_home', 'xG_away',
           'xPointsAway']][df['team_away'] == 'Arsenal']

# Rename the columns to match the format of the home team dataframe
away = away.rename(columns={
    'team_home': 'opponent',  # Change 'team_away' to 'opponent'
    'xG_away': 'xG',         # Change 'xG_away' to 'xG'
    'xG_home': 'xGA',        # Change 'xG_home' to 'xGA'
    'xPointsAway': 'xPoints'  # Change 'xPointsAway' to 'xPoints'
})

# Concatenate home and away dataframes for Arsenal, sort by matchweek, and reset index
results = pd.concat([home, away], ignore_index=True).sort_values(
    'matchweek').reset_index(drop=True)

# Merge expected results with actual results on matchweek and opponent columns, keeping only matching rows
results = pd.merge(results, df2, on=['matchweek', 'opponent'], how='left')

# Sort fixtures by date, reset index, and convert date column to datetime format
results = results.sort_values('date').reset_index(drop=True)
results['date'] = pd.to_datetime(results['date'])

# Create new columns for various cumulative and difference variables based on expected and actual results
results['Points_var'] = results['Points'] - results['xPoints']
results['G_var'] = results['G'] - results['xG']
results['GA_var'] = results['GA'] - results['xGA']

results['cum_xPoints'] = results['xPoints'].cumsum()
results['cum_Points'] = results['Points'].cumsum()
results['cum_Points_var'] = results['Points_var'].cumsum()

results['cum_xG'] = results['xG'].cumsum()
results['cum_G'] = results['G'].cumsum()
results['cum_G_var'] = results['G_var'].cumsum()

results['cum_xGA'] = results['xGA'].cumsum()
results['cum_GA'] = results['GA'].cumsum()
results['cum_GA_var'] = results['GA_var'].cumsum()

print(results)

results.to_csv('~/Downloads/expected-points.csv', sep='\t')

print('10,000 matches simulated. "expected-points.csv" placed in "Downloads" folder')
