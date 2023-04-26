import pandas as pd

"""
Cody Whitt
pkz325
CPSC 4530 Spring 2023
Course Project

Parse code for state population data from US Census (appointment.csv)

Since Census data is on a 10 year scale, this performs a linear interpolation to provide
data on a yearly scale, as well as putting things in a more friendly format for the needs of this
project.

Writes to parsed_data/state_population.csv
"""


def parse_data():

    # Load, Check Null, Find Relevant Attribute Keys
    raw_df = pd.read_csv("raw_data/apportionment.csv")
    print(raw_df.head())
    print(raw_df.info())

    # Drop non-relevant attributes
    keep_columns = ["Name", "Year", "Resident Population"]
    raw_df = raw_df[keep_columns]
    print(raw_df.head())
    print(raw_df.info())

    # Check Unique Names (States)
    print(raw_df["Name"].unique())
    print(len(raw_df["Name"].unique()))

    # Remove non-states (Also District of Columbia and Puerto Rico also being removed since not technically states)
    remove_names = ['Midwest Region', 'Northeast Region', 'South Region', 'West Region', 'United States',
                    'District of Columbia', 'Puerto Rico']
    raw_df = raw_df[~raw_df["Name"].isin(remove_names)]
    print(raw_df["Name"].unique())
    print(len(raw_df["Name"].unique()))

    # Check Unique Years, pull out some attribute values for iteration below
    print(raw_df["Year"].unique())
    year_list = list(raw_df["Year"].unique())
    state_list = list(raw_df["Name"].unique())

    # For final parse step
    parsed_df = [["state", "year", "population"]]

    # For each state and each pair of census years, perform a linear interpolation by weighted average to
    # calculate population for each state on yearly interval
    for state in state_list:
        state_df = raw_df[raw_df["Name"] == state]
        for i, base_year in enumerate(year_list):
            if i == len(year_list) - 1:
                break
            next_year = year_list[i+1]
            base_pop = int(state_df[state_df["Year"] == base_year].iloc[0]["Resident Population"].replace(",", ""))
            next_pop = int(state_df[state_df["Year"] == next_year].iloc[0]["Resident Population"].replace(",", ""))
            for next_weight, range_year in enumerate(range(base_year, next_year)):
                next_weight = float(next_weight / 10.0)
                base_weight = 1.0 - next_weight
                weighted_base_pop = base_weight * base_pop
                weighted_next_pop = next_weight * next_pop
                weighted_pop = int(weighted_base_pop + weighted_next_pop)
                parsed_df.append([state, range_year, weighted_pop])

    # Check and write
    parsed_df = pd.DataFrame(data=parsed_df[1:], columns=parsed_df[0])
    print(parsed_df.head(112))

    parsed_df.to_csv("parsed_data/state_population.csv", index=False)


def main():

    parse_data()


if __name__ == "__main__":

    main()

