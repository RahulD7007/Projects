# System Log Anomaly Detection via DeepLog LSTMs

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.16-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Tests](https://img.shields.io/badge/Tests-19_Passed-brightgreen)

A complete, production-ready, end-to-end Deep Learning system for infrastructure and distributed systems log anomaly detection using **TensorFlow/Keras** and **Long Short-Term Memory (LSTM)** networks. Strictly adheres to the official **Cookiecutter Data Science (v2)** project standard.

---

## 1. The Problem and Our Solution

### The Challenge for Big Companies

Large computer systems generate huge amounts of log data every single day. IT and security teams struggle with two major issues:

1. **Too Many False Alarms & Burnout:** Old-school monitoring just looks for words like "ERROR". This triggers a lot of fake alerts when the system is just busy, which exhausts the team.
2. **Missing the "Quiet" Failures:** Sometimes, major crashes or hacker attacks don't generate huge error warnings. Instead, they look like normal messages just happening in the wrong order. Traditional rules completely miss these hidden dangers.

### How DeepLog Fixes It

We treat computer logs the same way we treat sentences in a language.

1. **Organize the Mess:** We take messy log text and turn it into simple, numbered event codes.
2. **Learn What's Normal:** We use an AI model (a Stacked LSTM) to study the system when it is perfectly healthy. It learns the "grammar" of the system.
3. **Detect Deviations:** If a new event doesn't fit the grammar (isn't in the Top-K predictions), we flag it as an anomaly.

## 2. Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the entire pipeline
make all

# Run unit tests
make test
