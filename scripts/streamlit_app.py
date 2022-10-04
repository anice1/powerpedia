#!/usr/bin/python3
from turtle import color
import numpy as np
import streamlit as st

# setup page configuration
st.set_page_config(
    layout="wide",
    page_icon="https://data2bots.com/wp-content/uploads/2018/11/image_1_8-2.png",
)


def intro():

    st.write("# D2b Data Pipeline ♽")

    st.markdown(
        """
        ### Overview
        D2b is a simple data pipeline designed to help automate the processes involved in extracting, transforming, analysing and exporting data insights carried out by data professionals at Data2bot. The automation pipeline is designed to abstract complexities and allow analysts to focus solely on SQL.

        ### **Installation and setup** 🔩🪛
        Clone the repository.
        ```bash 
        git clone https://github.com/anochima/data2bot.git
        cd data2bot
        ```

        ```bash
        make setup
        ```
        The above commands: 

        * Creates and activate a virtual environmnent (.data2bot) at the root directory
        * Installs all neccessary packages needed to successfully run the project
        * And finally creates a configuration file (config.ini) for setting up the Database connections, etc.
        
        After running the above script, a new configuration file will be added to the project directory `config.ini`. Make sure to set up all necessary configurations for the database. 

        Now run the command below on terminal to start the pipeline:
        ```bash
        make run
        ```
    """
    )


def plot_analytics():
    import altair as alt
    import pandas as pd

    st.markdown(f"# {list(pages.keys())[1]}")
    st.write(
        """
        These dashboards visually summarizes all analysis carried out in the project. Enjoy!
        """
    )
    st.write("\n")
    plot = st.radio(
        "Select Analysis",
        ["Public Holiday Orders", "Shipment Deliveries", "Best Performing Product"],
        horizontal=False,
    )
    if plot.lower() == "public holiday orders":

        st.header("Public Holiday Orders")
        st.write(
            "The total number of orders placed on a public holiday every month, for the past year"
        )
        st.write("#### ")
        df = pd.read_csv("../data2bot/data/transformed/agg_public_holiday.csv")
        df = df.set_index("ingestion_date")
        df = df.T.reset_index()

        df = pd.melt(df, id_vars=["index"]).rename(
            columns={"index": "month", "value": "total_orders"}
        )

        chart = (
            alt.Chart(df)
            .mark_area(opacity=0.5)
            .encode(
                x="ingestion_date:T",
                y=alt.Y("total_orders:Q", stack=None),
                color="month:N",
            )
        )

        st.altair_chart(chart, use_container_width=True)

    elif plot.lower() == "shipment deliveries":

        st.header("Shipments")
        st.write("The total number of Late shipments Vs. Undelivered shipments")
        df = pd.read_csv("../data2bot/data/transformed/agg_shipments.csv")
        df = df.set_index("ingestion_date")

        col1, col2 = st.columns(2)
        col1.metric("Average Late Shipments", df["tt_late_shipments"].median(), "%")
        col2.metric(
            "Average Undelivered Orders", df["tt_undelivered_items"].median(), "%"
        )

        df = df.T.reset_index()
        df = pd.melt(df, id_vars=["index"]).rename(
            columns={"index": "month", "value": "deliveries"}
        )

        chart = (
            alt.Chart(df)
            .mark_line()
            .encode(
                x="ingestion_date:T",
                y=alt.Y("deliveries:Q", stack=None),
                color="month:N",
            )
        )
        st.altair_chart(chart, use_container_width=True)

    else:
        col1, col2 = st.columns(2)
        col1.metric("Most Ordered Date", "70 °F", "1.2 °F")
        col2.metric("Wind", "9 mph", "-8%")


pages = {"—": intro, "Dashboards": plot_analytics}

d2b = st.sidebar.selectbox("Menu", pages.keys())
pages[d2b]()
