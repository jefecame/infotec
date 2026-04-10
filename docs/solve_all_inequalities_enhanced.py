import csv
import re
from fractions import Fraction

def parse_number(num_str):
    """Parse a number string that might have + or - prefix."""
    if not num_str:
        return 0
    num_str = num_str.strip()
    if num_str.startswith('+'):
        num_str = num_str[1:]
    if num_str == '' or num_str == '+' or num_str == '-':
        return 1 if num_str != '-' else -1
    return float(num_str)

def solve_j_complex_inequality(expression):
    """Specialized solver for J variable complex inequalities."""
    try:
        # Pattern: outer_coeff(inner_coeff*J + inner_const) / divisor [operator] right_coeff*J + right_const
        
        # Find the inequality operator
        operators = ['≤', '≥', '<', '>']
        operator = None
        for op in operators:
            if op in expression:
                operator = op
                left_side, right_side = expression.split(op, 1)
                break
        
        if not operator:
            return f"No operator found in J expression: {expression}"
        
        left_side = left_side.strip()
        right_side = right_side.strip()
        
        # Parse left side: outer_coeff(inner_expression)/divisor
        paren_start = left_side.find('(')
        paren_end = left_side.find(')')
        
        if paren_start == -1 or paren_end == -1:
            return f"No parentheses found in left side: {left_side}"
        
        # Extract components
        outer_coeff_str = left_side[:paren_start]
        inner_expr = left_side[paren_start+1:paren_end]
        after_paren = left_side[paren_end+1:]
        
        # Parse outer coefficient
        outer_coeff = parse_number(outer_coeff_str) if outer_coeff_str else 1
        
        # Parse divisor (after parentheses should be /divisor)
        if not after_paren.startswith('/'):
            return f"No division found after parentheses: {after_paren}"
        
        divisor_str = after_paren[1:]  # Remove '/'
        divisor = parse_number(divisor_str)
        
        # Parse inner expression: inner_coeff*J + inner_const
        inner_parts = inner_expr.split('J')
        if len(inner_parts) != 2:
            return f"J not found in inner expression: {inner_expr}"
        
        inner_coeff = parse_number(inner_parts[0]) if inner_parts[0] else 1
        inner_const = parse_number(inner_parts[1]) if inner_parts[1] else 0
        
        # Parse right side: right_coeff*J + right_const
        right_parts = right_side.split('J')
        if len(right_parts) != 2:
            return f"J not found in right side: {right_side}"
        
        right_coeff = parse_number(right_parts[0]) if right_parts[0] else 1
        right_const = parse_number(right_parts[1]) if right_parts[1] else 0
        
        # Now we have:
        # Left side: (outer_coeff * (inner_coeff * J + inner_const)) / divisor
        # Right side: right_coeff * J + right_const
        
        # Expand left side: (outer_coeff * inner_coeff * J + outer_coeff * inner_const) / divisor
        left_j_coeff = (outer_coeff * inner_coeff) / divisor
        left_const = (outer_coeff * inner_const) / divisor
        
        # The inequality becomes:
        # left_j_coeff * J + left_const [operator] right_coeff * J + right_const
        
        # Move all J terms to left side, constants to right side:
        # (left_j_coeff - right_coeff) * J [operator] right_const - left_const
        
        final_j_coeff = left_j_coeff - right_coeff
        final_const = right_const - left_const
        
        if abs(final_j_coeff) < 1e-10:  # Essentially zero
            if abs(final_const) < 1e-10:
                return "J: All values (identity)"
            else:
                return "J: No solution (contradiction)"
        
        solution = final_const / final_j_coeff
        
        # Handle inequality direction
        if final_j_coeff < 0:
            # Flip inequality when dividing by negative
            flip_map = {'≤': '≥', '≥': '≤', '<': '>', '>': '<'}
            final_operator = flip_map.get(operator, operator)
        else:
            final_operator = operator
        
        return f"J {final_operator} {solution:.2f}"
        
    except Exception as e:
        return f"J complex error: {str(e)}"

def solve_simple_inequality(expression, variable):
    """Solve simple inequalities like '-81A-90 ≤ -60' or '+46B+42 > -44B-32'."""
    try:
        # Find the inequality operator
        operators = ['≤', '≥', '<', '>']
        operator = None
        for op in operators:
            if op in expression:
                operator = op
                left_side, right_side = expression.split(op, 1)
                break
        
        if not operator:
            return f"No operator found in: {expression}"
        
        left_side = left_side.strip()
        right_side = right_side.strip()
        
        # Check if variable appears on both sides (like B expressions)
        if variable in left_side and variable in right_side:
            return solve_variable_both_sides(left_side, right_side, operator, variable)
        elif variable in left_side:
            return solve_variable_left_side(left_side, right_side, operator, variable)
        else:
            return f"Variable {variable} not found in expression"
            
    except Exception as e:
        return f"Error in simple: {str(e)}"

