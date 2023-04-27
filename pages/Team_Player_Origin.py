import streamlit as st
import pandas as pd
import plotly.graph_objs as go


st.markdown("# NFL Birth -> HighSchool -> College Flow")


@st.cache_data
def load_df():
    player_df_ref = pd.read_csv("parsed_data/nfl_players.csv")
    player_df_ref.dropna(inplace=True)
    player_df_ref = player_df_ref[player_df_ref["draft_year"] >= 2010]
    return player_df_ref


def process_selection_df(draft_team, player_df):

    selection_df = player_df[player_df["draft_team"] == draft_team]

    birth_states = list(selection_df["birth_state"].unique())
    high_school_states = list(selection_df["high_school_state"].unique())
    colleges = list(selection_df["college"].unique())

    label_list = birth_states + high_school_states + colleges
    link_dict = {"source": [],
                 "target": [],
                 "value": []}

    for birth_state_i, birth_state in enumerate(birth_states):

        for high_school_state_i, high_school_state in enumerate(high_school_states):

            sub_df = selection_df[(selection_df["high_school_state"] == high_school_state) &
                                  (selection_df["birth_state"] == birth_state)]
            high_school_count = len(sub_df)

            link_dict["source"].append(birth_state_i)
            link_dict["target"].append(len(birth_states) + high_school_state_i)
            link_dict["value"].append(high_school_count)

            for college_i, college in enumerate(colleges):
                sub_df = selection_df[(selection_df["high_school_state"] == high_school_state) &
                                      (selection_df["birth_state"] == birth_state) &
                                      (selection_df["college"] == college)]
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

    fig.update_layout(title_text=f"{draft_team} Player Origin Since 2010 Draft", font_size=10)
    return fig


plot_df = load_df()

team_options = list(plot_df["draft_team"].unique())
team_selector = st.selectbox("Select Draft Team",
                             team_options)

dis_fig = process_selection_df(team_selector, plot_df)

st.plotly_chart(dis_fig, use_container_width=True)

st.header("Interaction Notes")
st.markdown("Choose An NFL Team")
st.markdown("From Left to Right, Shows Birth State -> High School -> College Flow for NFL Players drafted by that "
            "team between 2010 and 2017")
