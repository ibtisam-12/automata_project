#!/usr/bin/env python3
"""
Clean Script - Test File 5
This is a legitimate script with NO malware indicators
Should produce zero or minimal detections
"""

import math
import datetime
import json

def calculate_fibonacci(n):
    """Calculate the nth Fibonacci number"""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

def process_data(data_list):
    """Process a list of numbers"""
    total = sum(data_list)
    average = total / len(data_list)
    maximum = max(data_list)
    minimum = min(data_list)
    
    return {
        "total": total,
        "average": average,
        "max": maximum,
        "min": minimum
    }

def save_results(results, filename):
    """Save results to a JSON file"""
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)

def main():
    # Calculate some Fibonacci numbers
    print("Fibonacci sequence:")
    for i in range(10):
        print(f"F({i}) = {calculate_fibonacci(i)}")
    
    # Process some data
    numbers = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    stats = process_data(numbers)
    
    print("\nStatistics:")
    print(f"Total: {stats['total']}")
    print(f"Average: {stats['average']}")
    print(f"Max: {stats['max']}")
    print(f"Min: {stats['min']}")
    
    # Save results
    timestamp = datetime.datetime.now().isoformat()
    results = {
        "timestamp": timestamp,
        "statistics": stats,
        "fibonacci": [calculate_fibonacci(i) for i in range(10)]
    }
    
    save_results(results, "results.json")
    print("\nResults saved to results.json")

if __name__ == "__main__":
    main()
