# AnomaAI App

## Overview
The AnomaAI App is designed to detect anomalies in AWS infrastructure by monitoring metrics like CPU utilization, memory utilization, disk I/O, and network I/O. It uses a combination of AWS services and Python libraries for anomaly detection and automated instance management. The app integrates with Streamlit for real-time data visualization and includes automation for instance handling based on detected anomalies.

![image](https://github.com/Rupanshu-Kapoor/formidium-hackathon/assets/121911821/36d9e911-9d44-43c8-b4e1-bb22c36c334e)

## Features
**- Real-Time Anomaly Detection**: Monitors AWS instances in real-time for anomalies.

**- AWS Integration**: Uses AWS SNS for notifications and AWS Lambda for event-driven actions.

**- Instance Management**: Automatically handles instances by rebooting, terminating, or upscaling based on detected anomalies.

**- Visualization**: Provides real-time data visualization using Streamlit and Altair.

**- Synthetic Data Generation**: Generates synthetic data for training and testing the model.

## Workflow
![Blank diagram](https://github.com/Rupanshu-Kapoor/formidium-hackathon/assets/121911821/f067ccd3-072c-43c0-a43e-646ed88309b6)

## Components
**- Synthetic Data Generation** : Generates synthetic data to simulate real-world scenarios and train the autoencoder model.

**- Training Autoencoder**: Uses synthetic data to train an autoencoder model for anomaly detection.

**- AWS Anomaly Detection** : Monitors AWS metrics and triggers a Lambda function upon detecting anomalies.

**- Lambda Function**: Triggers anomaly detection and interacts with the autoencoder model.

**- Autoencoder Model**: Processes incoming data to detect anomalies.

**- Anomaly Detection** : Identifies anomalies and triggers AWS SNS for notifications and actions.

**- AWS SNS (Notifications)** : Sends notifications for detected anomalies.

**- Instance Handler** : Manages AWS instances by rebooting, terminating, or upscaling them based on detected anomalies.

## Prerequisites

**- AWS Account**: Required to set up AWS services such as SNS, Lambda, and EC2.

**- Streamlit**: Install Streamlit for data visualization.

**- Python Libraries**: Ensure the following Python libraries are installed: streamlit, joblib, numpy, pandas, scikit-learn, matplotlib, seaborn, plotly, boto3.

## Installation

1. Clone the repository.
   `git clone https://github.com/your-username/anomaai.git`

2. Install the required Python libraries.
   `pip install -r requirements.txt`

## Usage
1. Run the Streamlit App
`streamlit run app.py`

- Open the app in your browser
- Use the sidebar to select the metric for monitoring.
- The app will automatically stop or upscale instances based on detected anomalies.
- Notifications will be sent via AWS SNS.
