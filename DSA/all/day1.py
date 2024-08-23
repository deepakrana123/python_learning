import math

class Solution:
    def gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a
    
    def fractionAddition(self, expression: str) -> str:
        # Initialize numerator and denominator
        numerator = 0
        denominator = 1
        
        # Parse the expression
        i = 0
        n = len(expression)
        
        while i < n:
            # Determine the sign of the fraction
            sign = 1
            if expression[i] == '-' or expression[i] == '+':
                if expression[i] == '-':
                    sign = -1
                i += 1
            
            # Parse the numerator
            start = i
            while i < n and expression[i].isdigit():
                i += 1
            curr_num = int(expression[start:i]) * sign
            
            # Skip the slash
            i += 1
            
            # Parse the denominator
            start = i
            while i < n and expression[i].isdigit():
                i += 1
            curr_denom = int(expression[start:i])
            numerator = numerator * curr_denom + curr_num * denominator
            denominator *= curr_denom
            gcd_value = self.gcd(abs(numerator), denominator)
            numerator //= gcd_value
            denominator //= gcd_value
        return f"{numerator}/{denominator}"
