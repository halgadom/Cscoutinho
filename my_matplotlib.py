import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
from datetime import timedelta

# Connect to the SQLite database
conn = sqlite3.connect('/static/{db_name}.db')

# Execute a SQL query and load the data into a pandas DataFrame
df = pd.read_sql_query("SELECT timestamp, passes_home, passes_away, expected_goals_home, expected_goals_away, ball_possession_home, ball_possession_away, total_shots_home, total_shots_away, shots_on_target_home, shots_on_target_away, big_chances_home, big_chances_away FROM statistics", conn)

# Close the connection
conn.close()

# Convert the 'timestamp' column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d-%m-%Y-%H-%M-%S')

# Sort the DataFrame by the 'timestamp' column
df.sort_values('timestamp', inplace=True)

# List of statistical groups to plot
statistics = [
    ('passes_home', 'passes_away', 'Passes'),
    ('expected_goals_home', 'expected_goals_away', 'Expected Goals'),
    ('ball_possession_home', 'ball_possession_away', 'Ball Possession'),
    ('total_shots_home', 'total_shots_away', 'Total Shots'),
    ('shots_on_target_home', 'shots_on_target_away', 'Shots on Target'),
    ('big_chances_home', 'big_chances_away', 'Big Chances')
]

# Get the minimum and maximum timestamps from the dataframe
min_timestamp = df['timestamp'].min()
max_timestamp = df['timestamp'].max()

# Create a new array of timestamps that increments by 90 seconds
new_timestamps = pd.date_range(start=min_timestamp, end=max_timestamp, freq='90S')

# Convert the new_timestamps to strings and format them to include hours, minutes, and seconds
new_timestamps_str = [ts.strftime('%H:%M:%S') for ts in new_timestamps]

# Plot the graph
for home, away, title in statistics:
    plt.figure(figsize=(10, 6))
    plt.plot(df['timestamp'], df[home].astype(int), label=f'{title} Home')
    plt.plot(df['timestamp'], df[away].astype(int), label=f'{title} Away')
    plt.xlabel('Timestamp')
    plt.ylabel(title)
    plt.title(f'{title} Home vs Away Over Time')
    plt.legend()
    plt.xticks(new_timestamps, new_timestamps_str, rotation=45) # Set the x-ticks to the new timestamps
    plt.yticks(range(int(df[home].min()), int(df[home].max()) + 1))
    plt.savefig(f'/static/{title.replace(" ", "_").lower()}_{db_name}_home_vs_away_over_time.png')
    plt.show()
