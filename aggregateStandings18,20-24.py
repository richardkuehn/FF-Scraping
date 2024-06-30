import csv
import os
from utils import get_number_of_owners
from constants import leagueID, standings_directory
import pandas as pd
# Aggregates scraped standings data into a single CSV file
# Assumptions:
# Top half of the league makes the playoffs

# Initialize a dictionary to store aggregated data
aggregated_data = {}

# Iterate through each file in the directory
for filename in ('2018.csv','2020.csv','2021.csv','2022.csv','2023.csv'):      # os.listdir(standings_directory):
    if filename.endswith(".csv"):
        filepath = os.path.join(standings_directory, filename)
        with open(filepath, 'r', newline='') as file:
            reader = csv.DictReader(file)
            num_owners = get_number_of_owners(leagueID, filename[:-4])
            # Iterate through each row in the CSV file
            for row in reader:
                manager_name = row["ManagerName"]

                # Initialize the manager's data if it doesn't exist
                if manager_name not in aggregated_data:
                    cols = ["PointsFor","PointsAgainst","Moves","Trades","Wins","Losses","Ties","Championships","Playoffs","ToiletBowls","DraftPosition"]
                    aggregated_data[manager_name] = {col: 0 for col in cols}
                    aggregated_data[manager_name]["Seasons"] = 1
                else:
                    aggregated_data[manager_name]["Seasons"] += 1
                # Sum the values for each column except "ManagerName"
                for key, value in row.items():
                    if key in ["PointsFor", "PointsAgainst", "Moves", "Trades", "DraftPosition"]:
                        aggregated_data[manager_name][key] += float(value.replace(",", ""))
                    elif key == "Record":
                        wins, losses, ties = map(int, value.split("-"))
                        aggregated_data[manager_name]["Wins"] += wins
                        aggregated_data[manager_name]["Losses"] += losses
                        aggregated_data[manager_name]["Ties"] += ties
                    elif key == "PlayoffRank":
                        if int(value) == 1:
                            aggregated_data[manager_name]["Playoffs"] += 1
                            aggregated_data[manager_name]["Championships"] += 1
                        elif int(value) == num_owners:
                            aggregated_data[manager_name]["ToiletBowls"] += 1
                        elif int(value) <= 4:
                            aggregated_data[manager_name]["Playoffs"] += 1
                        elif int(value) in (5, 6) and filename == '2023.csv':
                            aggregated_data[manager_name]["Playoffs"] += 1
## THINK ABOUT HOW TO CHANGE THIS SECTION TO ACCOUNT FOR 6 TEAM PLAYOFFS

# Convert dict_keys to a list
column_names = list(aggregated_data.values())[0].keys()

# Round PointFor, PointAgainst to 2 decimals
# Average Draft Position
aggregated_data_df = pd.DataFrame(aggregated_data).T
aggregated_data_df[['PointsFor', 'PointsAgainst']] = aggregated_data_df[['PointsFor', 'PointsAgainst']].round(2)

columns_to_round = ['Moves', 'Trades', 'Wins', 'Losses', 'Ties', 'Championships', 'Playoffs', 'ToiletBowls', 'DraftPosition', 'Seasons']
aggregated_data_df[columns_to_round] = aggregated_data_df[columns_to_round].round(0).astype(int)

aggregated_data_df['AvgDraftPosition'] = (aggregated_data_df['DraftPosition'] / aggregated_data_df['Seasons']).round(1)

aggregated_data_df

# Export dataframe
aggregated_data_df.to_csv('./output/aggregate/inc_2018_agg_data.csv', index=True)



# Write the aggregated data to a new CSV file
# output_filepath = './output/aggregated_standings_exc_2018.csv'
# with open(output_filepath, 'w', newline='') as file:
#     writer = csv.DictWriter(file, fieldnames=["ManagerName"] + list(column_names))
#     # Write the aggregated data to the CSV file
#     writer.writeheader()
#     for manager_name, data in aggregated_data.items():
#         data["ManagerName"] = manager_name
#         writer.writerow(data)

# print(f"Aggregated data written to {output_filepath}")

# print(filename)