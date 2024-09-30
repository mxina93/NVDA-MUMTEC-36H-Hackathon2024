# NVDA-MUMTEC-36H-Hackathon2024
<br />This is the Predictive Maintanance Model demo from our project.
<br />We have another 2 demo that is Firmware Optimization Model Demo and Decentralized Identity Management System Demo.
<br />The links to the other 2 repository are
<br />Firmware Optimization Model
<br />https://github.com/rabbitmomo/Firmware-Optimization-Model
<br />Decentralized Identity Management System 
<br />https://github.com/lingyuqian0301/Decentralised-identity-management

# Machine Anomaly Detection and Hardware Failure Prediction Demo

## Overview

This demo application leverages machine learning techniques to detect anomalies in machine data and predict potential hardware failures. The application consists of a front-end built with React for user interaction and a back-end model implemented in Python using the Isolation Forest algorithm from the `scikit-learn` library.

## Technologies Used

- **Front-End**: 
  - React.js
  - PapaParse (for CSV parsing)
  - CSS (for styling)

- **Back-End**: 
  - Python
  - Pandas (for data manipulation)
  - Scikit-Learn (for anomaly detection)
  - Matplotlib (optional, for visualization)

# Usage Instructions

### Front-End

1. Open your web browser and go to `http://localhost:3000`.
2. Follow the instructions displayed on the web page to upload a CSV file containing the required machine data.
3. After uploading the file, click on the "Upload and Analyze" button. The application will process the data and display the results.

### Back-End

The back-end script processes the result data file and detects anomalies using the Isolation Forest algorithm. It also evaluates the risk of hardware failure based on the percentage of detected anomalies.

# Data Format

The CSV file should contain the following columns, with numeric values:

- Air temperature [K]
- Process temperature [K]
- Rotational speed [rpm]
- Torque [Nm]
- Tool wear [min]
- Machine failure
- TWF
- HDF
- PWF
- OSF
- RNF

**Note:** The Machine failure and failure type columns should contain binary values (0 or 1).

# Functionality

- **Anomaly Detection:** The application uses the Isolation Forest algorithm to identify anomalies in the provided data.
- **Risk Assessment:** Based on the detected anomalies, the application provides a risk assessment indicating low, medium, or high risk of hardware failure.
- **Results Display:** Detected anomalies and their corresponding risk scores are displayed in a table format for user review.

