import os
import csv

from utils import get_number_of_owners
from constants import gamecenter_directory, leagueID

# Script which iterates over all games, and finds the biggest blowouts, and narrowest victories.
largest_margin = 0
narrowest_margin = 1000

# Iterate through each year
for year in (2020, 2021, 2022, 2023):
    print(year)
    path = gamecenter_directory + str(year) + '/'
    num_owners = get_number_of_owners(leagueID, path)
    
    # Iterate through each week
    for filename in os.listdir(path):
        if filename.endswith(".csv"):
            filepath = os.path.join(path, filename)
            with open(filepath, 'r', newline='') as file:
                reader = csv.DictReader(file)
                
                # Iterate through each team in the week
                for row in reader:
                    # Skip weeks where the team had a bye
                    if row['Total'] == "-" or row['Opponent Total'] == "-":
                        continue
                    # Calculate the margin of victory
                    margin = float(row['Total']) - float(row['Opponent Total'])
                    if margin > largest_margin:
                        print("Week " + filename[:-4] + " " + row['Owner'] + " has a new blowout with a " + str(round(margin,2)) + " point win over " + row['Opponent'])
                        largest_margin = margin
                    if margin > 0 and margin < narrowest_margin:
                        print("Week " + filename[:-4] + " " + row['Owner'] + " has a new narrow victory with a " + str(round(margin,2)) + " point win over " + row['Opponent'])
                        narrowest_margin = margin