def solve_variable_left_side(left_side, right_side, operator, variable):
    """Solve when variable is only on left side."""
    # Parse left side: coefficient*variable + constant
    # Split around the variable
    if variable not in left_side:
        return "Variable not found"
    
    parts = left_side.split(variable)
    if len(parts) != 2:
        return f"Invalid format: {left_side}"
    
    coeff_part = parts[0]
    const_part = parts[1]
    
    # Parse coefficient
    if coeff_part == '' or coeff_part == '+':
        coefficient = 1
    elif coeff_part == '-':
        coefficient = -1
    else:
        coefficient = parse_number(coeff_part)
    
    # Parse constant
    constant = parse_number(const_part) if const_part else 0
    
    # Parse right side
    right_value = parse_number(right_side)
    
    # Solve: coefficient * variable + constant [operator] right_value
    # Rearrange: coefficient * variable [operator] right_value - constant
    target = right_value - constant
    
    # Divide by coefficient (flip inequality if negative)
    if coefficient == 0:
        return "Division by zero"
    
    solution = target / coefficient
    
    if coefficient < 0:
        # Flip inequality
        flip_map = {'≤': '≥', '≥': '≤', '<': '>', '>': '<'}
        final_operator = flip_map.get(operator, operator)
    else:
        final_operator = operator
    
    return f"{variable} {final_operator} {solution:.2f}"

def solve_variable_both_sides(left_side, right_side, operator, variable):
    """Solve when variable appears on both sides like '+46B+42 > -44B-32'."""
    # Parse left side
    left_parts = left_side.split(variable)
    if len(left_parts) != 2:
        return f"Invalid left format: {left_side}"
    
    left_coeff = parse_number(left_parts[0]) if left_parts[0] else 1
    left_const = parse_number(left_parts[1]) if left_parts[1] else 0
    
    # Parse right side
    right_parts = right_side.split(variable)
    if len(right_parts) != 2:
        return f"Invalid right format: {right_side}"
    
    right_coeff = parse_number(right_parts[0]) if right_parts[0] else 1
    right_const = parse_number(right_parts[1]) if right_parts[1] else 0
    
    # Move all variable terms to left, constants to right
    # left_coeff * variable + left_const [operator] right_coeff * variable + right_const
    # (left_coeff - right_coeff) * variable [operator] right_const - left_const
    
    final_coeff = left_coeff - right_coeff
    final_const = right_const - left_const
    
    if final_coeff == 0:
        return "No variable solution (coefficients cancel)"
    
    solution = final_const / final_coeff
    
    if final_coeff < 0:
        # Flip inequality
        flip_map = {'≤': '≥', '≥': '≤', '<': '>', '>': '<'}
        final_operator = flip_map.get(operator, operator)
    else:
        final_operator = operator
    
    return f"{variable} {final_operator} {solution:.2f}"

