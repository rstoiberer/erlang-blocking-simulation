# Richard Stoiberer, CMS 380, Dr. Myers

import numpy as np
import math

# Erlang-B formula implementation using factorial (for comparison)
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

# M/M/c/c queue simulation with two-stage Erlang service times
class MMccErlangSimulator:
    def __init__(self, arrival_rate, service_time, num_servers):
        """
        Initialize simulation parameters
        arrival_rate: λ, rate of arrivals (Poisson process)
        service_time: s, average total service time
        num_servers: c, number of servers
        """
        self.arrival_rate = arrival_rate
        self.service_time = service_time
        self.num_servers = num_servers
        
        # Statistics
        self.total_arrivals = 0
        self.blocked_arrivals = 0
        
        # System state
        self.current_time = 0
        self.num_in_system = 0
        self.event_list = []
    
    def generate_interarrival_time(self):
        """Generate exponentially distributed interarrival time"""
        return np.random.exponential(1/self.arrival_rate)
    
    def generate_service_time(self):
        """
        Generate two-stage Erlang service time by adding two exponential
        random variables, each with mean service_time/2
        """
        # Two-stage Erlang: sum of two exponentials each with mean service_time/2
        return np.random.exponential(self.service_time/2) + np.random.exponential(self.service_time/2)
    
    def add_event(self, event_time, event_type):
        """Add event to the event list"""
        self.event_list.append((event_time, event_type))
        self.event_list.sort()  # Sort by event time
    
    def run_simulation(self, max_arrivals=10000):
        """
        Run the simulation until max_arrivals is reached
        Returns the blocking probability
        """
        # Reset statistics and state
        self.total_arrivals = 0
        self.blocked_arrivals = 0
        self.current_time = 0
        self.num_in_system = 0
        self.event_list = []
        
        # Schedule first arrival
        self.add_event(self.generate_interarrival_time(), "arrival")
        
        # Main simulation loop
        while self.total_arrivals < max_arrivals and self.event_list:
            # Get next event
            event_time, event_type = self.event_list.pop(0)
            self.current_time = event_time
            
            if event_type == "arrival":
                # Process arrival event
                self.total_arrivals += 1
                
                # Schedule next arrival
                self.add_event(self.current_time + self.generate_interarrival_time(), "arrival")
                
                if self.num_in_system < self.num_servers:
                    # System not full, accept customer
                    self.num_in_system += 1
                    
                    # Schedule departure
                    self.add_event(self.current_time + self.generate_service_time(), "departure")
                else:
                    # System full, block customer
                    self.blocked_arrivals += 1
            
            elif event_type == "departure":
                # Process departure event
                self.num_in_system -= 1
        
        # Calculate blocking probability
        return self.blocked_arrivals / self.total_arrivals if self.total_arrivals > 0 else 0

# Find servers needed for target blocking probability (simulation)
def find_servers_needed_erlang(arrival_rate, service_time, target_prob, 
                               max_arrivals=100000, num_trials=5):
    """
    Find the minimum number of servers needed to achieve target blocking probability
    with two-stage Erlang service times
    """
    # Start with the offered load as initial guess
    offered_load = arrival_rate * service_time
    servers = int(offered_load)
    
    while True:
        # Run multiple trials
        sim_results = []
        print(f"\nTrying {servers} servers:")
        
        for trial in range(num_trials):
            simulator = MMccErlangSimulator(arrival_rate, service_time, servers)
            blocking_prob = simulator.run_simulation(max_arrivals)
            sim_results.append(blocking_prob)
            print(f"  Trial {trial+1}: Blocking probability = {blocking_prob*100:.6f}%")
        
        # Calculate average blocking probability
        avg_blocking_prob = sum(sim_results) / len(sim_results)
        print(f"  Average blocking probability: {avg_blocking_prob*100:.6f}%")
        
        if avg_blocking_prob <= target_prob:
            # Found enough servers
            return servers, avg_blocking_prob
        
        # Try more servers
        servers += 1

def main():
    """
    Compare blocking probabilities for exponential vs two-stage Erlang service times
    """
    # Parameters as specified in the assignment
    arrival_rate = 10  # λ = 10
    service_time = 1   # s = 1 (total mean)
    target_prob = 0.01  # Target blocking probability: 1%
    
    print("M/M/c/c Queue with Two-Stage Erlang Service Times")
    print("=================================================")
    print(f"Parameters:")
    print(f"  Arrival rate (λ): {arrival_rate}")
    print(f"  Service time (s): {service_time}")
    print(f"  Each Erlang stage has mean {service_time/2} (total mean {service_time})")
    print(f"  Target blocking probability: {target_prob*100:.1f}%")
    
    # Calculate for exponential service times (theoretical)
    offered_load = arrival_rate * service_time
    servers_exp = 0
    for m in range(int(offered_load), 100):
        if erlang_b(m, offered_load) <= target_prob:
            servers_exp = m
            break
    
    print("\nExponential service times (from first part):")
    print(f"  Required servers: {servers_exp}")
    print(f"  Blocking probability: {erlang_b(servers_exp, offered_load)*100:.6f}%")
    
    # Calculate for two-stage Erlang service times (simulation)
    print("\nTwo-stage Erlang service times (simulation):")
    servers_erlang, prob_erlang = find_servers_needed_erlang(
        arrival_rate, service_time, target_prob)
    
    print("\nResults summary:")
    print(f"  Required servers with Erlang service times: {servers_erlang}")
    print(f"  Blocking probability: {prob_erlang*100:.6f}%")
    
    # Comparison
    print("\nComparison:")
    print(f"  Exponential service times: {servers_exp} servers required")
    print(f"  Two-stage Erlang service times: {servers_erlang} servers required")
    print(f"  Difference: {abs(servers_erlang - servers_exp)} servers")
    
    if servers_erlang > servers_exp:
        print("\nAnalysis: Two-stage Erlang distribution requires MORE servers than exponential.")
        print("This is because the Erlang distribution has lower variance (coefficient of")
        print("variation 1/√2 ≈ 0.707) compared to exponential (coefficient of variation 1).")
        print("With less variability in service times, more servers are needed because the")
        print("system cannot benefit as much from the statistical multiplexing effect that")
        print("comes with high variability.")
    elif servers_erlang < servers_exp:
        print("\nAnalysis: Two-stage Erlang distribution requires FEWER servers than exponential.")
        print("This is an interesting result, as typically less variable service times require")
        print("more capacity. The Erlang distribution has lower variance (coefficient of")
        print("variation 1/√2 ≈ 0.707) compared to exponential (coefficient of variation 1).")
    else:
        print("\nAnalysis: Both distributions require the same number of servers.")
        print("This suggests that for this specific arrival rate and blocking probability target,")
        print("the reduced variability of the Erlang distribution doesn't impact capacity requirements.")

if __name__ == "__main__":
    main()