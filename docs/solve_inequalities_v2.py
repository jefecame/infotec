import csv
import re
from fractions import Fraction

def tokenize_expression(expr):
    """Split expression into meaningful tokens while preserving operators."""
    # First split by spaces, then handle operators and numbers
    tokens = []
    parts = expr.split()
    
    for part in parts:
        # Check if this part contains an inequality operator
        for op in ['≤', '≥', '<', '>']:
            if op in part:
                # Split around the operator
                before, after = part.split(op, 1)
                if before:
                    tokens.append(before)
                tokens.append(op)
                if after:
                    tokens.append(after)
                break
        else:
            # No operator found, just add the token
            tokens.append(part)
    
    return [t for t in tokens if t]  # Remove empty tokens

def parse_simple_linear_expression(tokens, variable):
    """Parse a simple linear expression like ['- 81', 'A', '- 90']"""
    # Find the variable index
    var_idx = None
    for i, token in enumerate(tokens):
        if variable in token:
            var_idx = i
            break
    
    if var_idx is None:
        return None, None
    
    # Get coefficient (everything before the variable)
    coeff_tokens = tokens[:var_idx]
    # Get constant (everything after the variable)
    const_tokens = tokens[var_idx + 1:]
    
    # Parse coefficient
    if not coeff_tokens:
        coefficient = 1
    else:
        coeff_str = ''.join(coeff_tokens)
        coeff_str = coeff_str.replace(' ', '')
        if coeff_str == '+' or coeff_str == '':
            coefficient = 1
        elif coeff_str == '-':
            coefficient = -1
        else:
            coefficient = float(coeff_str)
    
    # Parse constant
    if not const_tokens:
        constant = 0
    else:
        const_str = ''.join(const_tokens)
        const_str = const_str.replace(' ', '')
        if const_str.startswith('+'):
            const_str = const_str[1:]
        constant = float(const_str)
    
    return coefficient, constant

def solve_inequality(expression):
    """Solve a mathematical inequality for its variable."""
    try:
        # Tokenize the expression
        tokens = tokenize_expression(expression)
        
        # Find the inequality operator
        operator = None
        op_idx = None
        for i, token in enumerate(tokens):
            if token in ['≤', '≥', '<', '>']:
                operator = token
                op_idx = i
                break
        
        if not operator:
            return "No inequality operator found"
        
        # Split into left and right sides
        left_tokens = tokens[:op_idx]
        right_tokens = tokens[op_idx + 1:]
        
        # Find the variable
        variables = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        variable = None
        for var in variables:
            for token in left_tokens:
                if var in token:
                    variable = var
                    break
            if variable:
                break
        
        if not variable:
            return "No variable found"
        
        # Handle different expression types
        if any('(' in token for token in left_tokens) and any('/' in token for token in left_tokens):
            return solve_fraction_expression(left_tokens, right_tokens, operator, variable)
        elif any('(' in token for token in left_tokens):
            return solve_parenthetical_expression(left_tokens, right_tokens, operator, variable)
        else:
            return solve_simple_expression(left_tokens, right_tokens, operator, variable)
            
    except Exception as e:
        return f"Error: {str(e)}"

def solve_simple_expression(left_tokens, right_tokens, operator, variable):
    """Solve simple linear expressions like '- 81 A - 90'."""
    # Parse left side
    coefficient, constant = parse_simple_linear_expression(left_tokens, variable)
    
    if coefficient is None:
        return "Failed to parse left side"
    
    # Parse right side
    right_str = ''.join(right_tokens).replace(' ', '')
    if right_str.startswith('+'):
        right_str = right_str[1:]
    right_value = float(right_str)
    
    # Solve: coefficient * variable + constant [operator] right_value
    # Rearrange to: coefficient * variable [operator] right_value - constant
    target = right_value - constant
    
    # Divide by coefficient
    if coefficient > 0:
        solution = target / coefficient
        final_operator = operator
    else:
        solution = target / coefficient
        # Flip inequality if coefficient is negative
        flip_map = {'≤': '≥', '≥': '≤', '<': '>', '>': '<'}
        final_operator = flip_map.get(operator, operator)
    
    return f"{variable} {final_operator} {solution:.2f}"

