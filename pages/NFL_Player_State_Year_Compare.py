import streamlit as st
import pandas as pd
import plotly.express as px


st.markdown("# NFL Player State Year Compare")


@st.cache_data
def load_df():
    return pd.read_csv("plot_data/nfl_player_state_year_compare.csv")


plot_df = load_df()

slider_years = list(plot_df["nfl_year"].unique())
year_min = int(min(slider_years))
year_max = int(max(slider_years))
nfl_year_selection = st.select_slider("NFL Season",
                                      options=list(range(year_min, year_max+1)),
                                      value=year_min)

state_key_options = list(plot_df["state_key"].unique())
state_key_selector = st.selectbox("Compare By Player Birth State or High School State",
                                  state_key_options)


sub_df = plot_df[(plot_df["nfl_year"] == nfl_year_selection) & (plot_df["state_key"] == state_key_selector)]

fig = px.choropleth(sub_df, locations="state_value",
                    color="nfl_state_ratio_diff",
                    locationmode="USA-states",
                    scope="usa",
                    color_continuous_scale=px.colors.sequential.RdBu)
st.plotly_chart(fig, use_container_width=True)

