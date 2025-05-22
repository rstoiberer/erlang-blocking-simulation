# 📞 Erlang-B Blocking Probability Simulator  
**M/M/c/c Queueing Simulation with Exponential and Erlang Service Times**

This project models an M/M/c/c queue — a loss system with no buffer — to analyze blocking probabilities. It compares theoretical results using the Erlang-B formula with simulation-based estimates using both exponential and two-stage Erlang-distributed service times.

---

## 📚 Project Context

Agner Erlang, a Danish engineer and mathematician, created foundational models of telephone traffic in the early 1900s. This project replicates one such model: the **M/M/c/c queue**, where:

- Customers arrive via a **Poisson process (λ)**
- Service times are **exponentially distributed (s)** or follow a **two-stage Erlang distribution**
- There are **c servers** and **no waiting queue**: blocked calls are dropped

---

## 🔍 What This Project Does

- Implements the **Erlang-B formula** to compute theoretical blocking probabilities
- Uses **binary search** to determine the number of servers needed for desired performance
- Simulates an **M/M/c/c system** with both:
  - Exponentially distributed service times
  - Two-stage Erlang service times (sum of two exponentials)
- Compares theoretical and simulated blocking probabilities across multiple trials

---

## 🧪 Key Concepts

- **Erlang-B Formula:**  
  Calculates the probability that a customer is blocked in an M/M/c/c system:
  
  Blocking probability:
  ```
  B(m, E) = (E^m / m!) / Σ_{j=0}^m (E^j / j!)
  ```
- **Erlang Service Time:**  
  Two-stage Erlang is generated as:  
  ```
  np.random.exponential(s/2) + np.random.exponential(s/2)
  ```
  Blocking Probability:
Simulated as the fraction of customers dropped when all servers are busy.

---

## 📈 Example Output

- Output **simulation_erlang.py**

```text
  Parameters: λ = 10, s = 1, E = 10

Part 1: Required servers based on Erlang-B formula:
For blocking probability < 10.0%: 13 servers required
  Actual blocking probability: 8.433886%
For blocking probability < 1.0%: 18 servers required
  Actual blocking probability: 0.714244%
For blocking probability < 0.1%: 21 servers required
  Actual blocking probability: 0.088923%

Part 2: Simulation verification:

Verifying 13 servers for target < 10.0%:
  Trial 1: Blocking probability = 8.180000%
  Trial 2: Blocking probability = 8.564000%
  Trial 3: Blocking probability = 8.540000%
  Trial 4: Blocking probability = 8.466000%
  Trial 5: Blocking probability = 8.472000%
  Average simulation result: 8.444400%
  Theoretical result: 8.433886%
  Difference: 0.010514%

Verifying 18 servers for target < 1.0%:
  Trial 1: Blocking probability = 0.800000%
  Trial 2: Blocking probability = 0.783000%
  Trial 3: Blocking probability = 0.692000%
  Trial 4: Blocking probability = 0.725000%
  Trial 5: Blocking probability = 0.776000%
  Average simulation result: 0.755200%
  Theoretical result: 0.714244%
  Difference: 0.040956%

Verifying 21 servers for target < 0.1%:
  Trial 1: Blocking probability = 0.071000%
  Trial 2: Blocking probability = 0.082000%
  Trial 3: Blocking probability = 0.098000%
  Trial 4: Blocking probability = 0.080000%
  Trial 5: Blocking probability = 0.111000%
  Average simulation result: 0.088400%
  Theoretical result: 0.088923%
  Difference: 0.000523%  
```

- Output **simulation_erlang_two_stage.py**