def solve_parenthetical_expression(left_tokens, right_tokens, operator, variable):
    """Solve expressions with parentheses like '94 ( - 95 G + 75 ) - 40'."""
    try:
        # Convert tokens back to string for easier parsing
        left_str = ' '.join(left_tokens)
        
        # Find parentheses content
        paren_start = left_str.find('(')
        paren_end = left_str.find(')')
        if paren_start == -1 or paren_end == -1:
            return "Invalid parenthetical format"
        
        # Extract parts
        outer_part = left_str[:paren_start].strip()
        inner_part = left_str[paren_start+1:paren_end].strip()
        after_part = left_str[paren_end+1:].strip()
        
        # Parse outer coefficient
        if outer_part == '' or outer_part == '+':
            outer_coeff = 1
        elif outer_part == '-':
            outer_coeff = -1
        else:
            outer_coeff_str = outer_part.replace(' ', '')
            if outer_coeff_str.startswith('+'):
                outer_coeff_str = outer_coeff_str[1:]
            outer_coeff = float(outer_coeff_str)
        
        # Parse inner expression
        inner_tokens = inner_part.split()
        inner_coeff, inner_const = parse_simple_linear_expression(inner_tokens, variable)
        
        if inner_coeff is None:
            return "Failed to parse inner expression"
        
        # Parse after part (additional constant)
        if after_part == '':
            after_const = 0
        else:
            after_const_str = after_part.replace(' ', '')
            if after_const_str.startswith('+'):
                after_const_str = after_const_str[1:]
            after_const = float(after_const_str)
        
        # Parse right side
        right_str = ''.join(right_tokens).replace(' ', '')
        if right_str.startswith('+'):
            right_str = right_str[1:]
        right_value = float(right_str)
        
        # The expression is: outer_coeff * (inner_coeff * variable + inner_const) + after_const
        # Expanding: outer_coeff * inner_coeff * variable + outer_coeff * inner_const + after_const
        final_var_coeff = outer_coeff * inner_coeff
        final_const = outer_coeff * inner_const + after_const
        
        # Solve: final_var_coeff * variable + final_const [operator] right_value
        target = right_value - final_const
        
        # Divide by final coefficient
        if final_var_coeff > 0:
            solution = target / final_var_coeff
            final_operator = operator
        else:
            solution = target / final_var_coeff
            # Flip inequality if coefficient is negative
            flip_map = {'≤': '≥', '≥': '≤', '<': '>', '>': '<'}
            final_operator = flip_map.get(operator, operator)
        
        return f"{variable} {final_operator} {solution:.2f}"
        
    except Exception as e:
        return f"Parenthetical error: {str(e)}"

