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

def format_fraction(value):
    """Convert a decimal value to simplified fraction format."""
    try:
        # Convert to Fraction for exact representation
        frac = Fraction(value).limit_denominator(10000)  # Limit denominator for reasonable fractions
        
        if frac.denominator == 1:
            # Integer case
            return str(frac.numerator)
        else:
            # Fraction case
            if frac.numerator < 0:
                return f"-{abs(frac.numerator)}/{frac.denominator}"
            else:
                return f"{frac.numerator}/{frac.denominator}"
    except:
        # Fallback to decimal if fraction conversion fails
        return f"{value:.2f}"

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
        
        # Use Fraction for exact arithmetic
        outer_coeff_frac = Fraction(outer_coeff).limit_denominator(10000)
        inner_coeff_frac = Fraction(inner_coeff).limit_denominator(10000)
        inner_const_frac = Fraction(inner_const).limit_denominator(10000)
        divisor_frac = Fraction(divisor).limit_denominator(10000)
        right_coeff_frac = Fraction(right_coeff).limit_denominator(10000)
        right_const_frac = Fraction(right_const).limit_denominator(10000)
        
        # Expand left side: (outer_coeff * inner_coeff * J + outer_coeff * inner_const) / divisor
        left_j_coeff = (outer_coeff_frac * inner_coeff_frac) / divisor_frac
        left_const = (outer_coeff_frac * inner_const_frac) / divisor_frac
        
        # The inequality becomes:
        # left_j_coeff * J + left_const [operator] right_coeff * J + right_const
        
        # Move all J terms to left side, constants to right side:
        # (left_j_coeff - right_coeff) * J [operator] right_const - left_const
        
        final_j_coeff = left_j_coeff - right_coeff_frac
        final_const = right_const_frac - left_const
        
        if abs(final_j_coeff) < Fraction(1, 10000):  # Essentially zero
            if abs(final_const) < Fraction(1, 10000):
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
        
        solution_str = format_fraction(float(solution))
        return f"J {final_operator} {solution_str}"
        
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
    
    # Use fractions for exact arithmetic
    coeff_frac = Fraction(coefficient).limit_denominator(10000)
    const_frac = Fraction(constant).limit_denominator(10000)
    right_frac = Fraction(right_value).limit_denominator(10000)
    
    # Solve: coefficient * variable + constant [operator] right_value
    # Rearrange: coefficient * variable [operator] right_value - constant
    target = right_frac - const_frac
    
    # Divide by coefficient (flip inequality if negative)
    if coeff_frac == 0:
        return "Division by zero"
    
    solution = target / coeff_frac
    
    if coeff_frac < 0:
        # Flip inequality
        flip_map = {'≤': '≥', '≥': '≤', '<': '>', '>': '<'}
        final_operator = flip_map.get(operator, operator)
    else:
        final_operator = operator
    
    solution_str = format_fraction(float(solution))
    return f"{variable} {final_operator} {solution_str}"

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
    
    # Use fractions for exact arithmetic
    left_coeff_frac = Fraction(left_coeff).limit_denominator(10000)
    left_const_frac = Fraction(left_const).limit_denominator(10000)
    right_coeff_frac = Fraction(right_coeff).limit_denominator(10000)
    right_const_frac = Fraction(right_const).limit_denominator(10000)
    
    # Move all variable terms to left, constants to right
    # left_coeff * variable + left_const [operator] right_coeff * variable + right_const
    # (left_coeff - right_coeff) * variable [operator] right_const - left_const
    
    final_coeff = left_coeff_frac - right_coeff_frac
    final_const = right_const_frac - left_const_frac
    
    if final_coeff == 0:
        return "No variable solution (coefficients cancel)"
    
    solution = final_const / final_coeff
    
    if final_coeff < 0:
        # Flip inequality
        flip_map = {'≤': '≥', '≥': '≤', '<': '>', '>': '<'}
        final_operator = flip_map.get(operator, operator)
    else:
        final_operator = operator
    
    solution_str = format_fraction(float(solution))
    return f"{variable} {final_operator} {solution_str}"

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
        
        # Use fractions for exact arithmetic
        num_coeff_frac = Fraction(num_coeff).limit_denominator(10000)
        num_const_frac = Fraction(num_const).limit_denominator(10000)
        divisor_frac = Fraction(divisor_val).limit_denominator(10000)
        remainder_frac = Fraction(remainder_val).limit_denominator(10000)
        right_frac = Fraction(right_val).limit_denominator(10000)
        
        # Solve: (num_coeff * variable + num_const) / divisor_val + remainder_val [operator] right_val
        # Rearrange: (num_coeff * variable + num_const) / divisor_val [operator] right_val - remainder_val
        target = right_frac - remainder_frac
        
        # Multiply both sides by divisor_val
        if divisor_frac == 0:
            return "Division by zero"
        
        target *= divisor_frac
        
        if divisor_frac < 0:
            # Flip inequality when multiplying by negative
            flip_map = {'≤': '≥', '≥': '≤', '<': '>', '>': '<'}
            operator = flip_map.get(operator, operator)
        
        # Now solve: num_coeff * variable + num_const [operator] target
        final_target = target - num_const_frac
        
        if num_coeff_frac == 0:
            return "No variable coefficient"
        
        solution = final_target / num_coeff_frac
        
        if num_coeff_frac < 0:
            # Flip inequality when dividing by negative
            flip_map = {'≤': '≥', '≥': '≤', '<': '>', '>': '<'}
            operator = flip_map.get(operator, operator)
        
        solution_str = format_fraction(float(solution))
        return f"{variable} {operator} {solution_str}"
        
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
        
        # Use fractions for exact arithmetic
        outer_coeff_frac = Fraction(outer_coeff_val).limit_denominator(10000)
        inner_coeff_frac = Fraction(inner_coeff).limit_denominator(10000)
        inner_const_frac = Fraction(inner_const).limit_denominator(10000)
        divisor_frac = Fraction(divisor_val).limit_denominator(10000)
        remainder_frac = Fraction(remainder_val).limit_denominator(10000)
        right_frac = Fraction(right_val).limit_denominator(10000)
        
        # The expression is: outer_coeff_val * (inner_coeff * variable + inner_const) / divisor_val + remainder_val [operator] right_val
        # Simplify: (outer_coeff_val * inner_coeff * variable + outer_coeff_val * inner_const) / divisor_val + remainder_val [operator] right_val
        
        final_var_coeff = outer_coeff_frac * inner_coeff_frac
        final_const_num = outer_coeff_frac * inner_const_frac
        
        # Rearrange: (final_var_coeff * variable + final_const_num) / divisor_val [operator] right_val - remainder_val
        target = right_frac - remainder_frac
        
        # Multiply by divisor
        if divisor_frac == 0:
            return "Division by zero"
        
        target *= divisor_frac
        
        if divisor_frac < 0:
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
        
        solution_str = format_fraction(float(solution))
        return f"{variable} {operator} {solution_str}"
        
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