```text
  M/M/c/c Queue with Two-Stage Erlang Service Times
=================================================
Parameters:
  Arrival rate (λ): 10
  Service time (s): 1
  Each Erlang stage has mean 0.5 (total mean 1)
  Target blocking probability: 1.0%

Exponential service times (from first part):
  Required servers: 18
  Blocking probability: 0.714244%

Two-stage Erlang service times (simulation):

Trying 10 servers:
  Trial 1: Blocking probability = 21.665000%
  Trial 2: Blocking probability = 21.349000%
  Trial 3: Blocking probability = 21.237000%
  Trial 4: Blocking probability = 21.670000%
  Trial 5: Blocking probability = 21.278000%
  Average blocking probability: 21.439800%

Trying 11 servers:
  Trial 1: Blocking probability = 16.272000%
  Trial 2: Blocking probability = 16.450000%
  Trial 3: Blocking probability = 16.495000%
  Trial 4: Blocking probability = 16.331000%
  Trial 5: Blocking probability = 16.258000%
  Average blocking probability: 16.361200%

Trying 12 servers:
  Trial 1: Blocking probability = 12.053000%
  Trial 2: Blocking probability = 12.045000%
  Trial 3: Blocking probability = 11.769000%
  Trial 4: Blocking probability = 11.774000%
  Trial 5: Blocking probability = 12.156000%
  Average blocking probability: 11.959400%

Trying 13 servers:
  Trial 1: Blocking probability = 8.372000%
  Trial 2: Blocking probability = 8.506000%
  Trial 3: Blocking probability = 8.170000%
  Trial 4: Blocking probability = 8.574000%
  Trial 5: Blocking probability = 8.279000%
  Average blocking probability: 8.380200%

Trying 14 servers:
  Trial 1: Blocking probability = 5.613000%
  Trial 2: Blocking probability = 5.617000%
  Trial 3: Blocking probability = 5.598000%
  Trial 4: Blocking probability = 5.562000%
  Trial 5: Blocking probability = 5.736000%
  Average blocking probability: 5.625200%

Trying 15 servers:
  Trial 1: Blocking probability = 3.603000%
  Trial 2: Blocking probability = 3.629000%
  Trial 3: Blocking probability = 3.708000%
  Trial 4: Blocking probability = 3.587000%
  Trial 5: Blocking probability = 3.626000%
  Average blocking probability: 3.630600%

Trying 16 servers:
  Trial 1: Blocking probability = 2.261000%
  Trial 2: Blocking probability = 2.151000%
  Trial 3: Blocking probability = 2.253000%
  Trial 4: Blocking probability = 2.366000%
  Trial 5: Blocking probability = 2.257000%
  Average blocking probability: 2.257600%

Trying 17 servers:
  Trial 1: Blocking probability = 1.357000%
  Trial 2: Blocking probability = 1.334000%
  Trial 3: Blocking probability = 1.289000%
  Trial 4: Blocking probability = 1.303000%
  Trial 5: Blocking probability = 1.254000%
  Average blocking probability: 1.307400%

Trying 18 servers:
  Trial 1: Blocking probability = 0.694000%
  Trial 2: Blocking probability = 0.737000%
  Trial 3: Blocking probability = 0.722000%
  Trial 4: Blocking probability = 0.757000%
  Trial 5: Blocking probability = 0.765000%
  Average blocking probability: 0.735000%

Results summary:
  Required servers with Erlang service times: 18
  Blocking probability: 0.735000%

Comparison:
  Exponential service times: 18 servers required
  Two-stage Erlang service times: 18 servers required
  Difference: 0 servers

Analysis: Both distributions require the same number of servers.
This suggests that for this specific arrival rate and blocking probability target,
the reduced variability of the Erlang distribution doesn't impact capacity requirements.
```

---

## 🧠 Goals & Takeaways

- Understand and apply Erlang-B theory
- Compare theoretical vs. simulated system performance
- See how service time variability affects capacity needs

---

## 🙏 Credits

This project was inspired by and based on starter code provided by
**Dr. Dan S. Myers**, Rollins College for the course **Simulation & Stochastic**.

---

## 🚀 How to Run the Simulation

1. Clone the Repository
   
```text
git clone https://github.com/rstoiberer/erlang-blocking-simulation.git
cd erlang-blocking-simulation
```

2. Install Dependencies

Make sure you have Python and NumPy installed. If you use a virtual environment, activate it first. Then:
```text
pip install -r requirements.txt
```
**Note**: If you don’t have a requirements.txt, you can create one with:
```text
echo numpy > requirements.txt
```

3. Run the **Exponential Service Time Simulation**
   
This script calculates theoretical blocking probabilities using the Erlang-B formula and compares them with simulated values.
```text
python3 simulation_erlang.py
```

4. Run the **Two-Stage Erlang Service Time Simulation**

This script uses service times based on the Erlang-2 distribution to determine how many servers are needed to meet the same blocking thresholds.
```text
python3 simulation_erlang_two_stage.py
```

---