def solve_fraction_expression(left_tokens, right_tokens, operator, variable):
    """Solve expressions with fractions like '( + 15 C ) / + 76 - 35'."""
    try:
        # Convert back to string for easier parsing
        left_str = ' '.join(left_tokens)
        
        # Find parentheses and division
        paren_start = left_str.find('(')
        paren_end = left_str.find(')')
        div_pos = left_str.find('/', paren_end)
        
        if paren_start == -1 or paren_end == -1 or div_pos == -1:
            return "Invalid fraction format"
        
        # Extract parts
        numerator_part = left_str[paren_start+1:paren_end].strip()
        after_div = left_str[div_pos+1:].strip()
        
        # Split the after_div part into divisor and remainder
        after_div_tokens = after_div.split()
        divisor_str = after_div_tokens[0]
        remainder_tokens = after_div_tokens[1:] if len(after_div_tokens) > 1 else []
        
        # Parse numerator
        num_tokens = numerator_part.split()
        num_coeff, num_const = parse_simple_linear_expression(num_tokens, variable)
        
        if num_coeff is None:
            return "Failed to parse numerator"
        
        # We assume the numerator constant is 0 for fraction expressions like ( + 15 C )
        num_const = 0
        
        # Parse divisor
        divisor_str = divisor_str.replace(' ', '')
        if divisor_str.startswith('+'):
            divisor_str = divisor_str[1:]
        divisor = float(divisor_str)
        
        # Parse remainder constant
        if remainder_tokens:
            remainder_str = ''.join(remainder_tokens).replace(' ', '')
            if remainder_str.startswith('+'):
                remainder_str = remainder_str[1:]
            remainder_const = float(remainder_str)
        else:
            remainder_const = 0
        
        # Parse right side
        right_str = ''.join(right_tokens).replace(' ', '')
        if right_str.startswith('+'):
            right_str = right_str[1:]
        right_value = float(right_str)
        
        # The expression is: (num_coeff * variable) / divisor + remainder_const
        # Solve: (num_coeff * variable) / divisor + remainder_const [operator] right_value
        # Rearrange: (num_coeff * variable) / divisor [operator] right_value - remainder_const
        target = right_value - remainder_const
        
        # Multiply by divisor
        if divisor > 0:
            target *= divisor
            final_operator = operator
        else:
            target *= divisor
            # Flip inequality if divisor is negative
            flip_map = {'≤': '≥', '≥': '≤', '<': '>', '>': '<'}
            final_operator = flip_map.get(operator, operator)
        
        # Divide by coefficient
        if num_coeff > 0:
            solution = target / num_coeff
        else:
            solution = target / num_coeff
            # Flip inequality if coefficient is negative
            flip_map = {'≤': '≥', '≥': '≤', '<': '>', '>': '<'}
            final_operator = flip_map.get(final_operator, final_operator)
        
        return f"{variable} {final_operator} {solution:.2f}"
        
    except Exception as e:
        return f"Fraction error: {str(e)}"

def main():
    # Test with a few examples first
    test_expressions = [
        "- 81 A - 90 ≤ - 60",
        "( + 15 C ) / + 76 - 35 > - 24",
        "+ 94 ( - 95 G + 75 ) - 40 ≥ - 79"
    ]
    
    print("Testing expressions:")
    for expr in test_expressions:
        result = solve_inequality(expr)
        print(f"{expr} => {result}")
    
    print("\nProcessing full CSV...")
    
    # Read the CSV file
    solutions = []
    
    with open('alumnos.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Process each row from 3 to 119 (student data)
    for i, line in enumerate(lines[2:], start=3):  # Skip header rows
        if i > 119:  # Only process up to row 119
            break
            
        # Parse the line
        content = line.strip().split('|', 1)[1] if '|' in line else line.strip()
        row_data = content.split(',')
        
        # Extract first 5 columns (student info)
        student_info = row_data[:5]
        
        # Extract and solve inequalities from columns 6-15 (F1-F10)
        inequality_solutions = []
        for j in range(5, 15):  # Columns 6-15 (indices 5-14)
            if j < len(row_data):
                inequality = row_data[j].strip()
                solution = solve_inequality(inequality)
                inequality_solutions.append(solution)
            else:
                inequality_solutions.append("No data")
        
        # Combine student info with solutions
        full_row = student_info + inequality_solutions
        solutions.append(full_row)
        
        # Print first few for verification
        if i <= 7:
            print(f"Row {i}: {student_info[2]} {student_info[3]}")
            for k, sol in enumerate(inequality_solutions[:3]):  # Show first 3 solutions
                print(f"  F{k+1}: {sol}")
    
    # Create the new CSV file
    with open('alumnos_solutions_v2.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write headers
        headers = ['CLAVE', 'EXP', 'NOMBRE', 'APELLIDOS', 'CORREO', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10']
        writer.writerow(headers)
        
        # Write empty template row
        empty_row = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        writer.writerow(empty_row)
        
        # Write solutions
        for solution_row in solutions:
            writer.writerow(solution_row)
    
    print(f"\nCreated alumnos_solutions_v2.csv with {len(solutions)} student records")

if __name__ == "__main__":
    main()