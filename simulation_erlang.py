# Richard Stoiberer, CMS 380, Dr. Myers

import numpy as np
import math
from collections import deque
import heapq

# Erlang-B formula implementation using factorial
def erlang_b(m, E):
    """
    Calculate blocking probability using Erlang-B formula
    m: number of servers
    E: offered load (λs)
    """
    # Numerator: E^m / m!
    numerator = (E ** m) / math.factorial(m)
    
    # Denominator: sum(E^j / j!) for j from 0 to m
    denominator = 0
    for j in range(m + 1):
        denominator += (E ** j) / math.factorial(j)
    
    # Return blocking probability
    return numerator / denominator

# Binary search to find number of servers needed for target blocking probability
def find_servers_needed(E, target_prob):
    """
    Find minimum number of servers needed to achieve a target blocking probability
    E: offered load
    target_prob: target blocking probability
    """
    # Initial search range
    lower = int(E)  # Minimum servers needed is typically around the offered load
    upper = int(E * 3)  # Upper bound estimate
    
    # Expand upper bound if needed
    while erlang_b(upper, E) > target_prob:
        upper *= 2
    
    # Binary search
    while lower < upper - 1:
        mid = (lower + upper) // 2
        prob = erlang_b(mid, E)
        
        if prob > target_prob:
            lower = mid
        else:
            upper = mid
    
    return upper  # Return the minimum number of servers that meets requirement

# M/M/c/c queue simulation
class MMccSimulation:
    def __init__(self, arrival_rate, service_time, num_servers):
        """
        Initialize simulation parameters
        arrival_rate: λ, rate of arrivals (Poisson process)
        service_time: s, average service time (exponentially distributed)
        num_servers: c, number of servers
        """
        self.arrival_rate = arrival_rate
        self.service_time = service_time
        self.num_servers = num_servers
        self.reset()
    
    def reset(self):
        """Reset simulation state"""
        self.current_time = 0
        self.num_customers = 0
        self.event_queue = []
        self.total_arrivals = 0
        self.blocked_arrivals = 0
        
        # Schedule first arrival
        arrival_time = self.generate_interarrival_time()
        heapq.heappush(self.event_queue, (arrival_time, "arrival", None))
    
    def generate_interarrival_time(self):
        """Generate exponentially distributed interarrival time"""
        return np.random.exponential(1/self.arrival_rate)
    
    def generate_service_time(self):
        """Generate exponentially distributed service time"""
        return np.random.exponential(self.service_time)
    
    def run(self, max_arrivals=10000):
        """
        Run simulation until max_arrivals is reached
        max_arrivals: maximum number of arrivals to simulate
        """
        while self.total_arrivals < max_arrivals and self.event_queue:
            # Get next event
            time, event_type, server_id = heapq.heappop(self.event_queue)
            self.current_time = time
            
            if event_type == "arrival":
                # Process arrival
                self.total_arrivals += 1
                
                # Schedule next arrival
                next_arrival = self.current_time + self.generate_interarrival_time()
                heapq.heappush(self.event_queue, (next_arrival, "arrival", None))
                
                if self.num_customers < self.num_servers:
                    # Customer can be served
                    self.num_customers += 1
                    
                    # Schedule departure
                    departure_time = self.current_time + self.generate_service_time()
                    heapq.heappush(self.event_queue, (departure_time, "departure", None))
                else:
                    # System is full, customer is blocked
                    self.blocked_arrivals += 1
            
            elif event_type == "departure":
                # Process departure
                self.num_customers -= 1
        
        # Calculate blocking probability
        return self.blocked_arrivals / self.total_arrivals if self.total_arrivals > 0 else 0

# Main analysis
def main():
    # Parameters
    arrival_rate = 10  # λ = 10
    service_time = 1   # s = 1
    offered_load = arrival_rate * service_time  # E = λs = 10
    
    print(f"Parameters: λ = {arrival_rate}, s = {service_time}, E = {offered_load}")
    
    # Part 1: Find required servers using Erlang-B formula
    target_probs = [0.1, 0.01, 0.001]  # 10%, 1%, 0.1%
    
    print("\nPart 1: Required servers based on Erlang-B formula:")
    for target in target_probs:
        servers = find_servers_needed(offered_load, target)
        print(f"For blocking probability < {target*100}%: {servers} servers required")
        print(f"  Actual blocking probability: {erlang_b(servers, offered_load)*100:.6f}%")
    
    # Part 2: Verify with simulation
    print("\nPart 2: Simulation verification:")
    
    for target in target_probs:
        servers = find_servers_needed(offered_load, target)
        print(f"\nVerifying {servers} servers for target < {target*100}%:")
        
        # Run 5 trials
        sim_results = []
        for trial in range(5):
            sim = MMccSimulation(arrival_rate, service_time, servers)
            blocking_prob = sim.run(max_arrivals=100000)  # Use large sample for accuracy
            sim_results.append(blocking_prob)
            print(f"  Trial {trial+1}: Blocking probability = {blocking_prob*100:.6f}%")
        
        # Calculate average and compare with theory
        avg_sim = np.mean(sim_results)
        theory = erlang_b(servers, offered_load)
        print(f"  Average simulation result: {avg_sim*100:.6f}%")
        print(f"  Theoretical result: {theory*100:.6f}%")
        print(f"  Difference: {abs(avg_sim-theory)*100:.6f}%")

if __name__ == "__main__":
    main()
