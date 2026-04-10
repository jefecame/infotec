import csv
import re
from fractions import Fraction

def parse_inequality(expression):
    """Parse a mathematical inequality expression and solve for the variable."""
    try:
        # Clean the expression - remove extra spaces
        expr = expression.strip()
        
        # Extract the inequality operator
        inequality_ops = ['≤', '≥', '<', '>']
        operator = None
        for op in inequality_ops:
            if op in expr:
                operator = op
                break
        
        if not operator:
            return "No valid inequality operator found"
        
        # Split by the operator
        left_side, right_side = expr.split(operator, 1)
        left_side = left_side.strip()
        right_side = right_side.strip()
        
        # Extract variable from the expression (A, B, C, D, E, F, G, H, I, J)
        variables = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        variable = None
        for var in variables:
            if var in expr:
                variable = var
                break
        
        if not variable:
            return "No variable found"
        
        # Solve different types of inequalities
        solution = solve_inequality_for_variable(left_side, right_side, operator, variable)
        return solution
        
    except Exception as e:
        return f"Error: {str(e)}"

def solve_inequality_for_variable(left_side, right_side, operator, variable):
    """Solve the inequality for the specified variable."""
    try:
        # Convert right side to number
        right_value = parse_number(right_side)
        
        # Handle different types of left side expressions
        if '(' in left_side and ')' in left_side and '/' in left_side:
            # Handle expressions like: ( + 15 C ) / + 76 - 35
            return solve_fraction_inequality(left_side, right_value, operator, variable)
        elif '(' in left_side and ')' in left_side:
            # Handle expressions like: + 94 ( - 95 G + 75 ) - 40
            return solve_parenthetical_inequality(left_side, right_value, operator, variable)
        else:
            # Handle simple expressions like: - 55 A - 8
            return solve_simple_inequality(left_side, right_value, operator, variable)
            
    except Exception as e:
        return f"Solve error: {str(e)}"

def parse_number(num_str):
    """Parse a number string that might have + or - prefix."""
    num_str = num_str.strip()
    # Remove extra spaces within the number
    num_str = re.sub(r'\s+', '', num_str)
    if num_str.startswith('+'):
        num_str = num_str[1:]
    return float(num_str)

def solve_simple_inequality(left_side, right_value, operator, variable):
    """Solve simple inequalities like: -55 A - 8 ≤ +38"""
    try:
        # Parse the left side to extract coefficient and constant
        # Pattern: [coefficient] [variable] [±constant]
        
        # Remove the variable to split around it
        parts = left_side.split(variable)
        if len(parts) != 2:
            return "Invalid simple expression format"
        
        coeff_str = parts[0].strip()
        constant_str = parts[1].strip()
        
        # Parse coefficient
        if coeff_str == '+' or coeff_str == '':
            coefficient = 1
        elif coeff_str == '-':
            coefficient = -1
        else:
            coefficient = parse_number(coeff_str)
        
        # Parse constant
        if constant_str == '':
            constant = 0
        else:
            constant = parse_number(constant_str)
        
        # Solve: coefficient * variable + constant [operator] right_value
        # Rearrange to: coefficient * variable [operator] right_value - constant
        target = right_value - constant
        
        # Divide by coefficient (flip inequality if negative)
        if coefficient > 0:
            solution = target / coefficient
            final_operator = operator
        else:
            solution = target / coefficient
            # Flip the inequality operator
            flip_map = {'≤': '≥', '≥': '≤', '<': '>', '>': '<'}
            final_operator = flip_map.get(operator, operator)
        
        return f"{variable} {final_operator} {solution:.2f}"
        
    except Exception as e:
        return f"Simple solve error: {str(e)}"

