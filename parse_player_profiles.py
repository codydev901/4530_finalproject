import json
import pandas as pd

"""
Cody Whitt
pkz325
CPSC 4530 Spring 2023
Course Project

Parses the NFL player dataset (profiles_1512362725.022629.json) from JSON to a .csv, where each player is associated
with a US State in terms of where they were born and went to high school. In addition, information regarding their
position, draft team/year, and college is kept for secondary analysis.

Writes to parsed_data/nfl_players.csv
"""


def state_helper(raw_entry, state_abbrev_map):
    """
    For use below in converting location of NFL Player birth_place and high_school to a US State in format used
    for this project.
    """

    state_list = [state_abbrev_map[k] for k in state_abbrev_map]

    if raw_entry in state_list:
        return raw_entry

    # Inefficient handling of an edge-case detected later on, but fine in terms of speed here.
    raw_entry_key = raw_entry.split(",")[-1].strip().upper()
    if raw_entry_key == 'CA;NY':
        raw_entry_key = "NY"

    try:
        return state_abbrev_map[raw_entry_key]
    except KeyError:
        # May or may not do something with the international country
        return f"International-{raw_entry.split(',', 1)[-1].strip()}"


def parse_data():

    # Load up JSON file, take a look at number of elements and an example entry.
    # In this case, its roughly JSONL equivalent in that items exist in an outer-level array
    with open("raw_data/profiles_1512362725.022629.json", "r") as r_file:
        info_json = json.load(r_file)
    print(len(info_json))
    print(info_json[0])
    print(len(info_json[0]))

    # So looks like we will be interested in the following:
    # player_id, name, position, birth_place, college, high_school, draft_team, draft_round, draft_year
    # Pull ^ out and put in a DataFrame to see how it looks

    parsed_df = [["player_id", "name", "position", "birth_place", "college", "high_school", "draft_team",
                  "draft_round", "draft_year", "birth_date"]]
    for row in info_json:
        parsed_df.append([row[k] for k in parsed_df[0]])

    parsed_df = pd.DataFrame(data=parsed_df[1:], columns=parsed_df[0])
    print(parsed_df.head())
    print(parsed_df.info())

    # Handle an Edge Cases
    parsed_df['name'] = parsed_df['name'].apply(lambda x: x.strip())

    # Mostly complete, will drop nulls involving birth_place, college, high_school since fewer there, but leave nulls
    # for draft_team, draft_round, draft_year since those attributes may or may not be used in more secondary analysis
    # or might be able to be filled in through the game data set.
    parsed_df = parsed_df[parsed_df['birth_place'].notna()]
    parsed_df = parsed_df[parsed_df['college'].notna()]
    parsed_df = parsed_df[parsed_df['high_school'].notna()]
    parsed_df = parsed_df[parsed_df['birth_date'].notna()]
    print(parsed_df.head())
    print(parsed_df.info())

    # Convert birth_date to birth_year
    parsed_df["birth_date"] = parsed_df["birth_date"].apply(lambda x: x.split("-", 1)[0].strip())
    parsed_df.rename(columns={"birth_date": "birth_year"}, inplace=True)

    # So now lets convert birth_place and high_school to "US State" in same format as the Census Data
    # Use another dataset to build a map
    state_abbrev_df = pd.read_csv("raw_data/states.csv")
    print(state_abbrev_df.head())
    state_abbrev_map = dict()
    state_abbrev_map_state_to_abr = dict()
    track_states = []
    for i, row in state_abbrev_df.iterrows():
        state_abbrev_map[row["Abbreviation"]] = row["State"]
        state_abbrev_map_state_to_abr[row["State"]] = row["Abbreviation"]
        track_states.append(row["State"])
    print(state_abbrev_map)

    # Use helper function to transform
    parsed_df["birth_place"] = parsed_df["birth_place"].apply(lambda x: state_helper(x, state_abbrev_map))
    parsed_df["high_school"] = parsed_df["high_school"].apply(lambda x: state_helper(x, state_abbrev_map))
    print(parsed_df.head())

    # Rename columns
    print("OK")
    parsed_df.rename(columns={"birth_place": "birth_state", "high_school": "high_school_state"}, inplace=True)
    print(parsed_df.head())
    print(parsed_df.info())

    # Check unique birth_state and high_school_state
    print(len(parsed_df["birth_state"].unique()))
    print(parsed_df["birth_state"].unique())
    # Caught an edge case w/ high_school_state (not there now)
    print(len(parsed_df["high_school_state"].unique()))
    print(parsed_df["high_school_state"].unique())

    # Remove International Players
    print("Remove International")
    print(len(parsed_df))
    parsed_df = parsed_df[(parsed_df["birth_state"].isin(track_states)) &
                          (parsed_df["high_school_state"].isin(track_states))]
    print(len(parsed_df))

    parsed_df["birth_state_abr"] = parsed_df["birth_state"].apply(lambda x: state_abbrev_map_state_to_abr[x])
    parsed_df["high_school_state_abr"] = parsed_df["high_school_state"].apply(lambda x: state_abbrev_map_state_to_abr[x])

    # Write to parsed_data
    parsed_df.to_csv("parsed_data/nfl_players.csv", index=False)


def main():

    parse_data()


if __name__ == "__main__":

    main()
