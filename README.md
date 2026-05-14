# real-time-fraud-detection
A simple architecture of a real time fraud detection
<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/29debc27-5ecd-45f6-9cbd-0460a3e9bfb6" />
Project Overview: Real-Time Fraud Inference Pipeline
1. The Vision
The goal of this project was to move away from "Static Analysis" (checking for fraud after the damage is done) toward "Proactive Prevention." By building a system that processes data as it flows, you created a framework where a bank could technically decline a transaction before the money leaves the account.

2. The Workflow Design (The "Complete Picture")
Your project follows a linear, highly efficient data path:

Ingestion (The Producer): Acts as the "Digital Sensor." It creates raw JSON events and pushes them into the cloud/local infrastructure.

Decoupling (The Kafka Broker): This is the most critical design choice. By using Kafka, you ensured that the Bank (Producer) and the Brain (Consumer) don't need to know about each other. They only care about the "Topic."

Intelligence (The ML Consumer): This is where the MLOps happens. The consumer deserializes the Kafka byte-stream, feeds it into a pre-trained Scikit-Learn Random Forest, and determines the "Fraud Probability" in milliseconds.

Serving (The Streamlit Dashboard): Instead of a static report, you built a live UI. It uses a "Polling" mechanism to read the latest sink (CSV) and provide real-time metrics to a human operator.

3. Key Technical Challenges Solved
During this build, you solved several "Senior-level" engineering hurdles:

Environment Isolation: Using Docker Compose to handle complex Kafka networking (listeners, protocols, and port mapping) so the code works on any machine.

Concurrency: Implementing Threading in the consumer. This allows the consumer to keep "listening" to Kafka without pausing while it saves the CSV file every few seconds.

Model Persistence: Using Joblib to save a trained state, allowing you to separate the Learning phase from the Execution phase.

4. Why This Project Stands Out
Most beginners build "Jupyter Notebook" models where the data is already in a clean file. Your project is different because:

It handles "Unbounded" data: Your system never "finishes"; it stays alive as long as transactions exist.

It is scalable: If your transaction volume triples, you can just spin up more Docker containers.

It is user-centric: By adding the Streamlit Dashboard and the One-Click Batch Launcher, you turned a complex set of scripts into a "Product."
