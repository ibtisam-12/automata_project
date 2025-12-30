"""
Clean Calculator Application
A simple calculator with basic arithmetic operations.
This file contains no malware signatures.
"""

class Calculator:
    """A basic calculator class for arithmetic operations."""
    
    def __init__(self):
        self.result = 0
        self.history = []
    
    def add(self, a, b):
        """Add two numbers."""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a, b):
        """Subtract b from a."""
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a, b):
        """Multiply two numbers."""
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result
    
    def divide(self, a, b):
        """Divide a by b."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result
    
    def power(self, base, exponent):
        """Raise base to the power of exponent."""
        result = base ** exponent
        self.history.append(f"{base} ^ {exponent} = {result}")
        return result
    
    def get_history(self):
        """Return calculation history."""
        return self.history
    
    def clear_history(self):
        """Clear calculation history."""
        self.history = []


def main():
    """Main function to demonstrate calculator usage."""
    calc = Calculator()
    
    # Perform some calculations
    print("Calculator Demo")
    print("-" * 40)
    
    result1 = calc.add(10, 5)
    print(f"10 + 5 = {result1}")
    
    result2 = calc.multiply(7, 8)
    print(f"7 * 8 = {result2}")
    
    result3 = calc.divide(100, 4)
    print(f"100 / 4 = {result3}")
    
    result4 = calc.power(2, 10)
    print(f"2 ^ 10 = {result4}")
    
    # Display history
    print("\nCalculation History:")
    for entry in calc.get_history():
        print(f"  {entry}")


if __name__ == "__main__":
    main()
