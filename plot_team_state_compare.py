import pandas as pd

"""
Cody Whitt
pkz325
CPSC 4530 Spring 2023
Course Project

Doc Doc Doc
"""


def parse_data():

    player_df = pd.read_csv("parsed_data/nfl_players.csv")
    team_year_df = pd.read_csv("parsed_data/nfl_players_team_year.csv")

    player_id_lu = {row['player_id']: row for i, row in player_df.iterrows()}

    final_df = [["team", "state", "nfl_year", "players_from_state", "from_desc"]]

    for team in team_year_df["team"].unique():
        for year in team_year_df["year"].unique():

            if year < 1967:
                continue

            sub_team_year_df = team_year_df[(team_year_df["team"] == team) &
                                            (team_year_df["year"] == year)]
            birth_states = {}
            high_school_states = {}
            for i, player in sub_team_year_df.iterrows():
                try:
                    player_info = player_id_lu[player['player_id']]
                except KeyError:  # For scrubbed international players
                    continue
                try:
                    birth_states[player_info["birth_state"]] += 1
                    high_school_states[player_info["high_school_state"]] += 1
                except KeyError:
                    birth_states[player_info["birth_state"]] = 1
                    high_school_states[player_info["high_school_state"]] = 1

            for b_s in birth_states:
                final_df.append([team, b_s, year, birth_states[b_s], "birth"])

            for h_s in high_school_states:
                final_df.append([team, h_s, year, high_school_states[h_s], "high_school"])

    final_df = pd.DataFrame(data=final_df[1:], columns=final_df[0])
    final_df.to_csv("plot_data/team_state_compare.csv", index=False)


def main():

    parse_data()


if __name__ == "__main__":

    main()
