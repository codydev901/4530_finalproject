import pandas as pd

"""
Cody Whitt
pkz325
CPSC 4530 Spring 2023
Course Project

Parse code for Super Bowl data (superbowl.csv)

No major transformations, just cleans up a little and pulls year from date.

Writes to parsed_data/superbowl_info.csv
"""


def parse_data():

    # Load, Check Null, Find Relevant Attribute Keys
    raw_df = pd.read_csv("raw_data/superbowl.csv")
    print(raw_df.head())
    print(raw_df.info())

    # So we want Year, Winning and Losing Teams, and MVP
    raw_df = raw_df[["Date", "Winner", "Loser", "MVP"]]
    print(raw_df.head())
    print(raw_df.info())

    # Calculate Year from Date
    raw_df["Date"] = raw_df["Date"].apply(lambda x: x.split(" ")[-1])
    raw_df.rename(columns={"Date": "year"}, inplace=True)
    print(raw_df.head(100))

    # Remove + Sign from MVP Names
    raw_df["MVP"] = raw_df["MVP"].apply(lambda x: x.replace("+", ""))
    print(raw_df.head())

    # Clean up column names
    raw_df.rename(columns={"Winner": "winning_team", "Loser": "losing_team", "MVP": "mvp"}, inplace=True)
    print(raw_df.head())

    # Write to Parsed
    raw_df.to_csv("parsed_data/superbowl_info.csv", index=False)


def main():

    parse_data()


if __name__ == "__main__":

    main()