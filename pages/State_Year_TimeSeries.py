import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown("# State Year TimeSeries")


@st.cache_data
def load_df():
    return pd.read_csv("plot_data/nfl_player_state_year_compare.csv")


plot_df = load_df()

state_key_options = list(plot_df["state_key"].unique())
state_key_selector = st.selectbox("Compare By Player Birth State or High School State",
                                  state_key_options)


sub_df = plot_df[plot_df["state_key"] == state_key_selector].copy()
sub_df.sort_values(by=["nfl_year"], inplace=True)

fig = px.line(data_frame=sub_df, x="nfl_year", y="nfl_players_ratio", color="state_value",
              hover_data=["nfl_players_absolute"], title="NFL Player Representation Over Time")

st.plotly_chart(fig, use_container_width=True)

st.header("Interaction Notes")
st.markdown("Choose to see where NFL players that season were born or went to highschool")
st.markdown("Click on the state abbreviations on the right to hide/show the individual states")
st.markdown("Timeseries line plot shows the relative percent of NFL players who were either born or "
            "attended high school in each state in the corresponding season.")
