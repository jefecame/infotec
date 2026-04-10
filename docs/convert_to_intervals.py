import csv
import re

def solution_to_interval(solution_text):
    """Convert a solution like 'A ≥ -10/27' to interval notation like '[-10/27;∞)'."""
    if not solution_text or solution_text.strip() == '':
        return solution_text
    
    # Handle special cases
    if "All values" in solution_text or "identity" in solution_text:
        return "(-∞;∞)"
    if "No solution" in solution_text or "contradiction" in solution_text:
        return "∅"
    if "error" in solution_text.lower():
        return solution_text  # Keep error messages as is
    
    # Parse the solution format: "Variable Operator Value"
    # Examples: "A ≥ -10/27", "B > -37/45", "C ≤ 1204/27", "D < 139/9"
    
    # Split by space to get parts
    parts = solution_text.strip().split()
    if len(parts) != 3:
        return solution_text  # Return original if format doesn't match
    
    variable, operator, value = parts
    
    # Convert based on operator - using semicolon instead of comma to avoid CSV conflicts
    if operator == '<':
        # x < value → (-∞; value)
        return f"(-∞;{value})"
    elif operator == '≤':
        # x ≤ value → (-∞; value]
        return f"(-∞;{value}]"
    elif operator == '>':
        # x > value → (value; ∞)
        return f"({value};∞)"
    elif operator == '≥':
        # x ≥ value → [value; ∞)
        return f"[{value};∞)"
    else:
        return solution_text  # Return original if operator not recognized

def main():
    print("Creating a copy of alumnos_with_fraction_solutions.csv with interval notation...")
    
    # Read from the fraction solutions file
    source_file = 'alumnos_with_fraction_solutions.csv'
    with open(source_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    print("Processing fraction solutions to interval notation...")
    
    # Process the data
    processed_lines = []
    
    for i, line in enumerate(lines):
        if i < 2:  # Keep header rows as is
            processed_lines.append(line.rstrip('\n'))
        else:  # Process data rows
            # Parse the line - handle both formats (with and without row numbers)
            if '|' in line:
                row_prefix, content = line.strip().split('|', 1)
                row_data = content.split(',')
                has_prefix = True
            else:
                content = line.strip()
                row_data = content.split(',')
                has_prefix = False
                row_prefix = ''
            
            # Keep first 5 columns as is (student info)
            new_row = row_data[:5]
            
            # Convert solutions in columns 6-15 (F1-F10) to interval notation
            for j in range(5, len(row_data)):  # Process columns 6 onwards
                if j < 15:  # Only process F1-F10 (columns 6-15)
                    solution = row_data[j].strip()
                    if solution:  # Only convert if there's content
                        interval = solution_to_interval(solution)
                        new_row.append(interval)
                    else:
                        new_row.append('')  # Keep empty cells empty
                else:
                    # Keep any additional columns as is
                    new_row.append(row_data[j])
            
            # Reconstruct the line
            if has_prefix:
                processed_lines.append(f"{row_prefix}|{','.join(new_row)}")
            else:
                processed_lines.append(','.join(new_row))
    
    # Write the modified data to a new file
    output_file = 'alumnos_with_intervals.csv'
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in processed_lines:
            file.write(line + '\n')
    
    print(f"Successfully created {output_file} with interval notation!")
    print(f"Converted solutions for {len(processed_lines) - 2} records")
    
    # Show a sample of the converted data
    print("\nSample of converted data:")
    for i in range(2, min(6, len(processed_lines))):  # Show rows 3-5
        line = processed_lines[i]
        content = line.split('|', 1)[1] if '|' in line else line
        row_data = content.split(',')
        if len(row_data) >= 5:
            name = row_data[2] if len(row_data) > 2 else "N/A"
            lastname = row_data[3] if len(row_data) > 3 else "N/A"
            print(f"Row {i+1}: {name} {lastname}")
            
            # Show first 5 interval conversions (F1-F5)
            variables = ['A', 'B', 'C', 'D', 'E']
            for k, var in enumerate(variables):
                col_index = k + 5  # Columns 6-10 are indices 5-9
                if col_index < len(row_data):
                    print(f"  {var}: {row_data[col_index]}")
            print()
    
    # Test some conversions for verification
    print("\nSample conversions:")
    test_cases = [
        "A ≥ -10/27",
        "B > -37/45", 
        "C ≤ 1204/27",
        "D < 139/9",
        "E ≥ 2381/87"
    ]
    
    for test in test_cases:
        result = solution_to_interval(test)
        print(f"{test} → {result}")
        
    print("\nNote: Using semicolons (;) instead of commas (,) in intervals to avoid CSV parsing conflicts.")

if __name__ == "__main__":
    main()