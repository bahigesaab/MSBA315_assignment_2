import numpy as np
import pandas as pd
import matplotlib as plt
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st

st.title("MSBA-325 Assignment 2")

## Part 1: Displaying the Dataframe of Netflix Subscribers Per Country in a Table:

st.header("Displaying Netflix Subscribers Per Country: ")

netflix_subscribers_df = pd.read_csv('netflix_subscribers_per_country.csv')
st.dataframe(netflix_subscribers_df)

st.header("Showing the Dataframe in a table: ")

netflix_subscribers_df_compressed = netflix_subscribers_df[
    ["Country", "Region", "latitude", "longitude", "# of Subscribers Q4 2021 (Estimate)",
     "Q4 2021 Revenue $ (Estimate)"]]
new_columns = {"# of Subscribers Q4 2021 (Estimate)": "Subscribers by 2021",
               "Q4 2021 Revenue $ (Estimate)": "Revenues by 2021"}
netflix_subscribers_df_compressed.rename(columns=new_columns, inplace=True)
netflix_subscribers_table = ff.create_table(netflix_subscribers_df_compressed)

st.write(netflix_subscribers_table)

## Part 2: Plotting Inline Bar Charts

### Part 2a: Plotting Bar Chart According to Countries
st.header("Plotting Inline: ")

st.subheader("Plotting Chart according to Countries: ")

netflix_subscribers_df.drop(netflix_subscribers_df[netflix_subscribers_df["Country"] == "United States"].index,
                            inplace=True)

data = [go.Bar(x=netflix_subscribers_df["Country"], y=netflix_subscribers_df["# of Subscribers Q4 2021 (Estimate)"])]

layout = go.Layout(title="Number of Netflix Subscribers per Country by end of 2021",
                   xaxis=dict(title="Country"),
                   yaxis=dict(title="Number of Subscribers"),
                   width=800)

fig_country = go.Figure(data=data, layout=layout)

st.plotly_chart(fig_country)


### Part 2b: Plotting Bar Chart According to Regions

st.subheader("Plotting Chart according to Regions: ")

netflix_subscribers_per_region = netflix_subscribers_df.groupby("Region", as_index=False)[
    ["Q1 2021 Revenue $", "Q2 2021 Revenue $", "Q3 2021 Revenue $ (Estimate)", "Q4 2021 Revenue $ (Estimate)"]].sum()

data = [go.Bar(x=netflix_subscribers_per_region["Region"],
               y=netflix_subscribers_per_region["Q1 2021 Revenue $"],
               name="First Quarter",
               marker=dict(color="rgb(0, 0, 255)")),
        go.Bar(x=netflix_subscribers_per_region["Region"],
               y=netflix_subscribers_per_region["Q2 2021 Revenue $"],
               name="Second Quarter",
               marker=dict(color="rgb(255, 0, 0)")),
        go.Bar(x=netflix_subscribers_per_region["Region"],
               y=netflix_subscribers_per_region["Q3 2021 Revenue $ (Estimate)"],
               name="Third Quarter",
               marker=dict(color="rgb(0, 255, 0)")),
        go.Bar(x=netflix_subscribers_per_region["Region"],
               y=netflix_subscribers_per_region["Q4 2021 Revenue $ (Estimate)"],
               name="Fourth Quarter",
               marker=dict(color="rgb(204, 0, 204)"))]

layout = go.Layout(title="Netflix Revenues per Quarter of 2021 in Different Regions of the World",
                   xaxis=dict(title="Region"),
                   yaxis=dict(title="Revenues in Millions of USD"))

fig_region = go.Figure(data=data, layout=layout)

st.plotly_chart(fig_region)

## Part 3 : Interactive Maps

st.header("Plotting a Map of Netflix Subscribers Per Country:")

mapbox_access_token = 'pk.eyJ1IjoiYmFoaWdlc2FhYiIsImEiOiJja3l5djA4czMwdzhoMnFxbDdqZXVhc2xjIn0.lqEdOX_HSMS4u-qNA6NXEQ'

px.set_mapbox_access_token(mapbox_access_token)

country_lat = netflix_subscribers_df.latitude
country_lon = netflix_subscribers_df.longitude
country_name = netflix_subscribers_df.Country

fig_map = px.scatter_mapbox(netflix_subscribers_df,
                        lat=country_lat,
                        lon=country_lon,
                        color="Region",
                        size="# of Subscribers Q4 2021 (Estimate)",
                        zoom=1,
                        )

fig_map.update_layout(title="Number of Netflix Subscribers Per Country in 2021", height=800, width=1100,
                  legend=dict(orientation="h"))

st.plotly_chart(fig_map)

## Part 4: 3D Plots:

st.subheader("Plotting 3D Chart:")

fig_3D = go.Figure(data=[go.Surface(z=netflix_subscribers_df.values)])
fig_3D.update_layout(title='Netflix Subscribers 3D Plot')

st.plotly_chart(fig_3D)

## Animations Section
st.header("Animations: ")

st.subheader("Displaying Dataframe of Growth of Netflix Subscribers in Each Region Per Year Quarter: ")

new_subscribers_per_region_df = pd.read_csv("new_subscribers_per_region.csv")
new_subscribers_per_region_table = ff.create_table(new_subscribers_per_region_df)

st.write(new_subscribers_per_region_table)

## Animated Bar Chart
st.subheader("Bar Chart of Growth of Netflix Subscribers in Each Region Per Year Quarter: ")

animated_bar_fig = px.bar(new_subscribers_per_region_df, x="Region", y="New Subscribers (Millions)",
          color="Region",  animation_frame="Quarter and Year", animation_group="Region", range_y=[0,15])

animated_bar_fig.update_layout( title = "Netflix Subscribers Growth per Quarter Period and Region",
                                width = 800,
                   legend= dict( orientation = "v",
                                   yanchor="bottom",
                                    y=1.02,
                                    xanchor="right",
                                    x=1),)

st.plotly_chart(animated_bar_fig)

# Animated Scatter Plot

st.subheader("Scatter Plot of Number of Netflix New Subscribers vs Revenues (USD) per Year Quarter: ")

fig_scatter = px.scatter(new_subscribers_per_region_df, x="New Subscribers (Millions)", y="Revenues (USD)",
                        color="Region", size="New Subscribers (Millions)", animation_frame="Quarter and Year",
                        animation_group="Region", hover_name="Region", range_x=[5,20], range_y=[0,3500000000])

fig_scatter.update_layout(legend=dict(
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                            ),
                          title="Number of Netflix New Subscribers vs Revenues (USD) per Year Quarter",
                          height=700,
                          width=850
                         )

st.plotly_chart(fig_scatter)