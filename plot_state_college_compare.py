import pandas as pd
import plotly.graph_objects as go

"""
Cody Whitt
pkz325
CPSC 4530 Spring 2023
Course Project

Flow
birth_state -> high_school -> college

filter by = draft_team

https://plotly.com/python/sankey-diagram/

Testing for the Sankey Diagram implementation.
"""


def parse_data():

    player_df = pd.read_csv("parsed_data/nfl_players.csv")
    player_df.dropna(inplace=True)

    draft_team = "Seattle Seahawks"
    player_df = player_df[(player_df["draft_team"] == draft_team) &
                          (player_df["draft_year"] >= 2010)]

    birth_states = list(player_df["birth_state"].unique())
    high_school_states = list(player_df["high_school_state"].unique())
    colleges = list(player_df["college"].unique())

    label_list = birth_states + high_school_states + colleges
    link_dict = {"source": [],
                 "target": [],
                 "value": []}

    for birth_state_i, birth_state in enumerate(birth_states):

        for high_school_state_i, high_school_state in enumerate(high_school_states):

            sub_df = player_df[(player_df["high_school_state"] == high_school_state) &
                               (player_df["birth_state"] == birth_state)]
            high_school_count = len(sub_df)

            link_dict["source"].append(birth_state_i)
            link_dict["target"].append(len(birth_states) + high_school_state_i)
            link_dict["value"].append(high_school_count)

            for college_i, college in enumerate(colleges):
                sub_df = player_df[(player_df["high_school_state"] == high_school_state) &
                                   (player_df["birth_state"] == birth_state) &
                                   (player_df["college"] == college)]
                college_count = len(sub_df)

                link_dict["source"].append(len(birth_states) + high_school_state_i)
                link_dict["target"].append(len(birth_states) + len(high_school_states) + college_i)
                link_dict["value"].append(college_count)

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=label_list,
            color="blue"
        ),
        link=link_dict)])

    fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
    fig.show()


def main():

    parse_data()


if __name__ == "__main__":

    main()
