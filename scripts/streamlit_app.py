#!/usr/bin/python3
import numpy as np
import streamlit as st


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
    import time
    import pandas as pd
    import matplotlib.pyplot as plt
    from Handlers.env_handler import env

    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')
    st.write(
        """
        This demo illustrates a combination of plotting and animation with
        Streamlit. We're generating a bunch of random numbers in a loop for around
        5 seconds. Enjoy!
        """
    )
    st.write('\n')
    plot = st.radio('Select Analysis', [
                         'Public Holiday Orders', 'Shipment Deliveries', 'Best Performing Product'], horizontal=True)
    
    if plot.lower() == 'public holiday orders':
        st.write('### Tabular Data')
        df = pd.read_csv("../data2bot/data/transformed/agg_public_holiday.csv")
        df.reset_index()    
        df = df.set_index("ingestion_date")
        st.dataframe(df)


    elif plot.lower() == 'shipment deliveries':
        pass
    else:
        pass

    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 1)
    chart = st.line_chart(last_rows)

    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        status_text.text("%i%% Complete" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        last_rows = new_rows
        time.sleep(0.05)

    progress_bar.empty()


def data_frame_demo():
    import streamlit as st
    import pandas as pd
    import altair as alt
    from urllib.error import URLError

    st.markdown(f"# {list(page_names_to_funcs.keys())[3]}")
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
            "Choose countries", list(df.index), [
                "China", "United States of America"]
        )
        if not countries:
            st.error("Please select at least one country.")
        else:
            data = df.loc[countries]
            data /= 1000000.0
            st.write("### Gross Agricultural Production ($B)",
                     data.sort_index())

            data = data.T.reset_index()
            data = pd.melt(data, id_vars=["index"]).rename(
                columns={"index": "year",
                         "value": "Gross Agricultural Product ($B)"}
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


page_names_to_funcs = {
    "—": intro,
    "Dashboards": plot_analytics
}

d2b = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[d2b]()
