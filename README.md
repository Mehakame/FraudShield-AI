# 🛡️ FraudShield AI

### Behavioral + Graph-Based Social Engineering Fraud Detection System

FraudShield AI is an academic fraud-detection prototype designed to identify suspicious digital payment transactions using a combination of behavioral intelligence, machine learning, and graph-based mule-account analysis.

Unlike traditional fraud systems that rely only on transaction amount or account history, FraudShield analyzes both the user's real-time behavioral signals and the receiver's transaction network before producing a risk decision.

---

## 🚨 Problem Statement

Social-engineering scams often convince legitimate users to voluntarily initiate payments while they are under pressure, on a phone call, or following instructions from a scammer.

From the bank's perspective, such transactions may initially appear legitimate because:

- the correct device is being used,
- the legitimate account owner is initiating the payment,
- authentication may be valid,
- and the payment itself may follow standard transaction rules.

FraudShield explores whether behavioral telemetry and graph-based account analysis can provide additional fraud signals before a payment is completed.

---

# 💡 Proposed Solution

FraudShield uses two major fraud-detection layers.

## 1. Behavioral Fraud Detection

The Android application collects prototype behavioral signals such as:

- typing pause duration
- typing variation
- device movement
- call-state signal
- transaction amount
- new beneficiary status
- transaction time
- previous transaction history

These features are sent to a machine-learning model that generates a behavioral fraud probability.

---

## 2. Graph-Based Mule Account Detection

Neo4j is used to represent transactions as a graph.

Example:

```text
VICTIM101 ─┐
VICTIM102 ─┼──> MULE100 ──> MULE200 ──> MULE300
VICTIM103 ─┘           ├──> MULE201
                       └──> MULE202
```

FraudShield evaluates graph indicators including:

- multiple unique senders
- multiple outgoing receivers
- high transaction velocity
- rapid pass-through behavior
- multi-hop fund movement
- reachable accounts
- 2–3 hop transaction chains

This allows the prototype to detect suspicious receiver networks even when the payer's behavioral signals appear normal.

---

# 🧠 System Architecture

```text
             Android Payment App
                     │
                     ▼
          Behavioral Telemetry
                     │
                     ▼
                FastAPI
              /         \
             /           \
            ▼             ▼
   Random Forest ML     Neo4j
   Behavioral Risk     Graph Risk
            \             /
             \           /
                ▼
         Combined Risk Engine
                │
        ┌───────┼─────────┐
        ▼       ▼         ▼
      ALLOW    WARN      HOLD
```

---

# ⚙️ Technology Stack

### Android

- Kotlin
- Jetpack Compose
- Retrofit
- Android Sensor APIs
- TelecomManager
- SQLite

### Backend

- Python
- FastAPI
- Uvicorn

### Machine Learning

- Scikit-learn
- Random Forest
- Pandas
- NumPy
- Joblib

### Graph Analytics

- Neo4j AuraDB
- Neo4j Python Driver
- Cypher Query Language

---

# 📊 Machine Learning Features

The ML model uses:

```text
amount
new_payee
on_call
typing_pause
typing_variance
device_movement
transaction_hour
previous_transactions
```

The model predicts the probability that a transaction belongs to the suspicious/fraud class.

---

# 🔍 Explainable AI

FraudShield does not only return a fraud score.

It also provides explanations such as:

- New beneficiary detected
- User currently on phone call
- Long typing pause detected
- Unusual device movement
- Multiple unique senders detected
- High transaction velocity
- Multi-hop transaction network detected
- Rapid fund movement detected

This helps make the prototype's decision easier to understand.

---

# 🚦 Risk Decisions

| Risk Score | Risk Level | Prototype Action |
|------------|------------|------------------|
| 0–29 | LOW | ALLOW |
| 30–69 | MEDIUM | WARN |
| 70–100 | HIGH | HOLD |

---

# 🧪 Example Scenarios

## Scenario 1 — Normal Transaction

```text
Behavioral Risk: LOW
Graph Risk: LOW
Final Risk: LOW

Action: ALLOW
```

---

## Scenario 2 — Suspicious Behavioral Signals

```text
Behavioral Risk: HIGH
Graph Risk: LOW
Final Risk: HIGH

Action: HOLD
```

---

## Scenario 3 — Mule Account Detection

The payer demonstrates normal behavior:

```text
Behavioral Risk: LOW
```

but the receiver is part of a suspicious transaction network:

```text
Graph Risk: HIGH
Graph Risk Score: 100%
```

FraudShield therefore produces:

```text
Final Risk: HIGH
Action: HOLD
```

This demonstrates why combining behavioral and graph intelligence can detect risks that either system alone may miss.

---

# 📈 Model Evaluation

The prototype evaluates the ML model using:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC
- Confusion Matrix

Evaluation results are generated using:

```bash
python models/evaluate_model.py
```

> Important: The machine-learning model is currently trained and evaluated on synthetically generated academic data. Reported performance should not be interpreted as real-world banking fraud accuracy.

---

# 🕸️ Graph Detection

The Neo4j graph engine detects:

```text
Multiple Senders
      ↓
Primary Mule
      ↓
Multiple Receivers
      ↓
Multi-Hop Distribution
```

Advanced indicators include:

- transaction velocity
- fan-in
- fan-out
- pass-through ratio
- reachable accounts
- maximum hop depth
- rapid 2–3 hop chains

---

# ▶️ Running the Project

## 1. Clone the repository

```bash
git clone <repository-url>
cd FraudShield_Ai
```

---

## 2. Create Python environment

```bash
python -m venv venv
```

Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Neo4j

Create:

```text
.env
```

using:

```env
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=your_username
NEO4J_PASSWORD=your_password
```

Never commit the real `.env` file.

---

## 5. Test Neo4j

```bash
python graph_engine/test_graph.py
```

---

## 6. Start FastAPI

```bash
python -m uvicorn backend.api:app --host 0.0.0.0 --port 8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 7. Run Android Application

Open the Android project in Android Studio.

Run the app using:

- Android Emulator, or
- physical Android device.

The Android application's Retrofit base URL should point to the machine running the FastAPI backend.

---

# 🧪 System Testing

Run:

```bash
python backend/test_system.py
```

Example tests include:

1. Normal behavior + normal receiver
2. Suspicious behavior + normal receiver
3. Normal behavior + mule receiver
4. Suspicious behavior + mule receiver

---

# 🔐 Privacy & Safety

FraudShield is an academic prototype.

The application does not require or collect:

- real UPI PINs
- banking passwords
- OTPs
- card PINs

Behavioral and graph signals are treated as risk indicators and should not independently be considered proof of fraud.

---

# ⚠️ Limitations

- ML training data is synthetic.
- The current graph-risk rules are heuristic.
- Device-motion signals alone cannot prove fraud.
- Phone-call state alone cannot prove social engineering.
- Real banking deployment would require regulated datasets, privacy controls, security reviews, fairness testing, and financial-institution integration.

---

# 🔮 Future Scope

Future improvements may include:

- Graph Neural Networks
- temporal graph learning
- real-time streaming transactions
- account reputation scoring
- device-risk intelligence
- explainable ML models
- federated learning
- anomaly detection
- scam-call intelligence
- continuous model monitoring

---

# 🎓 Project Type

Academic / Research Prototype

B.Tech Computer Science & Engineering

---

# 📌 Disclaimer

FraudShield AI is a proof-of-concept developed for educational and research purposes. It is not a production banking or payment-security system.
## 📄 License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.