def solve_fraction_inequality(left_side, right_value, operator, variable):
    """Solve fraction inequalities like: ( + 15 C ) / + 76 - 35 > - 24"""
    try:
        # Pattern: ( [expression] ) / [divisor] [±constant]
        
        # Find the parentheses content
        paren_start = left_side.find('(')
        paren_end = left_side.find(')')
        if paren_start == -1 or paren_end == -1:
            return "Invalid fraction format - no parentheses"
        
        numerator = left_side[paren_start+1:paren_end].strip()
        remainder = left_side[paren_end+1:].strip()
        
        # Parse the remainder: / [divisor] [±constant]
        if not remainder.startswith('/'):
            return "Invalid fraction format - no division"
        
        remainder = remainder[1:].strip()  # Remove the '/'
        
        # Split remainder into divisor and constant
        # Find where the divisor ends and constant begins
        parts = remainder.split()
        divisor_str = parts[0]
        
        if len(parts) > 1:
            constant_str = ' '.join(parts[1:])
            constant = parse_number(constant_str)
        else:
            constant = 0
        
        divisor = parse_number(divisor_str)
        
        # Parse numerator to get variable coefficient
        # numerator should be like: "+ 15 C" or "- 15 C"
        num_parts = numerator.split(variable)
        if len(num_parts) != 2:
            return "Invalid numerator format"
        
        coeff_str = num_parts[0].strip()
        if coeff_str == '+' or coeff_str == '':
            num_coefficient = 1
        elif coeff_str == '-':
            num_coefficient = -1
        else:
            num_coefficient = parse_number(coeff_str)
        
        # Solve: (num_coefficient * variable) / divisor + constant [operator] right_value
        # Rearrange: (num_coefficient * variable) / divisor [operator] right_value - constant
        target = right_value - constant
        
        # Multiply both sides by divisor
        if divisor > 0:
            target *= divisor
            final_operator = operator
        else:
            target *= divisor
            # Flip inequality if divisor is negative
            flip_map = {'≤': '≥', '≥': '≤', '<': '>', '>': '<'}
            final_operator = flip_map.get(operator, operator)
        
        # Divide by coefficient
        if num_coefficient > 0:
            solution = target / num_coefficient
        else:
            solution = target / num_coefficient
            # Flip inequality if coefficient is negative
            flip_map = {'≤': '≥', '≥': '≤', '<': '>', '>': '<'}
            final_operator = flip_map.get(final_operator, final_operator)
        
        return f"{variable} {final_operator} {solution:.2f}"
        
    except Exception as e:
        return f"Fraction solve error: {str(e)}"

def solve_parenthetical_inequality(left_side, right_value, operator, variable):
    """Solve parenthetical inequalities like: + 94 ( - 95 G + 75 ) - 40 ≥ - 79"""
    try:
        # Pattern: [outer_coeff] ( [inner_expression] ) [±constant]
        
        # Find the parentheses
        paren_start = left_side.find('(')
        paren_end = left_side.find(')')
        if paren_start == -1 or paren_end == -1:
            return "Invalid parenthetical format"
        
        outer_coeff_str = left_side[:paren_start].strip()
        inner_expr = left_side[paren_start+1:paren_end].strip()
        constant_str = left_side[paren_end+1:].strip()
        
        # Parse outer coefficient
        if outer_coeff_str == '+' or outer_coeff_str == '':
            outer_coeff = 1
        elif outer_coeff_str == '-':
            outer_coeff = -1
        else:
            outer_coeff = parse_number(outer_coeff_str)
        
        # Parse constant
        if constant_str == '':
            constant = 0
        else:
            constant = parse_number(constant_str)
        
        # Parse inner expression: should be like "- 95 G + 75"
        inner_parts = inner_expr.split(variable)
        if len(inner_parts) != 2:
            return "Invalid inner expression format"
        
        inner_coeff_str = inner_parts[0].strip()
        inner_constant_str = inner_parts[1].strip()
        
        # Parse inner coefficient
        if inner_coeff_str == '+' or inner_coeff_str == '':
            inner_coeff = 1
        elif inner_coeff_str == '-':
            inner_coeff = -1
        else:
            inner_coeff = parse_number(inner_coeff_str)
        
        # Parse inner constant
        if inner_constant_str == '':
            inner_constant = 0
        else:
            inner_constant = parse_number(inner_constant_str)
        
        # The expression is: outer_coeff * (inner_coeff * variable + inner_constant) + constant [operator] right_value
        # Expanding: outer_coeff * inner_coeff * variable + outer_coeff * inner_constant + constant [operator] right_value
        
        final_var_coeff = outer_coeff * inner_coeff
        final_constant = outer_coeff * inner_constant + constant
        
        # Solve: final_var_coeff * variable + final_constant [operator] right_value
        target = right_value - final_constant
        
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
        return f"Parenthetical solve error: {str(e)}"

def main():
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
                solution = parse_inequality(inequality)
                inequality_solutions.append(solution)
            else:
                inequality_solutions.append("No data")
        
        # Combine student info with solutions
        full_row = student_info + inequality_solutions
        solutions.append(full_row)
        
        print(f"Row {i}: {student_info[2]} {student_info[3]} - {len(inequality_solutions)} solutions")
    
    # Create the new CSV file
    with open('alumnos_solutions.csv', 'w', newline='', encoding='utf-8') as file:
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
    
    print(f"Created alumnos_solutions.csv with {len(solutions)} student records")

if __name__ == "__main__":
    main()