def solve_fraction_inequality(expression, variable):
    """Solve fraction inequalities like '(-54C)/+83-22 ≥ -51'."""
    try:
        # Find the inequality operator
        operators = ['≤', '≥', '<', '>']
        operator = None
        for op in operators:
            if op in expression:
                operator = op
                left_side, right_side = expression.split(op, 1)
                break
        
        if not operator:
            return f"No operator found"
        
        left_side = left_side.strip()
        right_side = right_side.strip()
        
        # Find the main division
        # Look for pattern: (numerator)/divisor+remainder
        paren_start = left_side.find('(')
        paren_end = left_side.find(')')
        
        if paren_start == -1 or paren_end == -1:
            return f"No parentheses found in fraction"
        
        numerator = left_side[paren_start+1:paren_end]
        after_paren = left_side[paren_end+1:]
        
        # Parse the part after parentheses: /divisor+remainder
        if not after_paren.startswith('/'):
            return f"No division found after parentheses"
        
        after_div = after_paren[1:]  # Remove the '/'
        
        # Find where divisor ends and remainder begins
        # Look for + or - that's not at the beginning
        divisor = ""
        remainder = ""
        
        i = 0
        if after_div[0] in '+-':
            i = 1
        
        while i < len(after_div) and after_div[i] not in '+-':
            i += 1
        
        divisor = after_div[:i]
        remainder = after_div[i:] if i < len(after_div) else ""
        
        # Parse numerator (should contain the variable)
        num_parts = numerator.split(variable)
        if len(num_parts) != 2:
            return f"Variable not found in numerator: {numerator}"
        
        num_coeff = parse_number(num_parts[0]) if num_parts[0] else 1
        num_const = parse_number(num_parts[1]) if num_parts[1] else 0
        
        # Parse divisor and remainder
        divisor_val = parse_number(divisor)
        remainder_val = parse_number(remainder) if remainder else 0
        right_val = parse_number(right_side)
        
        # Solve: (num_coeff * variable + num_const) / divisor_val + remainder_val [operator] right_val
        # Rearrange: (num_coeff * variable + num_const) / divisor_val [operator] right_val - remainder_val
        target = right_val - remainder_val
        
        # Multiply both sides by divisor_val
        if divisor_val == 0:
            return "Division by zero"
        
        target *= divisor_val
        
        if divisor_val < 0:
            # Flip inequality when multiplying by negative
            flip_map = {'≤': '≥', '≥': '≤', '<': '>', '>': '<'}
            operator = flip_map.get(operator, operator)
        
        # Now solve: num_coeff * variable + num_const [operator] target
        final_target = target - num_const
        
        if num_coeff == 0:
            return "No variable coefficient"
        
        solution = final_target / num_coeff
        
        if num_coeff < 0:
            # Flip inequality when dividing by negative
            flip_map = {'≤': '≥', '≥': '≤', '<': '>', '>': '<'}
            operator = flip_map.get(operator, operator)
        
        return f"{variable} {operator} {solution:.2f}"
        
    except Exception as e:
        return f"Fraction error: {str(e)}"

def solve_parenthetical_inequality(expression, variable):
    """Solve parenthetical inequalities like '+5(+23F-59) < -50'."""
    try:
        # Find the inequality operator
        operators = ['≤', '≥', '<', '>']
        operator = None
        for op in operators:
            if op in expression:
                operator = op
                left_side, right_side = expression.split(op, 1)
                break
        
        if not operator:
            return f"No operator found"
        
        left_side = left_side.strip()
        right_side = right_side.strip()
        
        # Find parentheses
        paren_start = left_side.find('(')
        paren_end = left_side.find(')')
        
        if paren_start == -1 or paren_end == -1:
            return f"No parentheses found"
        
        # Extract parts
        outer_coeff = left_side[:paren_start]
        inner_expr = left_side[paren_start+1:paren_end]
        after_paren = left_side[paren_end+1:]
        
        # Check for division after parentheses
        has_division = after_paren.startswith('/')
        
        if has_division:
            # Handle expressions like '+39(+6H+7)/+7 < -82'
            div_part = after_paren[1:]  # Remove '/'
            
            # Find where divisor ends and remainder begins
            i = 0
            if div_part[0] in '+-':
                i = 1
            while i < len(div_part) and div_part[i] not in '+-':
                i += 1
            
            divisor = div_part[:i]
            remainder = div_part[i:] if i < len(div_part) else ""
            
            divisor_val = parse_number(divisor)
            remainder_val = parse_number(remainder) if remainder else 0
        else:
            divisor_val = 1
            remainder_val = parse_number(after_paren) if after_paren else 0
        
        # Parse outer coefficient
        outer_coeff_val = parse_number(outer_coeff) if outer_coeff else 1
        
        # Parse inner expression
        inner_parts = inner_expr.split(variable)
        if len(inner_parts) != 2:
            return f"Variable not found in inner expression: {inner_expr}"
        
        inner_coeff = parse_number(inner_parts[0]) if inner_parts[0] else 1
        inner_const = parse_number(inner_parts[1]) if inner_parts[1] else 0
        
        right_val = parse_number(right_side)
        
        # The expression is: outer_coeff_val * (inner_coeff * variable + inner_const) / divisor_val + remainder_val [operator] right_val
        # Simplify: (outer_coeff_val * inner_coeff * variable + outer_coeff_val * inner_const) / divisor_val + remainder_val [operator] right_val
        
        final_var_coeff = outer_coeff_val * inner_coeff
        final_const_num = outer_coeff_val * inner_const
        
        # Rearrange: (final_var_coeff * variable + final_const_num) / divisor_val [operator] right_val - remainder_val
        target = right_val - remainder_val
        
        # Multiply by divisor
        if divisor_val == 0:
            return "Division by zero"
        
        target *= divisor_val
        
        if divisor_val < 0:
            flip_map = {'≤': '≥', '≥': '≤', '<': '>', '>': '<'}
            operator = flip_map.get(operator, operator)
        
        # Now solve: final_var_coeff * variable + final_const_num [operator] target
        final_target = target - final_const_num
        
        if final_var_coeff == 0:
            return "No variable coefficient"
        
        solution = final_target / final_var_coeff
        
        if final_var_coeff < 0:
            flip_map = {'≤': '≥', '≥': '≤', '<': '>', '>': '<'}
            operator = flip_map.get(operator, operator)
        
        return f"{variable} {operator} {solution:.2f}"
        
    except Exception as e:
        return f"Parenthetical error: {str(e)}"

