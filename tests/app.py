# import libraries
import streamlit as st
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split as tts
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import SimpleImputer, IterativeImputer
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from IPython.display import clear_output
import time
import altair as alt


def detect_anomalies(df, thresholds):
    cpu_threshold, memory_threshold, disk_io_threshold, network_io_threshold = thresholds[:4]
    anomalies = []
    
    for index, row in df.iterrows():
        if (row['CPUUtilization'] > cpu_threshold or
            row['MemoryUtilization'] > memory_threshold or
            row['DiskIO'] > disk_io_threshold or
            row['NetworkIO'] > network_io_threshold):
            anomalies.append(row)
    
    return anomalies    
# st.set_page_config(layout="wide")

st.set_page_config(
    page_title="MetalixAI App",
    page_icon="🧊",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)



# Set the background image
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://w.wallhaven.cc/full/jx/wallhaven-jx7w25.png");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)



# Title with Rainbow Transition Effect and Neon Glow
html_code = """
<div class="title-container">
  <h1 class="neon-text">
    MetalixAI
  </h1>
</div>

<style>
@keyframes rainbow-text-animation {
  0% { color: red; }
  16.67% { color: orange; }
  33.33% { color: yellow; }
  50% { color: green; }
  66.67% { color: blue; }
  83.33% { color: indigo; }
  100% { color: violet; }
}

.title-container {
  text-align: center;
  margin: 1em 0;
  padding-bottom: 10px;
  border-bottom: 4  px solid #fcdee9; /* Magenta underline */
}

.neon-text {
  font-family: Arial, sans-serif;
  font-size: 4em;
  margin: 0;
  animation: rainbow-text-animation 5s infinite linear;
  text-shadow: 0 0 5px rgba(255, 255, 255, 0.8),
               0 0 10px rgba(255, 255, 255, 0.7),
               0 0 20px rgba(255, 255, 255, 0.6),
               0 0 40px rgba(255, 0, 255, 0.6),
               0 0 80px rgba(255, 0, 255, 0.6),
               0 0 90px rgba(255, 0, 255, 0.6),
               0 0 100px rgba(255, 0, 255, 0.6),
               0 0 150px rgba(255, 0, 255, 0.6);
}
</style>
"""

st.markdown(html_code, unsafe_allow_html=True)
st.divider()



