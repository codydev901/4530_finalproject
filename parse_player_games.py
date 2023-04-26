import json
import pandas as pd

"""
Cody Whitt
pkz325
CPSC 4530 Spring 2023
Course Project

Parses NFL game data (games_1512362753.8735218.json) in order to determine the following:
For each player, for each year they played, which team did they play for in terms of the last game they played
that year?

Writes to parsed_data/nfl_players_team_year.csv
"""


def parse_data():

    # Load up JSON file, take a look at number of elements and an example entry.
    # In this case, its roughly JSONL equivalent in that items exist in an outer-level array
    with open("raw_data/games_1512362753.8735218.json", "r") as r_file:
        info_json = json.load(r_file)
    print(len(info_json))
    print(info_json[0])

    # So looks like we want player_id, year, date, game_number, team to start with
    parsed_df = [["player_id", "year", "date", "game_number", "team"]]
    for row in info_json:
        parsed_df.append([row[k] for k in parsed_df[0]])
    parsed_df = pd.DataFrame(data=parsed_df[1:], columns=parsed_df[0])
    print(parsed_df.head(20))
    print(parsed_df.info())

    # Convert game number to int
    parsed_df["game_number"] = parsed_df["game_number"].astype(int)

    # Let's see how SuperBowls look in terms of game_number and year, to make sure it doesn't roll over
    print(parsed_df[parsed_df["game_number"] == 17].head(40))
    print(list(parsed_df["game_number"].unique()))
    # ^ Looks good, a game played in January/February (playoff or super bowl) is properly associated with the Fall
    # season in terms of year. (Forgot about playoff games when saw unique game number went to 20 etc).

    # For final write, condense to which players ended the year on which teams
    final_df = [["player_id", "year", "team"]]

    # So to condense things down/account for trading, we want to know which team a player was playing for each year
    # on the last game that they played that year.
    for player_id in parsed_df["player_id"].unique():
        player_df = parsed_df[parsed_df['player_id'] == player_id]
        for player_year in player_df["year"].unique():
            player_year_df = player_df[player_df["year"] == player_year]
            player_max_game = player_year_df["game_number"].max()
            player_max_game_df = player_year_df[player_year_df["game_number"] == player_max_game]
            player_year_team = player_max_game_df.iloc[0]["team"]
            final_df.append([player_id, player_year, player_year_team])

    final_df = pd.DataFrame(data=final_df[1:], columns=final_df[0])
    print(final_df.head())
    print(final_df.info())

    # Write to parsed_data
    final_df.to_csv("parsed_data/nfl_players_team_year.csv", index=False)


def main():

    parse_data()


if __name__ == "__main__":

    main()