import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown("# Team State Compare")


def perform_comparison_calc(df, from_desc, team_1, team_2, year_tuple):

    sub_df = df[(df["nfl_year"].isin(list(range(year_tuple[0], year_tuple[1]+1)))) &
                (df["team"].isin([team_1, team_2])) &
                (df["from_desc"] == from_desc)]

    compare_df_ref = [["state", "team", "num_players", "state_total_players"]]

    for state in sub_df["state"].unique():
        team_1_state_players = sub_df[(sub_df["team"] == team_1) &
                                      (sub_df["state"] == state)]["players_from_state"].sum()
        team_2_state_players = sub_df[(sub_df["team"] == team_2) &
                                      (sub_df["state"] == state)]["players_from_state"].sum()
        compare_df_ref.append([state, team_1, team_1_state_players, team_1_state_players+team_2_state_players])
        compare_df_ref.append([state, team_2, team_2_state_players, team_1_state_players+team_2_state_players])

    compare_df_ref = pd.DataFrame(data=compare_df_ref[1:], columns=compare_df_ref[0])

    return compare_df_ref


@st.cache_data
def load_df():
    return pd.read_csv("plot_data/team_state_compare.csv")


plot_df = load_df()

state_key_options = list(plot_df["from_desc"].unique())
state_key_selector = st.selectbox("Compare By Player Birth State or High School State",
                                  state_key_options)

team_options = list(plot_df["team"].unique())
team_1_selector = st.selectbox("Select Team 1",
                               team_options)

team_2_selector = st.selectbox("Select Team 2",
                               team_options)

year_min = int(plot_df["nfl_year"].min())
year_max = int(plot_df["nfl_year"].max())

year_slider = st.slider("Select Year Range",
                        value=(year_min, year_max),
                        min_value=year_min,
                        max_value=year_max)

compare_df = perform_comparison_calc(plot_df, state_key_selector, team_1_selector, team_2_selector, year_slider)
compare_df.sort_values(by=["state_total_players"], inplace=True, ascending=False)

fig = px.bar(data_frame=compare_df, x="state", y="num_players", color="team", barmode="group")

st.plotly_chart(fig, use_container_width=True)

st.header("Interaction Notes")
st.markdown("Choose Birth State or High School State Reference")
st.markdown("Select Two Teams to Compare (Or the Same Team To Check One Team)")
st.markdown("Use Year Slider To Choose Date Range")
st.markdown("Grouped BarChart shows a comparison of the number of player-years contributed to the teams by each state "
            "in the selected date range in terms of absolute counts")
