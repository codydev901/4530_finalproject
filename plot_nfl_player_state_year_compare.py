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
    pop_year_df = pd.read_csv("parsed_data/state_population.csv")

    # Quick Check on Birth State vs. High School
    same_birth_hs = 0
    for i, row in player_df.iterrows():
        if row["birth_state"] == row["high_school_state"]:
            same_birth_hs += 1

    # Interesting, expected slightly higher, ~80% shared. Will track both.
    print(same_birth_hs)
    print(len(player_df))

    # Quick Reference to State Abbreviation
    states_abrs = list(pop_year_df["state_abr"].unique())
    print(states_abrs)

    # First set up a map to associate player_id with its row in DF for easier querying
    player_id_lu = {row['player_id']: row for i, row in player_df.iterrows()}

    final_df = [["nfl_year",
                 "state_key",                         # birth or high_school
                 "state_value",                       # Each of the 50 State Abr
                 "nfl_players_absolute",              # Absolute Count of NFL Players tied to above key/value
                 "nfl_players_ratio",                 # Ratio of key/value to total count of all players that year
                 "state_pop_ratio",                   # State population either 8 or 26 years ago in relation to US pop
                 "nfl_state_ratio_diff",              # nfl_ratio - state_pop_ratio
                 "state_pop_ref_year",                # Year the state population value was pulled from
                 "state_pop_ref_value",               # State population value tied to ^ year
                 ]]

    # For each year when players played in the NFL
    for year in team_year_df['year'].unique():
        team_year_df_by_year = team_year_df[team_year_df["year"] == year]

        year_us_population_birth = pop_year_df[pop_year_df["year"] == (year - 26)]["population"].sum()
        year_us_population_highschool = pop_year_df[pop_year_df["year"] == (year - 8)]["population"].sum()

        birth_states = []
        high_school_states = []
        # For each player who played that year, put state info into above lists (will count these later on)
        for i, player_row in team_year_df_by_year.iterrows():
            try:
                player_info = player_id_lu[player_row["player_id"]]
            except KeyError:  # For scrubbed international players
                continue
            birth_states.append(player_info["birth_state_abr"])
            high_school_states.append(player_info["high_school_state_abr"])

        year_nfl_players_absolute = len(birth_states)

        for state_abr in states_abrs:

            birth_abs_count = birth_states.count(state_abr)
            high_school_abs_count = high_school_states.count(state_abr)

            state_year_population_birth = pop_year_df[(pop_year_df["year"] == (year - 26)) &
                                                      (pop_year_df["state_abr"] == state_abr)]["population"].sum()
            state_year_population_highschool = pop_year_df[(pop_year_df["year"] == (year - 8)) &
                                                           (pop_year_df["state_abr"] == state_abr)]["population"].sum()

            nfl_birth_ratio = birth_abs_count / year_nfl_players_absolute
            pop_birth_ratio = state_year_population_birth / year_us_population_birth

            nfl_high_school_ratio = high_school_abs_count / year_nfl_players_absolute
            pop_high_school_ratio = state_year_population_highschool / year_us_population_highschool

            final_df.append([year,
                             "birth",
                             state_abr,
                             birth_abs_count,
                             nfl_birth_ratio,
                             pop_birth_ratio,
                             nfl_birth_ratio - pop_birth_ratio,
                             year - 26,
                             state_year_population_birth
                             ])

            final_df.append([year,
                             "highschool",
                             state_abr,
                             high_school_abs_count,
                             nfl_high_school_ratio,
                             pop_high_school_ratio,
                             nfl_high_school_ratio - pop_high_school_ratio,
                             year - 8,
                             state_year_population_highschool,
                             ])

    final_df = pd.DataFrame(data=final_df[1:], columns=final_df[0])
    final_df.to_csv("plot_data/nfl_player_state_year_compare.csv", index=False)


def super_bowl_helper():

    player_df = pd.read_csv("parsed_data/nfl_players.csv")
    super_bowl_df = pd.read_csv("parsed_data/superbowl_info.csv")

    player_name_lu = {row['name']: row for i, row in player_df.iterrows()}

    res_df = [["nfl_year", "super_bowl_mvp", "high_school_state", "birth_state", "high_school_state_abr",
               "birth_state_abr"]]

    for i, row in super_bowl_df.iterrows():

        if row["year"] > 2017:
            continue

        try:
            player_info = player_name_lu[row['mvp']]
            b_s = player_info["birth_state"]
            b_s_a = player_info["birth_state_abr"]
            h_s = player_info["high_school_state"]
            h_s_a = player_info["high_school_state_abr"]
        except KeyError:
            # Edge Case (Earlier Scrubbed international birth player)
            if row["mvp"] == "Mark Rypien":
                b_s = "Canada"
                b_s_a = "CAN"
                h_s = "Washington"
                h_s_a = "WA"
            # Edge Case (Two MVPs in same year)
            if row["mvp"] == "Harvey MartinRandy White":
                b_s = "Texas/Pennsylvania"
                b_s_a = "TX/PA"
                h_s = "Texas/Delaware"
                h_s_a = "TX/DE"

        res_df.append([row['year'], row["mvp"], h_s, b_s, h_s_a, b_s_a])

    res_df = pd.DataFrame(data=res_df[1:], columns=res_df[0])
    res_df.to_csv("plot_data/super_bowl_mvp_states.csv", index=False)




def main():

    parse_data()

    super_bowl_helper()


if __name__ == "__main__":

    main()



