import re
import pandas as pd

def parse_sas(sas_code):
    lines = sas_code.split('\n')
    data_statements = []
    proc_statements = []

    for i, line in enumerate(lines):
        if line.strip().upper().startswith('DATA'):
            # Extract the data step name
            match = re.search(r'DATA (\w+);', line)
            if match:
                data_name = match.group(1).strip()
                df = pd.DataFrame()
                data_statements.append((data_name, df))
        elif line.strip().upper().startswith('PROC'):
            proc_statements.append(line)

    # Parse input and cards statements
    for i, line in enumerate(lines):
        if 'input' in line.lower():
            match = re.search(r'(\w+)\s+([a-zA-Z]+);', line)
            if match:
                variable_name, variable_type = match.groups()
                df[variable_name] = pd.Series([], dtype=get_data_type(variable_type))
        elif 'cards' in line.lower():
            # Get the number of rows from the cards statement
            match = re.search(r'(.*?)\s*(\d+);', line)
            if match:
                num_rows = int(match.group(2))

    return {'data': data_statements, 'proc': proc_statements}

def get_data_type(type):
    type_map = {
        'char': str,
        'int': int,
        'float': float,
        'decimal': float
    }
    return type_map.get(type, object)

sas_code = """
data test;
input x y z;
cards;
1 2 3
4 5 6
7 8 9
;
run;

proc print test;
"""

result = parse_sas(sas_code)

print("Data Statements:")
for data_name, df in result['data']:
    print(f"Data Step: {data_name}")

# Print the input variables
print("\nInput Variables:")
for i, line in enumerate(result['data'][0][1].data):
    print(f"Variable {i+1}:")
    for column, value in line.items():
        print(f"{column}: {value}")