def clean_inequality_text(text):
    """Clean spaces from inequality expressions while preserving structure."""
    if not text or text.strip() == '':
        return text
    
    # Remove spaces around numbers and operators, but preserve the inequality structure
    import re
    
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove spaces around operators and numbers
    text = re.sub(r'\s*([+\-])\s*', r'\1', text)  # Remove spaces around +/-
    text = re.sub(r'\s*([≤≥<>])\s*', r' \1 ', text)  # Keep spaces around inequality operators
    text = re.sub(r'\s*([()]/)\s*', r'\1', text)  # Remove spaces around parentheses and division
    text = re.sub(r'\s*/\s*', r'/', text)  # Remove spaces around division
    
    return text.strip()

def main():
    print("Creating a copy of alumnos.csv with cleaned inequalities and fraction solutions...")
    
    # Read from the original alumnos.csv file
    source_file = 'alumnos.csv'
    with open(source_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    print("Using original alumnos.csv as source...")
    
    # Process the data
    processed_lines = []
    variables = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    
    for i, line in enumerate(lines):
        if i < 2:  # Keep header rows as is
            processed_lines.append(line.rstrip('\n'))
        elif i > 119:  # Keep rows after 119 as is
            processed_lines.append(line.rstrip('\n'))
        else:  # Process rows 3-119 (indices 2-118)
            # Parse the line
            content = line.strip().split('|', 1)[1] if '|' in line else line.strip()
            row_data = content.split(',')
            
            # Keep first 5 columns as is (student info)
            new_row = row_data[:5]
            
            # Replace inequalities in columns 6-15 (C6:C15) with solutions
            for j in range(5, min(len(row_data), 15)):  # Columns 6-15 (indices 5-14)
                var_index = j - 5
                if var_index < len(variables):
                    inequality = row_data[j].strip()
                    variable = variables[var_index]
                    if inequality:  # Only solve if there's content
                        # Clean the inequality text first (remove extra spaces)
                        cleaned_inequality = clean_inequality_text(inequality)
                        # Then solve it
                        solution = solve_inequality(cleaned_inequality, variable)
                        new_row.append(solution)
                    else:
                        new_row.append('')  # Keep empty cells empty
                else:
                    new_row.append(row_data[j] if j < len(row_data) else '')
            
            # Handle any remaining columns beyond 15
            if len(row_data) > 15:
                new_row.extend(row_data[15:])
            
            # Add row number prefix if it was there originally
            if '|' in line:
                row_num = line.strip().split('|')[0]
                processed_lines.append(f"{row_num}|{','.join(new_row)}")
            else:
                processed_lines.append(','.join(new_row))
    
    # Write the modified data to a new file
    output_file = 'alumnos_with_fraction_solutions.csv'
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in processed_lines:
            file.write(line + '\n')
    
    print(f"Successfully created {output_file} with fraction solutions!")
    print(f"Modified {len([l for i, l in enumerate(processed_lines) if 2 <= i <= 118])} student records (rows 3-119)")
    print("Range C6R3:C15R119 now contains inequality solutions in simplified fraction form.")
    
    # Show a sample of the first few modified rows for verification
    print("\nSample of modified data:")
    for i in range(2, min(6, len(processed_lines))):  # Show rows 3-5
        line = processed_lines[i]
        content = line.split('|', 1)[1] if '|' in line else line
        row_data = content.split(',')
        if len(row_data) >= 5:
            name = row_data[2] if len(row_data) > 2 else "N/A"
            lastname = row_data[3] if len(row_data) > 3 else "N/A"
            print(f"Row {i+1}: {name} {lastname}")
            for k, var in enumerate(variables[:5]):  # Show first 5 variables
                col_index = k + 5  # Columns 6-10 are indices 5-9
                if col_index < len(row_data):
                    print(f"  {var}: {row_data[col_index]}")
            print()

if __name__ == "__main__":
    main()