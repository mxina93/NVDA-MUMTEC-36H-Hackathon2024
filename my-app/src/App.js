import React, { useState } from 'react';
import Papa from 'papaparse';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [anomalies, setAnomalies] = useState([]);
  const [prediction, setPrediction] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      alert('Please select a file first!');
      return;
    }

    setLoading(true);

    Papa.parse(file, {
      complete: (result) => {
        const data = result.data;
        const columns = [
          "Air temperature [K]",
          "Process temperature [K]",
          "Rotational speed [rpm]",
          "Torque [Nm]",
          "Tool wear [min]",
          "Machine failure",
          "TWF",
          "HDF",
          "PWF",
          "OSF",
          "RNF"
        ];

        const anomalies = detectAnomalies(data, columns);
        const [anomaliesWithRisk, predictionResult] = predictHardwareFailure(anomalies, columns);

        setAnomalies(anomaliesWithRisk);
        setPrediction(predictionResult);
        setLoading(false);
      },
      header: true,
      dynamicTyping: true,
    });
  };

  const detectAnomalies = (data, columns) => {
    let anomalies = [];

    columns.forEach(column => {
      if (typeof data[0][column] === 'number') {
        const values = data.map(row => row[column]);
        const Q1 = quantile(values, 0.25);
        const Q3 = quantile(values, 0.75);
        const IQR = Q3 - Q1;
        const lowerBound = Q1 - 1.5 * IQR;
        const upperBound = Q3 + 1.5 * IQR;

        const columnAnomalies = data.filter(row => row[column] < lowerBound || row[column] > upperBound);
        anomalies = [...anomalies, ...columnAnomalies];
      }
    });

    return [...new Set(anomalies)];
  };

  const predictHardwareFailure = (anomalies, columns) => {
    if (anomalies.length === 0) {
      return [[], "No anomalies detected. Low risk of hardware failure."];
    }

    const riskScores = anomalies.map(anomaly => {
      let totalRiskScore = 0;
      let count = 0;

      columns.forEach(column => {
        if (typeof anomaly[column] === 'number') {
          const mean = average(anomalies.map(a => a[column]));
          const std = standardDeviation(anomalies.map(a => a[column]));
          const riskScore = Math.abs((anomaly[column] - mean) / std);
          totalRiskScore += riskScore;
          count++;
        }
      });

      return {
        ...anomaly,
        overall_risk_score: totalRiskScore / count
      };
    });

    const maxRisk = Math.max(...riskScores.map(a => a.overall_risk_score));

    let prediction;
    if (maxRisk > 3) {
      prediction = "High risk of imminent hardware failure. Immediate inspection recommended.";
    } else if (maxRisk > 2) {
      prediction = "Moderate risk of hardware failure. Schedule an inspection soon.";
    } else {
      prediction = "Low risk of hardware failure, but continue monitoring.";
    }

    return [riskScores, prediction];
  };

  const quantile = (arr, q) => {
    const sorted = arr.sort((a, b) => a - b);
    const pos = (sorted.length - 1) * q;
    const base = Math.floor(pos);
    const rest = pos - base;
    if (sorted[base + 1] !== undefined) {
      return sorted[base] + rest * (sorted[base + 1] - sorted[base]);
    } else {
      return sorted[base];
    }
  };

  const average = (arr) => arr.reduce((a, b) => a + b) / arr.length;

  const standardDeviation = (arr) => {
    const avg = average(arr);
    const squareDiffs = arr.map(value => Math.pow(value - avg, 2));
    const avgSquareDiff = average(squareDiffs);
    return Math.sqrt(avgSquareDiff);
  };

  return (
    <div className="App">
      <h1>Machine Anomaly Detection and Hardware Failure Prediction</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} accept=".csv" />
        <button type="submit" disabled={!file || loading}>
          {loading ? 'Processing...' : 'Upload and Analyze'}
        </button>
      </form>
      {loading && <p>Loading...</p>}
      {prediction && (
        <div className="prediction">
          <h2>Hardware Failure Prediction:</h2>
          <p>{prediction}</p>
        </div>
      )}
      {anomalies.length > 0 && (
        <table>
          <thead>
            <tr>
              <th>Air Temperature</th>
              <th>Process Temperature</th>
              <th>Rotational Speed</th>
              <th>Torque</th>
              <th>Tool Wear</th>
              <th>Risk Score</th>
            </tr>
          </thead>
          <tbody>
            {anomalies.map((anomaly, index) => (
              <tr key={index}>
                <td>{anomaly['Air temperature [K]']}</td>
                <td>{anomaly['Process temperature [K]']}</td>
                <td>{anomaly['Rotational speed [rpm]']}</td>
                <td>{anomaly['Torque [Nm]']}</td>
                <td>{anomaly['Tool wear [min]']}</td>
                <td>{anomaly.overall_risk_score.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;