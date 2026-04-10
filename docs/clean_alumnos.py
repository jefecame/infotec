import csv
import re

def clean_mathematical_expression(expr):
    """Clean mathematical expressions by removing unnecessary spaces while preserving inequality operators."""
    if not expr.strip():
        return expr
    
    # First, protect the inequality operators by replacing them with placeholders
    expr = expr.replace('≤', '|||LEQ|||')
    expr = expr.replace('≥', '|||GEQ|||')
    expr = expr.replace('<', '|||LT|||')
    expr = expr.replace('>', '|||GT|||')
    
    # Remove all spaces
    expr = re.sub(r'\s+', '', expr)
    
    # Restore the inequality operators with single spaces around them
    expr = expr.replace('|||LEQ|||', ' ≤ ')
    expr = expr.replace('|||GEQ|||', ' ≥ ')
    expr = expr.replace('|||LT|||', ' < ')
    expr = expr.replace('|||GT|||', ' > ')
    
    return expr

def main():
    # Read the original CSV file
    with open('alumnos.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Process each line
    cleaned_lines = []
    for i, line in enumerate(lines):
        if i < 2:  # Header rows - keep as is
            cleaned_lines.append(line)
            continue
        
        # Parse the line
        content = line.strip().split('|', 1)[1] if '|' in line else line.strip()
        row_data = content.split(',')
        
        # Clean the mathematical expressions in columns 6-15 (indices 5-14)
        for j in range(5, min(15, len(row_data))):
            if row_data[j].strip():
                row_data[j] = clean_mathematical_expression(row_data[j])
        
        # Reconstruct the line
        row_number = str(i + 1)
        new_content = ','.join(row_data)
        cleaned_line = f"{row_number}|{new_content}\r\n"
        cleaned_lines.append(cleaned_line)
        
        # Show progress for first few lines
        if i <= 5:
            print(f"Line {i+1} cleaned:")
            print(f"  Original: {line.strip()}")
            print(f"  Cleaned:  {cleaned_line.strip()}")
            print()
    
    # Write the cleaned CSV file
    with open('alumnos_cleaned.csv', 'w', encoding='utf-8') as file:
        file.writelines(cleaned_lines)
    
    print(f"Created alumnos_cleaned.csv with {len(cleaned_lines)} lines")

if __name__ == "__main__":
    main()