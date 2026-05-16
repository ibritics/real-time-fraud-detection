<img width="1220" height="537" alt="image" src="https://github.com/user-attachments/assets/d194ddf2-da88-430c-9f4f-ad59fd08639b" />


<br> <br>

**Real-Time Fraud Detection Engine with Apache Kafka & Machine Learning** 
<br>
A high-performance, event-driven streaming pipeline designed to ingest, process, scale, and visualize financial transactions for real-time fraud detection.

This project simulates real-world banking scales by streaming high-dimensional PCA components (matching the standard Kaggle Credit Card Fraud dataset layout) through an asynchronous Apache Kafka broker container, performing low-latency ML inference with automatic feature normalization, and displaying operational metrics in a live dashboard.

<br> **Component Breakdown** <br>
Model & Preprocessing Pipeline (train.py): Downloads the historical dataset, performs a stratified split, executes automated Grid Search tuning across three classification structures (Logistic Regression, Random Forest, XGBoost), balances class skews via SMOTE, and serializes both the Champion Model and the MinMaxScaler artifact to prevent data leakage.

Asynchronous Ingestion Broker (Docker / Kafka): Acts as an immutable log buffer to ingest transaction arrays under sub-millisecond network thresholds.

Data Stream Simulator (stream_producer.py): Connects to the local Kafka broker and sends transaction traffic. It dynamically iterates through all 30 expected feature domains (Time, Amount, V1-V28) based on true mathematical minimum and maximum historical bounds extracted during training.

Inference Consumer Core (stream_consumer.py): Pulls raw data from Kafka, passes it through the exact MinMaxScaler transformation pipeline generated during training, runs predictions, and enriches payloads with system timestamps.

Operational UI (dashboard.py): A Streamlit analytical viewport that monitors incoming transaction metrics, computes live fraud rates, and applies conditional color highlights to highlight fraudulent data points instantly.
<br> 
**Scaling to Production-Grade Big Data (e.g., 20,000+ Tx/s)** <br>
Moving this local project to an enterprise cloud ecosystem requires Horizontal Scaling without changing your core processing logic:

Kafka Partitions & Consumer Groups: By breaking the transactions Kafka topic into multiple parallel streams (Partitions), you can deploy your stream_consumer.py worker script inside a Kubernetes (K8s) Cluster as an autoscale group. Kafka automatically splits partition loads evenly across all active containers.

Swapping the Data Sink: For production volumes, the fraud_data.csv write layer must be swapped out for a distributed NoSQL Time-Series Database (such as Apache Cassandra, ScyllaDB, or Amazon DynamoDB) to handle millions of simultaneous concurrent writes across global infrastructure networks.
<br> 
🚀 **Deployment Instructions**
Prerequisites <br>
Python 3.11+
Docker Desktop (Make sure the application is active and running)
<br>
1. Project Directory Configuration
Ensure your local folder structure perfectly aligns with the required layout before executing scripts:


real-time-fraud-detection/ <br> 
├── models/ <br>
│   ├── feature_bounds.json <br>
│   ├── fraud_samples.json <br>
│   ├── scaler.pkl<br>
│   └── fraud_model.pkl <br>
├── dashboard.py<br> 
├── docker-compose.yml<br>
├── requirements.txt <br>
├── start_project.bat<br>
├── stream_consumer.py <br>
├── stream_producer.py <br>
└── train.py <br>
<br>
2. Automatic Initialization (Windows Batch Script)
Double-click start_project.bat or run it from your command terminal:

<br>
--> start_project.bat
This single orchestration script handles your complete pipeline execution sequence:

Provisions and mounts the Apache Kafka container broker via Docker Compose.

Halts for a 15-second safety cooldown to let internal network ports bind properly.

Automatically fires up train.py to acquire datasets and serialize analytical models.

Generates independent operational terminals for the Stream Consumer Worker, Streamlit Dashboard Web Server, and Transaction Stream Producer.
