import matplotlib.pyplot as plt
import numpy as np

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0

class CPUScheduler:
    def __init__(self):
        self.processes = []
        
    def add_process(self, pid, arrival_time, burst_time, priority=0):
        process = Process(pid, arrival_time, burst_time, priority)
        self.processes.append(process)
        
    def fcfs(self):
        processes = sorted(self.processes, key=lambda x: x.arrival_time)
        current_time = 0
        result = []
        
        for process in processes:
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            
            process.waiting_time = current_time - process.arrival_time
            process.completion_time = current_time + process.burst_time
            process.turnaround_time = process.completion_time - process.arrival_time
            current_time = process.completion_time
            
            result.append(process)
        return result

    def sjf(self):
        processes = sorted(self.processes, key=lambda x: x.arrival_time)
        n = len(processes)
        completed = []
        current_time = 0
        
        while len(completed) < n:
            available = [p for p in processes if p.arrival_time <= current_time and p not in completed]
            
            if not available:
                current_time += 1
                continue
                
            process = min(available, key=lambda x: x.burst_time)
            process.waiting_time = current_time - process.arrival_time
            process.completion_time = current_time + process.burst_time
            process.turnaround_time = process.completion_time - process.arrival_time
            current_time = process.completion_time
            
            completed.append(process)
        return completed

    def priority_scheduling(self):
        processes = sorted(self.processes, key=lambda x: x.arrival_time)
        n = len(processes)
        completed = []
        current_time = 0
        
        while len(completed) < n:
            available = [p for p in processes if p.arrival_time <= current_time and p not in completed]
            
            if not available:
                current_time += 1
                continue
                
            process = min(available, key=lambda x: x.priority)
            process.waiting_time = current_time - process.arrival_time
            process.completion_time = current_time + process.burst_time
            process.turnaround_time = process.completion_time - process.arrival_time
            current_time = process.completion_time
            
            completed.append(process)
        return completed

    def get_process_metrics(self, pid):
        process_metrics = {}
        
        # FCFS metrics
        fcfs_result = self.fcfs()
        fcfs_process = next((p for p in fcfs_result if p.pid == pid), None)
        if fcfs_process:
            process_metrics['FCFS'] = {
                'waiting_time': fcfs_process.waiting_time,
                'turnaround_time': fcfs_process.turnaround_time
            }
            
        # SJF metrics
        sjf_result = self.sjf()
        sjf_process = next((p for p in sjf_result if p.pid == pid), None)
        if sjf_process:
            process_metrics['SJF'] = {
                'waiting_time': sjf_process.waiting_time,
                'turnaround_time': sjf_process.turnaround_time
            }
            
        # Priority metrics
        priority_result = self.priority_scheduling()
        priority_process = next((p for p in priority_result if p.pid == pid), None)
        if priority_process:
            process_metrics['Priority'] = {
                'waiting_time': priority_process.waiting_time,
                'turnaround_time': priority_process.turnaround_time
            }
            
        return process_metrics
    
    def find_best_algorithm(self, pid):
        metrics = self.get_process_metrics(pid)
        
        # Compare waiting times
        waiting_times = {algo: values['waiting_time'] 
                        for algo, values in metrics.items()}
        best_waiting = min(waiting_times.items(), key=lambda x: x[1])
        
        # Compare turnaround times
        turnaround_times = {algo: values['turnaround_time'] 
                           for algo, values in metrics.items()}
        best_turnaround = min(turnaround_times.items(), key=lambda x: x[1])
        
        return {
            'best_waiting_time': best_waiting,
            'best_turnaround_time': best_turnaround
        }

    def plot_comparison_graphs(self):
        if not self.processes:
            print("No processes to plot! Please add processes first.")
            return

        # For each process, get its metrics from each algorithm
        for process in self.processes:
            metrics = self.get_process_metrics(process.pid)
            
            # Prepare data for plotting
            algorithms = list(metrics.keys())  # ['FCFS', 'SJF', 'Priority']
            waiting_times = [metrics[algo]['waiting_time'] for algo in algorithms]
            turnaround_times = [metrics[algo]['turnaround_time'] for algo in algorithms]

            # Create two subplots for each process
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
            fig.suptitle(f'Process {process.pid} Metrics')

            # Plot waiting times
            bars1 = ax1.bar(algorithms, waiting_times, color=['skyblue', 'lightgreen', 'lightcoral'])
            ax1.set_xlabel('Algorithms')
            ax1.set_ylabel('Waiting Time')
            ax1.set_title(f'Waiting Time Comparison for Process {process.pid}')
            
            # Add value labels on top of each bar
            for bar in bars1:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height}',
                        ha='center', va='bottom')

            # Plot turnaround times
            bars2 = ax2.bar(algorithms, turnaround_times, color=['skyblue', 'lightgreen', 'lightcoral'])
            ax2.set_xlabel('Algorithms')
            ax2.set_ylabel('Turnaround Time')
            ax2.set_title(f'Turnaround Time Comparison for Process {process.pid}')
            
            # Add value labels on top of each bar
            for bar in bars2:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height}',
                        ha='center', va='bottom')

            # Find and display best algorithm for this process
            best_waiting_algo = algorithms[waiting_times.index(min(waiting_times))]
            best_turnaround_algo = algorithms[turnaround_times.index(min(turnaround_times))]
            
            plt.figtext(0.02, 0.02, 
                       f'Best Waiting Time: {best_waiting_algo} ({min(waiting_times)})\n'
                       f'Best Turnaround Time: {best_turnaround_algo} ({min(turnaround_times)})',
                       fontsize=8)

            # Adjust layout and display
            plt.tight_layout()
            plt.show()

def main():
    scheduler = CPUScheduler()
    
    while True:
        print("\nCPU Scheduling Algorithms")
        print("1. Add Process")
        print("2. Get Process Metrics")
        print("3. Plot Comparison Graphs")
        print("4. Find Best Algorithm for a Process")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            pid = int(input("Enter Process ID: "))
            arrival_time = int(input("Enter Arrival Time: "))
            burst_time = int(input("Enter Burst Time: "))
            priority = int(input("Enter Priority (lower number = higher priority): "))
            
            scheduler.add_process(pid, arrival_time, burst_time, priority)
            print("Process added successfully!")
            
        elif choice == '2':
            pid = int(input("Enter Process ID to get metrics: "))
            metrics = scheduler.get_process_metrics(pid)
            
            print(f"\nMetrics for Process {pid}:")
            for algo, values in metrics.items():
                print(f"\n{algo}:")
                print(f"Waiting Time: {values['waiting_time']}")
                print(f"Turnaround Time: {values['turnaround_time']}")
                
        elif choice == '3':
            scheduler.plot_comparison_graphs()
            
        elif choice == '4':
            pid = int(input("Enter Process ID to find best algorithm: "))
            best_algos = scheduler.find_best_algorithm(pid)
            
            print(f"\nBest Algorithms for Process {pid}:")
            print(f"Best algorithm for Waiting Time: {best_algos['best_waiting_time'][0]} "
                  f"(Time: {best_algos['best_waiting_time'][1]})")
            print(f"Best algorithm for Turnaround Time: {best_algos['best_turnaround_time'][0]} "
                  f"(Time: {best_algos['best_turnaround_time'][1]})")
            
        elif choice == '5':
            print("Exiting program...")
            break
            
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()