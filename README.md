# -End-to-End-Process-Analytics-for-Workflow-Optimization-
Process Analytics project

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Snowflake](https://img.shields.io/badge/Snowflake-Enabled-lightgrey)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Random%20Forest%20%7C%20K--Means-orange)

## 1. Project Background
In complex Enterprise Data Management (EDM) systems, data entities traverse dozens of tables, undergoing various transformations, updates, and overrides. Currently, there is a lack of a unified, domain-free perspective on how these entities flow through the system. This project establishes an automated analytics pipeline to trace data lineage across EDM data tables, map process flows, and classify the underlying contexts of these data paths.

## 2. Business Value & Objective
Modern EDM environments generate massive telemetry and operational data, but extracting actionable process intelligence is heavily reliant on manual, domain-specific knowledge. By moving toward **full-link data monitoring**, this project allows us to:
*   **Automate Primary Key & Schema Discovery:** Programmatically identify relational links and date-time columns without hardcoded data dictionaries.
*   **Uncover Hidden Contexts:** Systematically discover what features (e.g., asset class, currency) dictate different processing routes.
*   **Identify Processing Bottlenecks:** Differentiate between normal Straight Through Processing (STP) and non-STP flows by mapping explicit process durations and timestamp deltas.
*   **Bridge the Gap Between Data and Product:** Transform raw table logs into a clear view of the data's operational life cycle, enabling better product management and system optimization.

## 3. System Architecture & Flow

The pipeline is designed to be highly modular, extracting data securely from the warehouse, applying unsupervised and supervised learning, and outputting probabilistic process maps.

```mermaid
graph TD
    A[(Snowflake Data Warehouse)] -->|RSA Auth Extraction| B(Data Loader Module)
    B --> C{Phase 1: Heuristics & Discovery}
    C -->|Stats & Entropy| D[Identify Date-Time Cols]
    C -->|JS Divergence| E[Map Primary Keys & Relations]
    D --> F{Phase 2: ML Clustering & Context}
    E --> F
    F -->|MCA & K-Means| G[Cluster PKs by Traversal Behavior]
    F -->|Random Forest| H[Extract Feature Importance/Context]
    G --> I{Phase 3: Process Mapping}
    H --> I
    I -->|Markov Chains| J[Calculate Sequence Probabilities]
    I -->|Time Deltas| K[Classify STP vs. Non-STP Latency]
    J --> L([Final Output: Lineage Maps & Matrices])
    K --> L
