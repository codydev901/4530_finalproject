import streamlit as st
import pandas as pd
import plotly.express as px


st.markdown("# NFL Player State Year Compare")


@st.cache_data
def load_df():
    return pd.read_csv("plot_data/nfl_player_state_year_compare.csv")


@st.cache_data
def load_super_bowl_df():
    return pd.read_csv("plot_data/super_bowl_mvp_states.csv")


plot_df = load_df()
sb_df = load_super_bowl_df()

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

# Single Value Display
total_nfl_players = sub_df["nfl_players_absolute"].sum()
total_us_population_reference = sub_df["state_pop_ref_value"].sum()
us_population_reference_year = sub_df["state_pop_ref_year"].iloc[0]

try:
    super_bowl_mvp = sb_df[sb_df["nfl_year"] == nfl_year_selection].iloc[0]
    super_bowl_mvp_name = super_bowl_mvp["super_bowl_mvp"]
    super_bowl_mvp_birth_state = super_bowl_mvp["birth_state"]
    super_bowl_mvp_high_school_state = super_bowl_mvp["high_school_state"]
except IndexError:
    super_bowl_mvp_name = "NA"
    super_bowl_mvp_birth_state = "NA"
    super_bowl_mvp_high_school_state = "NA"


fig = px.choropleth(sub_df, locations="state_value",
                    color="nfl_state_ratio_diff",
                    locationmode="USA-states",
                    scope="usa",
                    color_continuous_scale=px.colors.sequential.RdBu,
                    hover_data=["nfl_players_absolute", "state_pop_ref_value"],
                    title="NFL Relative Representation")
st.plotly_chart(fig, use_container_width=True)

st.header("Additional Information")
st.markdown(f"**NFL Players**: {total_nfl_players} in Season: {nfl_year_selection}")
st.markdown(f"**US Population**: {total_us_population_reference} in Year: {us_population_reference_year}")
st.markdown(f"**SuperBowl MVP**: {super_bowl_mvp_name}")
st.markdown(f"**MVP Birth State**: {super_bowl_mvp_birth_state}")
st.markdown(f"**MVP HighSchool State**: {super_bowl_mvp_high_school_state}")

st.header("Interaction Notes")
st.markdown("Use Slider To Select an NFL Season")
st.markdown("Choose to see where NFL players that season were born or went to highschool")
st.markdown("Choropleth shows which ares are over (positive/blue) or under (negative/red) represented in NFL in comparison "
            "to overall US population in relation to highschool year (8 years from season) or birth year (26 years from "
            "season")