def solve_inequality(expression, variable):
    """Main function to solve any type of inequality for a given variable."""
    if not expression or not expression.strip():
        return "Empty expression"
    
    expression = expression.strip()
    
    # Special handling for J variable complex expressions
    if variable == 'J' and '(' in expression and ')' in expression and '/' in expression and 'J' in expression:
        # Check if J appears on both sides
        operators = ['≤', '≥', '<', '>']
        for op in operators:
            if op in expression:
                left, right = expression.split(op, 1)
                if 'J' in left and 'J' in right:
                    return solve_j_complex_inequality(expression)
                break
    
    # Determine the type of expression and solve accordingly
    if '(' in expression and ')' in expression:
        if '/' in expression:
            # Could be fraction or parenthetical with division
            if expression.startswith('(') and '/' in expression[expression.find(')')+1:]:
                return solve_fraction_inequality(expression, variable)
            else:
                return solve_parenthetical_inequality(expression, variable)
        else:
            return solve_parenthetical_inequality(expression, variable)
    elif variable in expression:
        # Check if it's a simple case with variable on both sides
        operators = ['≤', '≥', '<', '>']
        for op in operators:
            if op in expression:
                left, right = expression.split(op, 1)
                if variable in left and variable in right:
                    return solve_simple_inequality(expression, variable)
                else:
                    return solve_simple_inequality(expression, variable)
        return f"No operator found in: {expression}"
    else:
        return f"Variable {variable} not found in: {expression}"

def main():
    # Test with J examples first
    test_cases = [
        ("-81A-90 ≤ -60", "A"),
        ("+46B+42 > -44B-32", "B"),
        ("(-54C)/+83-22 ≥ -51", "C"),
        ("+5(+23F-59) < -50", "F"),
        ("+39(+6H+7)/+7 < -82", "H"),
        ("-13(-58J-29)/-43 ≤ -48J-76", "J"),
        ("+19(+71J-6)/-24 > -16J-86", "J"),
        ("+22(+29J-16)/+31 > -25J-35", "J")
    ]
    
    print("Testing enhanced inequality solver with J support:")
    for expr, var in test_cases:
        result = solve_inequality(expr, var)
        print(f"{expr} => {result}")
    print()
    
    # Process the cleaned CSV file
    solutions = []
    
    with open('alumnos_cleaned.csv', 'r', encoding='utf-8') as file:
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
        
        # Variables for columns F1-F10
        variables = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        
        # Extract and solve inequalities from columns 6-15 (F1-F10)
        inequality_solutions = []
        for j in range(5, 15):  # Columns 6-15 (indices 5-14)
            if j < len(row_data) and j-5 < len(variables):
                inequality = row_data[j].strip()
                variable = variables[j-5]
                solution = solve_inequality(inequality, variable)
                inequality_solutions.append(solution)
            else:
                inequality_solutions.append("No data")
        
        # Combine student info with solutions
        full_row = student_info + inequality_solutions
        solutions.append(full_row)
        
        # Print first few for verification
        if i <= 5:
            name = student_info[2] if len(student_info) > 2 else "N/A"
            lastname = student_info[3] if len(student_info) > 3 else "N/A"
            print(f"Row {i}: {name} {lastname}")
            for k, (var, sol) in enumerate(zip(variables, inequality_solutions[:len(variables)])):
                print(f"  {var}: {sol}")
            print()
    
    # Create the new CSV file
    with open('alumnos_complete_solutions.csv', 'w', newline='', encoding='utf-8') as file:
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
    
    print(f"\nCreated alumnos_complete_solutions.csv with {len(solutions)} student records")

if __name__ == "__main__":
    main()