st.markdown(
    """
    <style>
    .success-message {
        font-family: Arial, sans-serif;
        font-size: 24px;
        color: green;
        text-align: left;
    }
    .unsuccess-message {
        font-family: Arial, sans-serif;
        font-size: 24px;
        color: red;
        text-align: left;
    }
    .prompt-message {
        font-family: Arial, sans-serif;
        font-size: 24px;
        color: #333;
        text-align: center;
    }
    .success-message2 {
        font-family: Arial, sans-serif;
        font-size: 18px;
        color: white;
        text-align: left;
    }
    .message-box {
        text-align: center;
        background-color: white;
        padding: 5px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        font-size: 24px;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True
)



plot_cols = ["CPUUtilization","MemoryUtilization","DiskIO",
             "InstanceUsageHours","DataTransferVolume","StorageUtilization"]

plot_cols_name = ["cpu_utilization","Memory_Utilization","Disk_IO",
             "Instance_Usage_Hours","Data_Transfer_Volume","Storage_Utilization"]
col = st.sidebar.selectbox("Select column for plotting",plot_cols)
col_name = plot_cols_name[plot_cols.index(col)]
thrs_list = [80,115,300,35,250,650]
thrs_val = round(thrs_list[plot_cols.index(col)])
d_thrs_list = [90,130,450,45,350,700]
d_thrs_val = round(d_thrs_list[plot_cols.index(col)])      

if st.sidebar.toggle("Proceed to Plot"):
    if st.sidebar.button("Stop plotting"):
        st.stop()
    # Load the dataset (example data used here, replace with actual CSV loading)
    data_df = pd.read_csv("all_data.csv")

    # Ensure the Timestamp column is in datetime format
    data_df["Timestamp"] = pd.to_datetime(data_df["Timestamp"])

    # Select only the relevant columns
    data_df1 = data_df[["Timestamp", col]].rename(columns={"Timestamp": "timestamp", col: col_name})

    # Set the window size
    window_size = 100  # Adjust this value to keep the desired number of data points

    st.title(f"Real-Time {col_name}")

    # Plotting area
    chart = st.empty()

    # Initialize an empty DataFrame for streaming
    streaming_df = pd.DataFrame(columns=["timestamp", col_name])

    # Function to stream data from data_df1
    def data_stream(data_df1):
        for i in range(len(data_df1)):
            yield data_df1.iloc[i]

    # Stream data and update the plot
    anamoly_button = st.button("Introduce Anomaly")
    for row in data_stream(data_df1):
        if anamoly_button:
            break
        
        new_row = pd.DataFrame([row])
        streaming_df = pd.concat([streaming_df, new_row], ignore_index=True)
        if len(streaming_df) > window_size:
            streaming_df = streaming_df[-window_size:]
        
        # Create an Altair chart with the threshold line
        base = alt.Chart(streaming_df).mark_line().encode(
            x='timestamp:T',
            y=f'{col_name}:Q'
        )
        
        threshold = alt.Chart(pd.DataFrame({'y': [thrs_val]})).mark_rule(strokeDash=[10, 10], color='yellow').encode(
            y='y:Q'
        )
        
        threshold2 = alt.Chart(pd.DataFrame({'y': [d_thrs_val]})).mark_rule(strokeDash=[10, 10], color='red').encode(
            y='y:Q'
        )
        combined_chart = base + threshold + threshold2
        
        with chart.container():
            st.altair_chart(combined_chart, use_container_width=True)
        
        time.sleep(0.01)  # Simulate real-time streaming

    # if st.sidebar.toggle("Proceed to Plot"):
    # Load the dataset
    data_df = pd.read_csv("sample.csv")

    # Ensure the Timestamp column is in datetime format
    data_df["Timestamp"] = pd.to_datetime(data_df["Timestamp"])

    # Select only the relevant columns
    data_df1 = data_df[["Timestamp", col]].rename(columns={"Timestamp": "timestamp", col: col_name})

    # Set the window size
    window_size = 100  # Adjust this value to keep the desired number of data points

    # Plotting area
    chart = st.empty()

    # Initialize an empty DataFrame for streaming
    streaming_df = pd.DataFrame(columns=["timestamp", col_name])

    # Function to stream data from data_df1
    # Function to stream data from data_df1
    def data_stream(data_df1):
        for i in range(len(data_df1)):
            yield data_df1.iloc[i]

    # Initialize a counter for consecutive threshold exceedances
    consecutive_exceedances = 0
    consecutive_exceedances2 = 0
    threshold = thrs_val  # Set your threshold value here
    thresh2 = d_thrs_val
    # Stream data and update the plot
    for row in data_stream(data_df1):
        new_row = pd.DataFrame([row])
        streaming_df = pd.concat([streaming_df, new_row], ignore_index=True)
        if len(streaming_df) > window_size:
            streaming_df = streaming_df[-window_size:]

        # Check if the value exceeds the threshold
        if new_row[col_name].values[0] > threshold:
            consecutive_exceedances += 1
        else:
            consecutive_exceedances = 0

        # Stop the plot if the threshold is exceeded for 5 consecutive timestamps
        if consecutive_exceedances >= 5:
            st.write("Threshold exceeded for 5 consecutive timestamps. Stopping the plot.")
            break
        
        # Check if the value exceeds the threshold
        if new_row[col_name].values[0] > thresh2:
            consecutive_exceedances2 += 1
        else:
            consecutive_exceedances2 = 0

        # Stop the plot if the threshold is exceeded for 5 consecutive timestamps
        if consecutive_exceedances2 >= 2:
            st.write("Threshold critical exceeded for 2 consecutive timestamps. Stopping the plot.")
            break

        # Create an Altair chart with the threshold line
        base = alt.Chart(streaming_df).mark_line().encode(
            x='timestamp:T',
            y=f'{col_name}:Q'
        )

        threshold_line = alt.Chart(pd.DataFrame({'y': [threshold]})).mark_rule(strokeDash=[10, 10], color='yellow').encode(
            y='y:Q'
        )
        threshold2 = alt.Chart(pd.DataFrame({'y': [d_thrs_val]})).mark_rule(strokeDash=[10, 10], color='red').encode(
            y='y:Q'
        )    
        combined_chart = base + threshold_line + threshold2

        with chart.container():
            st.altair_chart(combined_chart, use_container_width=True)

        time.sleep(0.01)  # Simulate real-time streaming
