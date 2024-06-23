import pytest
import pandas as pd
from datetime import datetime

# Anomaly detection function (imported from your application module)
from app import detect_anomalies


df = pd.read_csv("all_data.csv")
df = df[:5000]
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# List of threshold values
thrs_list = [80, 115, 300, 35, 650]  # Adjusted for removed NetworkIO

# Test cases
@pytest.mark.parametrize("thresholds", [
    [80, 90, 300, 35, 650],
    [80, 115, 300, 35, 650],
    [80, 115, 300, 35, 600],
])
def test_detect_anomalies(thresholds):
    anomalies = detect_anomalies(df, thresholds)
    assert isinstance(anomalies, list)

def test_no_anomalies():
    thresholds = [5000, 5000,5000,5000]  # Using thresholds where no anomalies should be detected
    anomalies = detect_anomalies(df, thresholds)
    assert len(anomalies) == 0

def test_missing_data():
    df_missing = df.copy()
    df_missing.loc[0, 'CPUUtilization'] = None
    is_null = df_missing.isnull().sum().sum()
    assert is_null > 0

def test_different_user_ids():
    df_users = df.copy()
    unique_users = df_users["UserId"].unique()
    df_users.loc[1, 'UserId'] = 'user_21'
    assert len(unique_users) < len(df_users["UserId"].unique())

def test_high_variance():
    df_variance = df.copy()
    initial_variance = df_variance["CPUUtilization"].var()
    df_variance.loc[0, 'CPUUtilization'] += 30000
    new_variation = df_variance["CPUUtilization"].var()
    assert new_variation > initial_variance

def test_correct_anomaly_detection():
    thresholds = [80, 115, 300, 35, 650]
    anomalies = detect_anomalies(df, thresholds)
    assert anomalies[0]['Timestamp'] == pd.to_datetime("2024-05-24 01:56:33.587948")

# def test_edge_cases():
#     thresholds = [47.05223998749498, 68.48213001056598, 69.52091553810372, 18, 41.135713464747056, 415.79212081219725]
#     anomalies = detect_anomalies(df, thresholds)
#     assert len(anomalies) == 6

# def test_performance():
#     thresholds = [80, 115, 300, 35, 650]
#     large_data = df 
#     large_df = pd.DataFrame(large_data)
#     large_df['Timestamp'] = pd.to_datetime(large_df['Timestamp'])
#     anomalies = detect_anomalies(large_df, thresholds)
#     assert len(anomalies) > 0

def test_incorrect_data_types():
    df_incorrect_types = df.copy()
    df_incorrect_types['CPUUtilization'] = df_incorrect_types['CPUUtilization'].astype(str)
    thresholds = [80, 115, 300, 35, 650]
    with pytest.raises(TypeError):
        detect_anomalies(df_incorrect_types, thresholds)



if __name__ == "__main__":
    pytest.main()
