#!/usr/bin/python3
import numpy as np
import streamlit as st

# setup page configuration
st.set_page_config(
    layout='wide', page_icon='https://data2bots.com/wp-content/uploads/2018/11/image_1_8-2.png')

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
    import matplotlib.pyplot as plt
    from Handlers.env_handler import env

    st.markdown(f"# {list(page_names_to_funcs.keys())[1]}")
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

        st.header('Public Holiday Orders')
        st.write(
            'The total number of orders placed on a public holiday every month, for the past year')
        st.write("#### Tabular Data")
        df = pd.read_csv("../data2bot/data/transformed/agg_public_holiday.csv")
        df = df.set_index("ingestion_date")
        df = df.T.reset_index()

        df = pd.melt(df, id_vars=["index"]).rename(
            columns={"index": "month",
                     "value": "total_orders"}
        )

        chart = (
            alt.Chart(df)
            .mark_area(opacity=0.5)
            .encode(
                x="ingestion_date",
                y=alt.Y("total_orders:Q", stack=None),
                color="month:N",
            )
        )
        st.altair_chart(chart, use_container_width=True)
        


    elif plot.lower() == "shipment deliveries":
        pass
    else:
        col1, col2 = st.columns(2)
        col1.metric("Most Ordered Date", "70 °F", "1.2 °F")
        col2.metric("Wind", "9 mph", "-8%")



def data_frame_demo():
    import streamlit as st
    import pandas as pd
    import altair as alt
    from urllib.error import URLError

    st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")
    st.write(
        """
        This demo shows how to use `st.write` to visualize Pandas DataFrames.

        (Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)
        """
    )

    @st.cache
    def get_UN_data():
        AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
        df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
        return df.set_index("Region")

    try:
        df = get_UN_data()
        countries = st.multiselect(
            "Choose countries", list(df.index), ["China", "United States of America"]
        )
        if not countries:
            st.error("Please select at least one country.")
        else:
            data = df.loc[countries]
            data /= 1000000.0
            st.write("### Gross Agricultural Production ($B)", data.sort_index())

            data = data.T.reset_index()
            data = pd.melt(data, id_vars=["index"]).rename(
                columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
            )
            chart = (
                alt.Chart(data)
                .mark_area(opacity=0.3)
                .encode(
                    x="year:T",
                    y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                    color="Region:N",
                )
            )
            st.altair_chart(chart, use_container_width=True)
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**

            Connection error: %s
        """
            % e.reason
        )


page_names_to_funcs = {"—": intro,
                       "Dashboards": plot_analytics, 'plot': data_frame_demo}

d2b = st.sidebar.selectbox("Menu", page_names_to_funcs.keys())
page_names_to_funcs[d2b]()
