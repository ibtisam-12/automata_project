"""
Clean Data Processor
A safe data processing utility for CSV-like data.
This file contains no malware signatures.
"""

import json
from typing import List, Dict, Any


class DataProcessor:
    """Process and analyze data safely."""
    
    def __init__(self):
        self.data = []
    
    def load_data(self, data: List[Dict[str, Any]]):
        """Load data into the processor."""
        self.data = data
        print(f"Loaded {len(data)} records")
    
    def filter_by_key(self, key: str, value: Any) -> List[Dict[str, Any]]:
        """Filter data by key-value pair."""
        filtered = [item for item in self.data if item.get(key) == value]
        return filtered
    
    def sort_by_key(self, key: str, reverse: bool = False) -> List[Dict[str, Any]]:
        """Sort data by a specific key."""
        sorted_data = sorted(self.data, key=lambda x: x.get(key, 0), reverse=reverse)
        return sorted_data
    
    def aggregate_sum(self, key: str) -> float:
        """Calculate sum of values for a specific key."""
        total = sum(item.get(key, 0) for item in self.data)
        return total
    
    def aggregate_average(self, key: str) -> float:
        """Calculate average of values for a specific key."""
        if not self.data:
            return 0.0
        total = self.aggregate_sum(key)
        return total / len(self.data)
    
    def count_by_category(self, category_key: str) -> Dict[str, int]:
        """Count occurrences by category."""
        counts = {}
        for item in self.data:
            category = item.get(category_key, "Unknown")
            counts[category] = counts.get(category, 0) + 1
        return counts
    
    def export_to_json(self, filename: str):
        """Export data to JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=2)
        print(f"Data exported to {filename}")


def demo():
    """Demonstrate data processor functionality."""
    # Sample data
    sample_data = [
        {"name": "Alice", "age": 30, "department": "Engineering", "salary": 75000},
        {"name": "Bob", "age": 25, "department": "Marketing", "salary": 60000},
        {"name": "Charlie", "age": 35, "department": "Engineering", "salary": 85000},
        {"name": "Diana", "age": 28, "department": "Sales", "salary": 65000},
        {"name": "Eve", "age": 32, "department": "Engineering", "salary": 80000},
    ]
    
    # Create processor and load data
    processor = DataProcessor()
    processor.load_data(sample_data)
    
    # Filter engineers
    engineers = processor.filter_by_key("department", "Engineering")
    print(f"\nEngineers: {len(engineers)}")
    for eng in engineers:
        print(f"  - {eng['name']}: ${eng['salary']}")
    
    # Calculate average salary
    avg_salary = processor.aggregate_average("salary")
    print(f"\nAverage Salary: ${avg_salary:,.2f}")
    
    # Count by department
    dept_counts = processor.count_by_category("department")
    print("\nDepartment Distribution:")
    for dept, count in dept_counts.items():
        print(f"  {dept}: {count}")
    
    # Sort by salary
    sorted_by_salary = processor.sort_by_key("salary", reverse=True)
    print("\nTop Earners:")
    for person in sorted_by_salary[:3]:
        print(f"  {person['name']}: ${person['salary']:,}")


if __name__ == "__main__":
    demo()
